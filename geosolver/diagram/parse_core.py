from sklearn.cluster import KMeans
import itertools
import numpy as np
from geosolver.diagram.states import PrimitiveParse, CoreParse
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.diagram.computational_geometry import intersections_between_lines, intersections_between_circle_and_line, \
    intersections_between_circles, distance_between_points
import geosolver.parameters as params
from geosolver.ontology.ontology_definitions import VariableSignature, FormulaNode

__author__ = 'minjoon'


def parse_core(primitive_parse):
    """Improved parse_core with line extension support"""
    
    # Step 1: Get all intersections including extended line intersections
    all_intersections = _get_all_intersections_with_line_extensions(primitive_parse, params.INTERSECTION_EPS)
    print(f"Debug: Found {len(all_intersections)} raw intersections (including line extensions)")
    
    # Step 2: Pre-filter obviously invalid intersections
    valid_intersections = _filter_valid_intersections(all_intersections, primitive_parse)
    print(f"Debug: {len(valid_intersections)} valid intersections after filtering")
    
    # Step 3: Improved clustering
    clustered_intersections = _cluster_intersections_improved(valid_intersections, params.KMEANS_RADIUS_THRESHOLD)
    print(f"Debug: {len(clustered_intersections)} points after clustering")
    
    # Step 4: Ensure line endpoints are preserved
    final_intersections = _add_missing_line_endpoints(clustered_intersections, primitive_parse)
    print(f"Debug: {len(final_intersections)} final points after adding endpoints")
    
    # Step 5: Create point variables and assignments
    intersections = dict(enumerate(final_intersections))
    assignment = {}
    point_variables = {}
    for idx in intersections.keys():
        id_ = "point_%d" % idx
        vs = VariableSignature(id_, 'point')
        point_variables[idx] = FormulaNode(vs, [])
        assignment[id_] = intersections[idx]
    
    # Step 6: Get circles
    circles = _get_circles(primitive_parse, intersections)
    
    # Step 7: Create radius variables
    radius_variables = {}
    for point_idx, d in circles.items():
        radius_variables[point_idx] = {}
        for radius_idx in d.keys():
            id_ = "radius_%d_%d" % (point_idx, radius_idx)
            vs = VariableSignature(id_, 'number')
            radius_variables[point_idx][radius_idx] = FormulaNode(vs, [])
            assignment[id_] = circles[point_idx][radius_idx].radius
    
    core_parse = CoreParse(primitive_parse, intersections, point_variables, circles, radius_variables, assignment)
    return core_parse


def _get_all_intersections_with_line_extensions(primitive_parse, eps):
    """Get intersections including extended line intersections"""
    assert isinstance(primitive_parse, PrimitiveParse)

    intersections = []
    
    # Get intersections between primitive pairs
    primitives_list = list(primitive_parse.primitives.values())
    for i, pr0 in enumerate(primitives_list):
        for j, pr1 in enumerate(primitives_list[i+1:], i+1):
            candidate_intersections = _get_intersections_between_primitives(pr0, pr1, eps)
            valid_candidates = _validate_intersection_points(candidate_intersections, primitive_parse)
            intersections.extend(valid_candidates)

    # Add line endpoints
    for line in primitive_parse.lines.values():
        if _is_significant_endpoint(line, primitive_parse):
            intersections.extend([line.a, line.b])

    # Add circle centers
    for circle in primitive_parse.circles.values():
        if _is_valid_circle_center(circle, primitive_parse):
            intersections.append(circle.center)
    
    # NEW: Add extended line-to-line intersections
    extended_intersections = _get_extended_line_intersections(primitive_parse, eps)
    intersections.extend(extended_intersections)
    print(f"Debug: Added {len(extended_intersections)} extended line intersections")

    return intersections


def _get_extended_line_intersections(primitive_parse, eps):
    """Find intersections between extended lines that don't currently intersect"""
    intersections = []
    lines = list(primitive_parse.lines.values())
    
    for i, line1 in enumerate(lines):
        for j, line2 in enumerate(lines[i+1:], i+1):
            # Check if lines already intersect within their segments
            existing_intersections = intersections_between_lines(line1, line2, eps)
            if existing_intersections:
                continue  # Skip if lines already intersect
            
            # Create extended versions of the lines
            extended_line1 = _extend_line_infinitely(line1)
            extended_line2 = _extend_line_infinitely(line2)
            
            # Find intersection of extended lines
            try:
                extended_intersections = intersections_between_lines(extended_line1, extended_line2, eps)
                
                for intersection in extended_intersections:
                    # Check if this intersection is beyond at least one of the original line segments
                    beyond_line1 = _is_point_beyond_line_segment(intersection, line1)
                    beyond_line2 = _is_point_beyond_line_segment(intersection, line2)
                    
                    if beyond_line1 or beyond_line2:
                        intersections.append(intersection)
                        print(f"Debug: Found extended intersection at ({intersection.x:.1f}, {intersection.y:.1f})")
            except Exception as e:
                print(f"Warning: Failed to find extended intersection: {e}")
                continue
    
    return intersections


