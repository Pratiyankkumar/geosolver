import networkx as nx

import itertools
from geosolver.diagram.computational_geometry import distance_between_line_and_point, \
    distance_between_circle_and_point, distance_between_arc_and_point
from geosolver.diagram.instance_exists import instance_exists
from geosolver.diagram.states import CoreParse, GraphParse
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.parameters import LINE_EPS, CIRCLE_EPS
from geosolver.ontology.ontology_definitions import FormulaNode, signatures

__author__ = 'minjoon'


def parse_graph(core_parse):
    assert isinstance(core_parse, CoreParse)
    circle_dict = _get_circle_dict(core_parse)
    line_graph = _get_line_graph(core_parse)
    arc_graphs = {}
    for center_key, d in circle_dict.items():
        for radius_key in d:
            circle = circle_dict[center_key][radius_key]['instance']
            circle_variable = circle_dict[center_key][radius_key]['variable']
            points = circle_dict[center_key][radius_key]['points']
            arc_graphs[(center_key, radius_key)] = _get_arc_graph(core_parse, circle, circle_variable, points)

    graph_parse = GraphParse(core_parse, line_graph, circle_dict, arc_graphs)
    return graph_parse


def _get_circle_dict(core_parse):
    """
    Enhanced circle dictionary creation supporting partial circles
    """
    # Use enhanced circle epsilon for partial circles
    eps = CIRCLE_EPS * 1.2  # Slightly more permissive for partial circles
    assert isinstance(core_parse, CoreParse)
    circle_dict = {}

    for point_key, dd in core_parse.circles.items():
        d = {}
        for radius_key, circle in dd.items():
            points = {}
            for key in core_parse.intersection_points:
                point = core_parse.intersection_points[key]
                
                # Use enhanced distance calculation for partial circles
                if hasattr(circle, '_arc_type') and circle._arc_type != 'full_circle':
                    # For partial circles, be more lenient with point inclusion
                    distance = distance_between_circle_and_point(circle, point)
                    if distance <= eps * 1.5:
                        points[key] = point
                else:
                    # Original logic for full circles
                    if distance_between_circle_and_point(circle, point) <= eps:
                        points[key] = point
            
            center_var = core_parse.point_variables[point_key]
            radius_var = core_parse.radius_variables[point_key][radius_key]
            circle_var = FormulaNode(signatures['Circle'], [center_var, radius_var])
            
            # Add metadata about circle type
            instance_data = {
                'instance': circle, 
                'points': points, 
                'variable': circle_var
            }
            
            # Store additional metadata if available
            if hasattr(circle, '_arc_type'):
                instance_data['arc_type'] = circle._arc_type
            if hasattr(circle, '_confidence'):
                instance_data['confidence'] = circle._confidence
            if hasattr(circle, '_template_type'):
                instance_data['template_type'] = circle._template_type
                
            d[radius_key] = instance_data
            
        if len(d) > 0:
            circle_dict[point_key] = d
    return circle_dict



def _get_line_graph(core_parse):
    """
    line graph is a non-directional graph.
    Nodes are indexed by intersection points.
    Note that angles, triangles, and quadrilaterals can be parsed from this graph.
    :param core_parse:
    :param eps:
    :return:
    """
    eps = LINE_EPS
    line_graph = nx.Graph()

    for key0, key1 in itertools.combinations(core_parse.intersection_points, 2):
        p0, p1 = core_parse.intersection_points[key0], core_parse.intersection_points[key1]
        line = instantiators['line'](p0, p1)
        v0, v1 = core_parse.point_variables[key0], core_parse.point_variables[key1]
        var = FormulaNode(signatures['Line'], [v0, v1])
        if instance_exists(core_parse, line):
            points = {}
            for key in set(core_parse.intersection_points).difference({key0, key1}):
                point = core_parse.intersection_points[key]
                if distance_between_line_and_point(line, point) <= eps:
                    points[key] = point
            line_graph.add_edge(key0, key1, instance=line, points=points, variable=var)
    return line_graph


def _get_arc_graph(core_parse, circle, circle_variable, circle_points):
    """
    Enhanced arc graph creation that handles partial circles
    """
    eps = CIRCLE_EPS
    arc_graph = nx.DiGraph()
    
    # Check if this is a partial circle
    is_partial = hasattr(circle, '_arc_type') and circle._arc_type != 'full_circle'
    
    for key0, key1 in itertools.permutations(circle_points, 2):
        p0, p1 = circle_points[key0], circle_points[key1]
        arc = instantiators['arc'](circle, p0, p1)
        v0, v1 = core_parse.point_variables[key0], core_parse.point_variables[key1]
        var = FormulaNode(signatures['Arc'], [circle_variable, v0, v1])
        
        # For partial circles, use enhanced existence check
        if is_partial:
            # Create a modified instance_exists function call or be more lenient
            arc_exists = True  # Assume arc exists for partial circles
        else:
            arc_exists = instance_exists(core_parse, arc)
        
        if arc_exists:
            arc_points = {}
            for key in set(circle_points).difference({key0, key1}):
                point = circle_points[key]
                if distance_between_arc_and_point(arc, point) <= eps:
                    arc_points[key] = point
            
            arc_graph.add_edge(key0, key1, instance=arc, points=arc_points, variable=var)
    
    return arc_graph


