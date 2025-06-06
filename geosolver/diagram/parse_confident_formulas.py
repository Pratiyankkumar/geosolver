import itertools
from geosolver.diagram.get_instances import get_all_instances
from geosolver.ontology.ontology_definitions import FormulaNode, signatures, FunctionSignature
import numpy as np

__author__ = 'minjoon'

def parse_confident_formulas(graph_parse):
    eps = 0.5 # to be updated by the scale of the diagram
    core_parse = graph_parse.core_parse
    line_graph = graph_parse.line_graph
    circle_dict = graph_parse.circle_dict
    confident_formulas = []

    # Debug: Print coordinate information
    print("=== COORDINATE INFORMATION ===")
    
    # Method 1: Check if core_parse has points attribute
    if hasattr(core_parse, 'points'):
        print("Points from core_parse.points:")
        for point_id, coords in core_parse.points.items():
            print(f"  {point_id}: {coords}")
    
    # Method 2: Check if core_parse has primitive_parse with points
    if hasattr(core_parse, 'primitive_parse') and hasattr(core_parse.primitive_parse, 'points'):
        print("Points from core_parse.primitive_parse.points:")
        for point_id, point_obj in core_parse.primitive_parse.points.items():
            print(f"  {point_id}: {point_obj}")
            if hasattr(point_obj, 'coordinate'):
                print(f"    coordinates: {point_obj.coordinate}")
    
    # Method 3: Try to evaluate point variables to get coordinates
    print("Attempting to evaluate point variables:")
    for point_key, point_var in core_parse.point_variables.items():
        try:
            if hasattr(core_parse, 'evaluate'):
                coords = core_parse.evaluate(point_var)
                print(f"  {point_key}: {coords}")
            elif hasattr(point_var, 'coordinate'):
                print(f"  {point_key}: {point_var.coordinate}")
        except Exception as e:
            print(f"  {point_key}: Could not get coordinates ({e})")

    print("\n=== FORMULAS WITH COORDINATES ===")
    
    for from_key, to_key, data in line_graph.edges(data=True):
        line_variable = FormulaNode(signatures['Line'],
                                     [core_parse.point_variables[from_key], core_parse.point_variables[to_key]])
        points = data['points']
        
        # Get coordinates for line endpoints
        from_coords = get_point_coordinates(core_parse, from_key)
        to_coords = get_point_coordinates(core_parse, to_key)
        print(f"Line from {from_key}{from_coords} to {to_key}{to_coords}")
        
        for point_key, point in points.items():
            point_variable = core_parse.point_variables[point_key]
            variable_node = FormulaNode(signatures['PointLiesOnLine'], [point_variable, line_variable])
            confident_formulas.append(variable_node)
            
            # Get coordinates for the point on line
            point_coords = get_point_coordinates(core_parse, point_key)
            # Also try to get coordinates from the 'point' object directly
            direct_coords = extract_coordinates_from_point(point)
            
            print(f"PointLiesOnLine({point_key}{point_coords},Line({from_key}{from_coords},{to_key}{to_coords}))")
            if direct_coords:
                print(f"  -> Point coordinates from data: {direct_coords}")

    for center_key, d in circle_dict.items():
        for radius_key, dd in d.items():
            circle_variable = FormulaNode(signatures['Circle'],
                                           [core_parse.point_variables[center_key],
                                            core_parse.radius_variables[center_key][radius_key]])
            points = dd['points']
            
            # Get center coordinates
            center_coords = get_point_coordinates(core_parse, center_key)
            print(f"Circle centered at {center_key}{center_coords}")
            
            for point_key, point in points.items():
                point_variable = core_parse.point_variables[point_key]
                variable_node = FormulaNode(signatures['PointLiesOnCircle'], [point_variable, circle_variable])
                confident_formulas.append(variable_node)
                
                # Get coordinates for the point on circle
                point_coords = get_point_coordinates(core_parse, point_key)
                direct_coords = extract_coordinates_from_point(point)
                
                print(f"PointLiesOnCircle({point_key}{point_coords},Circle({center_key}{center_coords},$radius_{center_key}_{radius_key}:number))")
                if direct_coords:
                    print(f"  -> Point coordinates from data: {direct_coords}")

    return confident_formulas

def get_point_coordinates(core_parse, point_key):
    """Helper function to extract coordinates from various possible locations"""
    # Try multiple methods to get coordinates
    
    # Method 1: Direct points dictionary
    if hasattr(core_parse, 'points') and point_key in core_parse.points:
        return core_parse.points[point_key]
    
    # Method 2: Through primitive_parse
    if (hasattr(core_parse, 'primitive_parse') and 
        hasattr(core_parse.primitive_parse, 'points') and 
        point_key in core_parse.primitive_parse.points):
        point_obj = core_parse.primitive_parse.points[point_key]
        if hasattr(point_obj, 'coordinate'):
            return point_obj.coordinate
        elif hasattr(point_obj, 'x') and hasattr(point_obj, 'y'):
            return (point_obj.x, point_obj.y)
    
    # Method 3: Try to evaluate the point variable
    if point_key in core_parse.point_variables:
        point_var = core_parse.point_variables[point_key]
        try:
            if hasattr(core_parse, 'evaluate'):
                return core_parse.evaluate(point_var)
        except:
            pass
    
    return None  # Coordinates not found

def extract_coordinates_from_point(point_obj):
    """Helper function to extract coordinates from a point object"""
    if point_obj is None:
        return None
    
    # Try different attribute names
    if hasattr(point_obj, 'coordinate'):
        return point_obj.coordinate
    elif hasattr(point_obj, 'x') and hasattr(point_obj, 'y'):
        return (point_obj.x, point_obj.y)
    elif isinstance(point_obj, (list, tuple, np.ndarray)) and len(point_obj) >= 2:
        return tuple(point_obj[:2])
    elif hasattr(point_obj, 'pos'):
        return point_obj.pos
    elif hasattr(point_obj, 'position'):
        return point_obj.position
    
    return None