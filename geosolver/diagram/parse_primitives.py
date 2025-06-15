import cv2
import numpy as np

from geosolver.diagram.states import ImageSegmentParse, PrimitiveParse
from geosolver.diagram.computational_geometry import dot_distance_between_points
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.parameters import hough_line_parameters as line_params
from geosolver.parameters import hough_circle_parameters as circle_params
from geosolver.utils.num import dimension_wise_non_maximum_suppression

__author__ = 'minjoon'

# Global dictionary to store circle metadata since we can't modify circle objects directly
_circle_metadata = {}

def get_circle_metadata(circle):
    """Get metadata for a circle object"""
    circle_key = (circle.center.x, circle.center.y, circle.radius)
    return _circle_metadata.get(circle_key, {})

def set_circle_metadata(circle, **metadata):
    """Set metadata for a circle object"""
    circle_key = (circle.center.x, circle.center.y, circle.radius)
    _circle_metadata[circle_key] = metadata

def parse_primitives(image_segment_parse):
    assert isinstance(image_segment_parse, ImageSegmentParse)
    diagram_segment = image_segment_parse.diagram_image_segment
    lines = _get_lines(diagram_segment, line_params)
    circles = _get_circles_enhanced(diagram_segment, circle_params)  # CHANGED
    line_dict = {idx: line for idx, line in enumerate(lines)}
    circle_dict = {idx+len(lines): circle for idx, circle in enumerate(circles)}
    primitive_parse = PrimitiveParse(image_segment_parse, line_dict, circle_dict)
    return primitive_parse

# Keep original _get_lines function unchanged
def _get_lines(image_segment, params):
    lines = []
    temp = cv2.HoughLines(image_segment.binarized_segmented_image, params.rho, params.theta, params.threshold)
    if temp is None:
        return lines

    rho_theta_pairs = [temp[idx][0] for idx in range(len(temp))]
    if len(rho_theta_pairs) > params.max_num:
        rho_theta_pairs = rho_theta_pairs[:params.max_num]

    nms_rho_theta_pairs = dimension_wise_non_maximum_suppression(rho_theta_pairs, (params.nms_rho, params.nms_theta),
                                                                 _dimension_wise_distances_between_rho_theta_pairs)

    for rho_theta_pair in rho_theta_pairs:
        curr_lines = _segment_line(image_segment, rho_theta_pair, params)
        lines.extend(curr_lines)

    return lines

# ENHANCED CIRCLE DETECTION - MAIN ADDITION
def _get_circles_enhanced(image_segment, params):
    """Enhanced circle detection supporting full circles, semicircles, and arcs"""
    circles = []
    
    # Clear metadata from previous runs
    global _circle_metadata
    _circle_metadata.clear()
    
    # Method 1: Original Hough circles (for perfect full circles)
    original_circles = _get_circles_original(image_segment, params)
    circles.extend(original_circles)
    print(f"Original Hough detected {len(original_circles)} circles")
    
    # Method 2: Contour-based detection (for partial circles and thick lines)
    contour_circles = _get_circles_from_contours(image_segment)
    circles.extend(contour_circles)
    print(f"Contour method detected {len(contour_circles)} circles")
    
    # Method 3: Template matching (for standard shapes)
    template_circles = _get_circles_from_templates(image_segment)
    circles.extend(template_circles)
    print(f"Template method detected {len(template_circles)} circles")
    
    # Remove duplicates
    final_circles = _remove_duplicate_circles(circles)
    print(f"Final: {len(final_circles)} circles after deduplication")
    
    return final_circles

def _get_circles_original(image_segment, params):
    """Original Hough circle detection"""
    temp = cv2.HoughCircles(image_segment.segmented_image, cv2.HOUGH_GRADIENT, params.dp, params.minDist,
                            param1=params.param1, param2=params.param2,
                            minRadius=params.minRadius, maxRadius=params.maxRadius)
    if temp is None:
        return []

    circle_tuples = temp[0]
    if len(circle_tuples) > params.max_num:
        circle_tuples = circle_tuples[:params.max_num]

    circles = []
    for x, y, radius in circle_tuples:
        circle = instantiators['circle'](instantiators['point'](x, y), radius)
        # Store metadata separately
        set_circle_metadata(circle, 
                           arc_type='full_circle',
                           detection_method='hough',
                           confidence=1.0)
        circles.append(circle)
    
    return circles