def _extend_line_infinitely(line):
    """Create a very long line from the given line segment"""
    # Calculate direction vector
    dx = line.b.x - line.a.x
    dy = line.b.y - line.a.y
    length = np.sqrt(dx*dx + dy*dy)
    
    if length == 0:
        return line
    
    # Normalize direction
    dx_norm = dx / length
    dy_norm = dy / length
    
    # Extend by a very large distance
    extension = 5000  # Large enough for most diagram contexts
    
    # Create new extended endpoints
    new_a_x = line.a.x - dx_norm * extension
    new_a_y = line.a.y - dy_norm * extension
    new_b_x = line.b.x + dx_norm * extension
    new_b_y = line.b.y + dy_norm * extension
    
    new_a = instantiators['point'](new_a_x, new_a_y)
    new_b = instantiators['point'](new_b_x, new_b_y)
    
    return instantiators['line'](new_a, new_b)


def _is_point_beyond_line_segment(point, line_segment):
    """Check if a point lies beyond the endpoints of a line segment"""
    # Calculate parameter t for point on line: point = line.a + t * (line.b - line.a)
    dx = line_segment.b.x - line_segment.a.x
    dy = line_segment.b.y - line_segment.a.y
    
    # Handle degenerate case
    if abs(dx) < 1e-10 and abs(dy) < 1e-10:
        return False
    
    if abs(dx) > abs(dy):
        t = (point.x - line_segment.a.x) / dx if abs(dx) > 1e-10 else 0
    else:
        t = (point.y - line_segment.a.y) / dy if abs(dy) > 1e-10 else 0
    
    # Point is beyond the segment if t < 0 or t > 1
    # Use small tolerance for numerical errors
    return t < -0.05 or t > 1.05


def _add_missing_line_endpoints(clustered_points, primitive_parse):
    """Ensure important line endpoints aren't lost during clustering"""
    final_points = list(clustered_points)
    tolerance = getattr(params, 'ENDPOINT_TOLERANCE', 15.0)
    
    # Check each line endpoint
    for line in primitive_parse.lines.values():
        for endpoint in [line.a, line.b]:
            # Check if this endpoint is already represented in clustered points
            if not _is_point_near_any(endpoint, final_points, tolerance):
                final_points.append(endpoint)
                print(f"Debug: Added missing endpoint at ({endpoint.x:.1f}, {endpoint.y:.1f})")
    
    return final_points


def _is_point_near_any(target_point, point_list, tolerance):
    """Check if target point is within tolerance of any point in the list"""
    for point in point_list:
        if distance_between_points(target_point, point) <= tolerance:
            return True
    return False


# Keep all the original functions unchanged
def _validate_intersection_points(intersections, primitive_parse):
    """Filter out clearly invalid intersection points"""
    valid_intersections = []
    
    # Get image bounds if available
    try:
        image_segment = primitive_parse.image_segment_parse.diagram_image_segment
        height, width = image_segment.segmented_image.shape[:2]
        margin = max(width, height) * 0.3  # 30% margin for extensions
    except:
        # If we can't get image bounds, use a large bounding box
        height, width = 1000, 1000
        margin = 300
    
    for intersection in intersections:
        # Check if point is within reasonable image bounds
        if (-margin <= intersection.x <= width + margin and 
            -margin <= intersection.y <= height + margin):
            valid_intersections.append(intersection)
    
    return valid_intersections


def _is_significant_endpoint(line, primitive_parse):
    """Check if a line endpoint is likely to be a significant intersection"""
    threshold = getattr(params, 'ENDPOINT_SIGNIFICANCE_THRESHOLD', 10.0)
    
    for endpoint in [line.a, line.b]:
        is_significant = False
        
        # Check distance to other lines
        for other_line in primitive_parse.lines.values():
            if other_line != line:
                min_dist = min(
                    distance_between_points(endpoint, other_line.a),
                    distance_between_points(endpoint, other_line.b)
                )
                if min_dist < threshold:
                    is_significant = True
                    break
        
        # Check distance to circles
        if not is_significant:
            for circle in primitive_parse.circles.values():
                dist_to_center = distance_between_points(endpoint, circle.center)
                dist_to_circumference = abs(dist_to_center - circle.radius)
                if dist_to_circumference < threshold:
                    is_significant = True
                    break
        
        if is_significant:
            return True
    
    return False


def _is_valid_circle_center(circle, primitive_parse):
    """Check if a circle center should be included as an intersection point"""
    threshold = getattr(params, 'CIRCLE_CENTER_THRESHOLD', 15.0)
    
    for line in primitive_parse.lines.values():
        # Check if any line passes near the circle center
        from geosolver.diagram.computational_geometry import distance_between_line_and_point
        if distance_between_line_and_point(line, circle.center) < threshold:
            return True
    
    return True


