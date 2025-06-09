"""
"instance" referring to any instance instantiated by instantiators.
Ex. point, line, circle, arc, triangle, quadrilateral
Exists returns True / False

"""
import numpy as np

from geosolver.diagram.computational_geometry import line_length, line_unit_vector, distance_between_points, \
    distance_between_line_and_point, distance_between_arc_and_point, arc_length, distance_between_circle_and_point, \
    circumference
from geosolver.diagram.states import CoreParse
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.parameters import LINE_EPS

__author__ = 'minjoon'


def instance_exists(diagram_parse, instance):
    """Main instance existence check function"""
    if isinstance(instance, instantiators['line']):
        return _line_exists(diagram_parse, instance)
    elif isinstance(instance, instantiators['arc']):
        return _arc_exists(diagram_parse, instance)
    elif isinstance(instance, instantiators['circle']):
        return _circle_exists_enhanced(diagram_parse, instance)  # Use enhanced version
    else:
        return False  # Unknown instance type


def _line_exists(diagram_parse, line):
    # TODO : smarter line_exists function needed (check continuity, etc.)
    eps = LINE_EPS
    multiplier = 1.0
    assert isinstance(diagram_parse, CoreParse)
    pixels = diagram_parse.primitive_parse.image_segment_parse.diagram_image_segment.pixels
    near_pixels = set(pixel for pixel in pixels if distance_between_line_and_point(line, pixel) <= eps)
    length = line_length(line)
    ratio = float(len(near_pixels))/length
    if ratio < multiplier:
        return False
    return True


def _arc_exists(diagram_parse, arc):
    eps = 4
    multiplier = 1
    assert isinstance(diagram_parse, CoreParse)
    pixels = diagram_parse.primitive_parse.image_segment_parse.diagram_image_segment.pixels
    near_pixels = set(pixel for pixel in pixels if distance_between_arc_and_point(arc, pixel) <= eps)
    length = arc_length(arc)
    ratio = float(len(near_pixels))/length
    if ratio < multiplier:
        return False
    return True


def _circle_exists(diagram_parse, circle):
    """Original circle existence check"""
    eps = 4
    multiplier = 2
    assert isinstance(diagram_parse, CoreParse)
    pixels = diagram_parse.primitive_parse.image_segment_parse.diagram_image_segment.pixels
    near_pixels = set(pixel for pixel in pixels if distance_between_circle_and_point(circle, pixel) <= eps)
    length = circumference(circle)
    if len(near_pixels) < multiplier*length:
        return False
    return True


def _circle_exists_enhanced(diagram_parse, circle):
    """Enhanced circle existence check that handles partial circles"""
    eps = 4
    multiplier = 1  # Reduced multiplier for partial circles
    
    assert isinstance(diagram_parse, CoreParse)
    pixels = diagram_parse.primitive_parse.image_segment_parse.diagram_image_segment.pixels
    
    # Get circle metadata from the global dictionary
    from geosolver.diagram.parse_primitives import get_circle_metadata
    metadata = get_circle_metadata(circle)
    arc_type = metadata.get('arc_type', 'full_circle')
    
    # Check if this is a partial circle
    is_partial = arc_type != 'full_circle'
    
    if is_partial:
        # For partial circles, be more lenient
        near_pixels = set(pixel for pixel in pixels 
                         if distance_between_circle_and_point(circle, pixel) <= eps * 1.5)
        expected_length = circumference(circle)
        
        # Adjust expected length for partial circles
        if arc_type == 'semicircle':
            expected_length *= 0.5
        elif arc_type == 'quarter_circle':
            expected_length *= 0.25
        elif arc_type == 'arc':
            expected_length *= 0.3  # Assume 30% coverage for general arcs
        
        ratio = float(len(near_pixels)) / expected_length
        return ratio >= multiplier * 0.5  # More lenient threshold
    else:
        # Original logic for full circles
        near_pixels = set(pixel for pixel in pixels 
                         if distance_between_circle_and_point(circle, pixel) <= eps)
        length = circumference(circle)
        ratio = float(len(near_pixels)) / length
        return ratio >= multiplier


def _distance_to_closest_point(point, points):
    return min(distance_between_points(point, p) for p in points)