def _get_circles_from_contours(image_segment):
    """Detect circles and arcs using contour analysis"""
    circles = []
    
    # Preprocess image for better contour detection
    processed_image = _preprocess_for_contours(image_segment.segmented_image)
    
    # Find contours
    contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if len(contour) < 20:  # Skip very small contours
            continue
            
        # Check if contour could represent a circular shape
        circle_data = _analyze_contour_for_circle(contour)
        
        if circle_data is not None:
            center, radius, arc_type, confidence = circle_data
            
            # Create circle object
            circle = instantiators['circle'](
                instantiators['point'](center[0], center[1]), 
                radius
            )
            
            # Store metadata separately
            set_circle_metadata(circle,
                               arc_type=arc_type,
                               detection_method='contour',
                               confidence=confidence)
            circles.append(circle)
    
    return circles

def _preprocess_for_contours(image):
    """Preprocess image to improve contour detection for thick lines"""
    # Handle thick lines by thinning them
    kernel = np.ones((3,3), np.uint8)
    
    # If image is already binary, use it; otherwise binarize
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    # Adaptive threshold for robust binarization
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)
    
    # Morphological operations to clean up
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # Optional: thin thick lines
    thinned = cv2.morphologyEx(cleaned, cv2.MORPH_ERODE, kernel, iterations=1)
    
    return thinned

def _analyze_contour_for_circle(contour):
    """Analyze if contour represents a circle or circular arc"""
    try:
        # Fit circle to contour
        (x, y), radius = cv2.minEnclosingCircle(contour)
        
        if radius < 10 or radius > 300:  # Reasonable size limits
            return None
        
        # Check circularity
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            return None
            
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        
        # Calculate how much of the circle is covered
        points = contour.reshape(-1, 2)
        angles = []
        
        for point in points:
            angle = np.arctan2(point[1] - y, point[0] - x)
            angles.append(angle)
        
        angles = np.array(angles)
        angles = np.sort(angles)
        
        # Calculate angular coverage
        if len(angles) > 1:
            angle_diffs = np.diff(angles)
            max_gap = np.max(angle_diffs)
            total_coverage = 2 * np.pi - max_gap
            coverage_ratio = total_coverage / (2 * np.pi)
        else:
            coverage_ratio = 0
        
        # Determine circle type based on coverage
        if coverage_ratio > 0.8 and circularity > 0.7:
            arc_type = "full_circle"
            confidence = min(coverage_ratio, circularity)
        elif coverage_ratio > 0.4 and circularity > 0.5:
            if 0.4 < coverage_ratio < 0.6:
                arc_type = "semicircle"
            elif 0.2 < coverage_ratio < 0.35:
                arc_type = "quarter_circle"
            else:
                arc_type = "arc"
            confidence = min(coverage_ratio, circularity) * 0.8  # Lower confidence for partial
        else:
            return None  # Not circular enough
        
        # Validate by checking point distances to fitted circle
        distances = []
        for point in points:
            dist_to_center = np.linalg.norm(point - np.array([x, y]))
            dist_to_circle = abs(dist_to_center - radius)
            distances.append(dist_to_circle)
        
        avg_deviation = np.mean(distances)
        if avg_deviation > radius * 0.15:  # Too much deviation
            return None
        
        return (x, y), radius, arc_type, confidence
        
    except Exception as e:
        print(f"Error analyzing contour: {e}")
        return None

def _get_circles_from_templates(image_segment):
    """Detect circles using template matching for standard shapes with size validation"""
    circles = []
    image = image_segment.segmented_image
    
    # Check if image is large enough for template matching
    image_height, image_width = image.shape[:2]
    min_size = 30  # Minimum image size for template matching
    
    if image_width < min_size or image_height < min_size:
        print(f"Image too small ({image_width}x{image_height}) for template matching, skipping...")
        return circles
    
    # Create templates for different circle types
    templates = _create_circle_templates()
    
    for template_name, template in templates.items():
        # Check if template fits in image
        template_height, template_width = template.shape[:2]
        
        if template_width > image_width or template_height > image_height:
            print(f"Template {template_name} ({template_width}x{template_height}) too large for image ({image_width}x{image_height}), skipping...")
            continue
        
        matches = _match_template_multi_scale(image, template)
        
        for match in matches:
            x, y, scale, confidence = match
            radius = template.shape[0] // 2 * scale
            
            if confidence > 0.6 and 15 < radius < min(image_width, image_height) // 3:  # Adaptive size limits
                circle = instantiators['circle'](
                    instantiators['point'](x + radius, y + radius), 
                    radius
                )
                
                # Store metadata separately
                set_circle_metadata(circle,
                                   arc_type=template_name,
                                   detection_method='template',
                                   confidence=confidence)
                circles.append(circle)
    
    return circles