def _filter_valid_intersections(intersections, primitive_parse):
    """Secondary filtering of intersections based on geometric validity"""
    if len(intersections) <= 3:
        return intersections
    
    valid_intersections = []
    
    # Calculate some statistics to identify outliers
    if len(intersections) >= 2:
        # Calculate pairwise distances
        distances = []
        for i, p1 in enumerate(intersections):
            for j, p2 in enumerate(intersections[i+1:], i+1):
                distances.append(distance_between_points(p1, p2))
        
        # Remove points that are isolated (too far from all others)
        if distances:
            median_distance = np.median(distances)
            max_isolation_distance = median_distance * 3.0
            
            for point in intersections:
                min_distance_to_others = float('inf')
                for other_point in intersections:
                    if point != other_point:
                        dist = distance_between_points(point, other_point)
                        min_distance_to_others = min(min_distance_to_others, dist)
                
                if min_distance_to_others <= max_isolation_distance:
                    valid_intersections.append(point)
        else:
            valid_intersections = intersections
    else:
        valid_intersections = intersections
    
    return valid_intersections


def _cluster_intersections_improved(intersections, radius_threshold):
    """Improved clustering that's more robust and efficient"""
    if len(intersections) == 0:
        return []
    
    if len(intersections) == 1:
        return [instantiators['point'](intersections[0].x, intersections[0].y)]
    
    # Convert to numpy array for easier processing
    points_array = np.array([[p.x, p.y] for p in intersections])
    
    # Use a more sophisticated approach to determine the number of clusters
    optimal_k = _find_optimal_clusters(points_array, radius_threshold)
    
    if optimal_k == 1:
        # All points should be in one cluster
        center_x = np.mean(points_array[:, 0])
        center_y = np.mean(points_array[:, 1])
        return [instantiators['point'](center_x, center_y)]
    
    # Perform K-means with optimal number of clusters
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    assignments = kmeans.fit_predict(points_array)
    
    # Create cluster centers
    centers = []
    for cluster_idx in range(optimal_k):
        cluster_points = points_array[assignments == cluster_idx]
        if len(cluster_points) > 0:
            center_x = np.mean(cluster_points[:, 0])
            center_y = np.mean(cluster_points[:, 1])
            centers.append(instantiators['point'](center_x, center_y))
    
    return centers


def _find_optimal_clusters(points_array, radius_threshold):
    """Find optimal number of clusters using the radius threshold constraint"""
    n_points = len(points_array)
    
    if n_points <= 1:
        return 1
    
    # Try different numbers of clusters
    for k in range(1, min(n_points + 1, 20)):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        assignments = kmeans.fit_predict(points_array)
        
        # Check if all clusters satisfy the radius threshold
        all_clusters_valid = True
        for cluster_idx in range(k):
            cluster_points = points_array[assignments == cluster_idx]
            if len(cluster_points) > 1:
                # Calculate radius of this cluster
                center = np.mean(cluster_points, axis=0)
                max_distance = np.max([np.linalg.norm(point - center) for point in cluster_points])
                
                if max_distance > radius_threshold:
                    all_clusters_valid = False
                    break
        
        if all_clusters_valid:
            return k
    
    # If no valid clustering found, return number of points
    return min(n_points, 20)


def _get_intersections_between_primitives(obj0, obj1, eps):
    """Intersections between two primitives with additional validation"""
    is_line0 = isinstance(obj0, instantiators['line'])
    is_circle0 = isinstance(obj0, instantiators['circle'])
    is_line1 = isinstance(obj1, instantiators['line'])
    is_circle1 = isinstance(obj1, instantiators['circle'])
    
    try:
        if is_line0 and is_line1:
            intersections = intersections_between_lines(obj0, obj1, eps)
        elif is_line0 and is_circle1:
            intersections = intersections_between_circle_and_line(obj1, obj0, eps)
        elif is_circle0 and is_line1:
            intersections = intersections_between_circle_and_line(obj0, obj1, eps)
        elif is_circle0 and is_circle1:
            intersections = intersections_between_circles(obj0, obj1)
        else:
            return []
        
        # Filter out any None or invalid intersections
        valid_intersections = [p for p in intersections if p is not None]
        return valid_intersections
        
    except Exception as e:
        print(f"Warning: Failed to calculate intersection between primitives: {e}")
        return []


def _get_circles(primitive_parse, intersection_points):
    """A dictionary of dictionaries for circles"""
    eps = getattr(params, 'CIRCLE_EPS', 5.0)
    circle_dict = {}
    
    for point_key, point in intersection_points.items():
        d = {}
        radius_key = 0
        for circle in primitive_parse.circles.values():
            if distance_between_points(point, circle.center) <= eps:
                d[radius_key] = circle
                radius_key += 1
        if len(d) > 0:
            circle_dict[point_key] = d
    
    return circle_dict