def _create_circle_templates():
    """Create templates for different circle types with adaptive sizing"""
    templates = {}
    
    # Use smaller base radius for better compatibility with small images
    radius = 20  # Reduced from 30
    size = radius * 2 + 4
    
    # Full circle template
    full_circle = np.zeros((size, size), dtype=np.uint8)
    cv2.circle(full_circle, (size//2, size//2), radius, 255, 2)
    templates['full_circle'] = full_circle
    
    # Semicircle templates
    semicircle_top = np.zeros((size, size), dtype=np.uint8)
    cv2.ellipse(semicircle_top, (size//2, size//2), (radius, radius), 0, 0, 180, 255, 2)
    templates['semicircle_top'] = semicircle_top
    
    semicircle_bottom = np.zeros((size, size), dtype=np.uint8)
    cv2.ellipse(semicircle_bottom, (size//2, size//2), (radius, radius), 0, 180, 360, 255, 2)
    templates['semicircle_bottom'] = semicircle_bottom
    
    return templates

def _match_template_multi_scale(image, template, scales=None):
    """Match template at multiple scales with size validation"""
    if scales is None:
        scales = np.arange(0.5, 2.0, 0.2)
    
    matches = []
    
    # Get image dimensions
    image_height, image_width = image.shape[:2]
    
    for scale in scales:
        # Scale template
        new_width = int(template.shape[1] * scale)
        new_height = int(template.shape[0] * scale)
        
        # Skip if scaled template is too small
        if new_width < 10 or new_height < 10:
            continue
        
        # CRITICAL FIX: Skip if template is larger than image
        if new_width > image_width or new_height > image_height:
            continue
            
        scaled_template = cv2.resize(template, (new_width, new_height))
        
        # Template matching
        try:
            result = cv2.matchTemplate(image, scaled_template, cv2.TM_CCOEFF_NORMED)
            
            # Find good matches
            locations = np.where(result >= 0.5)
            
            for pt in zip(*locations[::-1]):
                confidence = result[pt[1], pt[0]]
                matches.append((pt[0], pt[1], scale, confidence))
                
        except cv2.error as e:
            # Skip this scale if template matching fails
            print(f"Warning: Template matching failed at scale {scale}: {e}")
            continue
    
    return matches

def _remove_duplicate_circles(circles):
    """Remove duplicate circles that are too similar"""
    if len(circles) <= 1:
        return circles
    
    final_circles = []
    
    for circle in circles:
        is_duplicate = False
        
        for existing_circle in final_circles:
            # Check if circles are too similar
            center_dist = np.linalg.norm(
                np.array([circle.center.x, circle.center.y]) - 
                np.array([existing_circle.center.x, existing_circle.center.y])
            )
            radius_diff = abs(circle.radius - existing_circle.radius)
            
            # Consider duplicate if centers are close and radii are similar
            if center_dist < 20 and radius_diff < 10:
                is_duplicate = True
                break
        
        if not is_duplicate:
            final_circles.append(circle)
    
    return final_circles

# Keep all other original functions unchanged
def _segment_line(image_segment, rho_theta_pair, params):
    lines = []
    near_pixels = _get_pixels_near_rho_theta_pair(image_segment.pixels, rho_theta_pair, params.eps)
    if len(near_pixels) == 0:
        return lines

    reference_pixel = near_pixels[0]
    distances = [dot_distance_between_points(_rho_theta_pair_unit_vector(rho_theta_pair), p, reference_pixel)
                 for p in near_pixels]
    order = np.argsort(distances)
    start_idx = None
    end_idx = None

    for order_idx, idx in enumerate(order):
        if start_idx is None:
            start_idx = idx
            end_idx = idx
        else:
            d0 = distances[idx]
            d1 = distances[order[order_idx-1]]
            if abs(d0-d1) > params.max_gap or order_idx == len(order) - 1:
                length = abs(distances[start_idx] - distances[end_idx])
                if length > params.min_length:
                    p0 = near_pixels[start_idx]
                    p1 = near_pixels[end_idx]
                    line = instantiators['line'](p0, p1)
                    lines.append(line)
                start_idx = None
            else:
                end_idx = idx

    return lines

def _get_pixels_near_rho_theta_pair(pixels, rho_theta_pair, eps):
    near_pixels = [pixel for pixel in pixels
                   if _distance_between_rho_theta_pair_and_point(rho_theta_pair, pixel) <= eps]
    return near_pixels

def _distance_between_rho_theta_pair_and_point(rho_theta_pair, point):
    rho, theta = rho_theta_pair
    x, y = point
    return abs(rho - x*np.cos(theta) - y*np.sin(theta))

def _rho_theta_pair_unit_vector(rho_theta_pair):
    _, theta = rho_theta_pair
    return tuple([np.sin(theta), -np.cos(theta)])

def _dimension_wise_distances_between_rho_theta_pairs(pair0, pair1):
    rho0, theta0 = pair0
    rho1, theta1 = pair1
    rho_distance = abs(rho0 - rho1)
    theta_distance = min(abs(theta0-theta1),
                         abs(theta0-theta1+2*np.pi),
                         abs(theta0-theta1-2*np.pi))
    return rho_distance, theta_distance