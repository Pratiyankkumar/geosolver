import os
import cv2
import traceback

from geosolver import geoserver_interface
from geosolver.diagram.computational_geometry import normalize_angle, horizontal_angle, area_of_polygon
from geosolver.diagram.get_instances import get_all_instances
from geosolver.diagram.parse_confident_formulas import parse_confident_formulas, get_point_coordinates
from geosolver.diagram.parse_core import parse_core
from geosolver.diagram.parse_graph import parse_graph
from geosolver.diagram.parse_image_segments import parse_image_segments
from geosolver.diagram.parse_primitives import parse_primitives
from geosolver.diagram.select_primitives import select_primitives
from geosolver.utils.prep import open_image
import numpy as np

__author__ = 'minjoon'

# ====== IMPROVED MANIM INTEGRATION FUNCTIONS ======

def calculate_optimal_scaling_and_centering(points_data, canvas_width=14, canvas_height=8, margin=1.5):
    """
    Calculate optimal scaling and centering to fit all points within Manim canvas
    
    Args:
        points_data: Dictionary of {point_id: (x, y)} in pixel coordinates
        canvas_width: Manim canvas width (default ~14 for 16:9 aspect ratio)
        canvas_height: Manim canvas height (default ~8 for 16:9 aspect ratio)
        margin: Margin to leave around the geometry
    
    Returns:
        tuple: (scale_factor, center_offset_x, center_offset_y)
    """
    if not points_data:
        return 0.01, 0, 0
    
    # Convert to numpy array for easier computation
    coords = np.array(list(points_data.values()))
    
    # Find bounding box
    min_x, min_y = np.min(coords, axis=0)
    max_x, max_y = np.max(coords, axis=0)
    
    # Calculate dimensions
    width = max_x - min_x
    height = max_y - min_y
    
    # Avoid division by zero
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    
    # Calculate scale factor to fit within canvas with margin
    available_width = canvas_width - 2 * margin
    available_height = canvas_height - 2 * margin
    
    scale_x = available_width / width
    scale_y = available_height / height
    
    # Use the smaller scale to ensure everything fits
    scale_factor = min(scale_x, scale_y)
    
    # Calculate center offset to center the geometry
    geometry_center_x = (min_x + max_x) / 2
    geometry_center_y = (min_y + max_y) / 2
    
    # Center offset in Manim coordinates
    center_offset_x = -geometry_center_x * scale_factor
    center_offset_y = geometry_center_y * scale_factor  # Flip Y axis
    
    return scale_factor, center_offset_x, center_offset_y


def export_to_manim_improved(graph_parse):
    """
    Improved function to convert graph_parse to Manim-ready data with optimal scaling
    
    Args:
        graph_parse: Your GraphParse object from the pipeline
    
    Returns:
        Dictionary with all data needed for Manim scene
    """
    # First pass: Extract raw pixel coordinates
    raw_points = {}
    for point_key, point_var in graph_parse.core_parse.point_variables.items():
        coords = get_point_coordinates(graph_parse.core_parse, point_key)
        if coords is not None:
            if hasattr(coords, 'x') and hasattr(coords, 'y'):
                x, y = float(coords.x), float(coords.y)
            elif isinstance(coords, (tuple, list)) and len(coords) >= 2:
                x, y = float(coords[0]), float(coords[1])
            else:
                continue
            raw_points[point_key] = (x, y)
    
    # Calculate optimal scaling and centering
    scale_factor, center_offset_x, center_offset_y = calculate_optimal_scaling_and_centering(raw_points)
    
    print(f"Optimal scaling: scale={scale_factor:.6f}, center_offset=({center_offset_x:.3f}, {center_offset_y:.3f})")
    
    # Second pass: Apply scaling and centering
    points_data = {}
    for point_key, (x, y) in raw_points.items():
        # Apply scaling and centering
        manim_x = x * scale_factor + center_offset_x
        manim_y = -y * scale_factor + center_offset_y  # Flip Y axis
        points_data[point_key] = (manim_x, manim_y)
    
    # Extract line connections
    lines_data = []
    processed_lines = set()
    
    for from_key, to_key, data in graph_parse.line_graph.edges(data=True):
        line_key = tuple(sorted([from_key, to_key]))
        if line_key in processed_lines:
            continue
        processed_lines.add(line_key)
        
        if from_key in points_data and to_key in points_data:
            lines_data.append({
                'start': from_key,
                'end': to_key,
                'start_coords': points_data[from_key],
                'end_coords': points_data[to_key]
            })
    
    # Extract circle data
    circles_data = []
    for center_key, d in graph_parse.circle_dict.items():
        for radius_key, dd in d.items():
            if center_key in points_data:
                points_on_circle = []
                points = dd.get('points', {})
                
                for point_key in points.keys():
                    if point_key in points_data:
                        points_on_circle.append(point_key)
                
                if points_on_circle:
                    # Calculate radius in Manim coordinates
                    center_coords = np.array(points_data[center_key])
                    radius_coords = np.array(points_data[points_on_circle[0]])
                    radius = np.linalg.norm(radius_coords - center_coords)
                    
                    circles_data.append({
                        'center': center_key,
                        'center_coords': points_data[center_key],
                        'radius': radius,
                        'points_on_circle': points_on_circle
                    })
    
    return {
        'points': points_data,
        'lines': lines_data,
        'circles': circles_data,
        'scale_info': {
            'scale_factor': scale_factor,
            'center_offset': (center_offset_x, center_offset_y),
            'raw_bounds': {
                'min': (min(coord[0] for coord in raw_points.values()), min(coord[1] for coord in raw_points.values())),
                'max': (max(coord[0] for coord in raw_points.values()), max(coord[1] for coord in raw_points.values()))
            }
        }
    }


def save_reusable_manim_file(manim_data, filename="geometry_scene.py"):
    """
    Save reusable Manim code that can be imported into other files
    
    Args:
        manim_data: Dictionary returned by export_to_manim_improved
        filename: Name of the file to save
    """
    label_map = {0: "D", 1: "C", 2: "B", 3: "O", 4: "A", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I"}
    
    manim_code = """from manim import *
import numpy as np

def create_geometry_from_geosolver():
    \"\"\"
    Create a VGroup containing all geometry elements from GeoSolver.
    This function can be imported and used in other Manim files.
    
    Returns:
        VGroup: Contains all points, labels, lines, and circles
    
    Usage in other files:
        from geometry_scene import create_geometry_from_geosolver
        geometry = create_geometry_from_geosolver()
        self.add(geometry)
    \"\"\"
    
    # Point coordinates (centered and scaled)
    point_coords = {
"""
    
    # Add point coordinates using numpy arrays
    for point_id, (x, y) in manim_data['points'].items():
        manim_code += f"        {point_id}: np.array([{x:.6f}, {y:.6f}, 0]),\n"
    
    manim_code += "    }\n\n"
    
    # Add point creation
    manim_code += "    # Create points and labels\n"
    manim_code += "    points = {}\n"
    manim_code += "    labels = {}\n\n"
    
    for point_id in manim_data['points'].keys():
        label = label_map.get(point_id, f"P{point_id}")
        manim_code += f"    points[{point_id}] = Dot(point_coords[{point_id}], color=YELLOW, radius=0.06)\n"
        manim_code += f"    labels[{point_id}] = Text('{label}', font_size=20, color=WHITE).next_to(points[{point_id}], UP+RIGHT, buff=0.12)\n"
    
    manim_code += "\n    # Create lines\n"
    manim_code += "    lines = []\n"
    for i, line in enumerate(manim_data['lines']):
        start_id = line['start']
        end_id = line['end']
        manim_code += f"    lines.append(Line(point_coords[{start_id}], point_coords[{end_id}], color=WHITE, stroke_width=2))\n"
    
    manim_code += "\n    # Create circles\n"
    manim_code += "    circles = []\n"
    for i, circle in enumerate(manim_data['circles']):
        center_id = circle['center']
        radius = circle['radius']
        manim_code += f"    circles.append(Circle(radius={radius:.6f}, color=WHITE, stroke_width=2).move_to(point_coords[{center_id}]))\n"
    
    # Create the VGroup
    manim_code += """
    # Combine all objects into a VGroup for easy manipulation
    geometry_group = VGroup()
    
    # Add all points
    for point in points.values():
        geometry_group.add(point)
    
    # Add all labels
    for label in labels.values():
        geometry_group.add(label)
    
    # Add all lines
    for line in lines:
        geometry_group.add(line)
    
    # Add all circles
    for circle in circles:
        geometry_group.add(circle)
    
    return geometry_group


def get_geometry_components():
    \"\"\"
    Get individual components of the geometry for more control.
    
    Returns:
        dict: Contains 'points', 'labels', 'lines', 'circles', 'point_coords'
    \"\"\"
    
    # Point coordinates
    point_coords = {
"""
    
    # Add point coordinates again for the component function
    for point_id, (x, y) in manim_data['points'].items():
        manim_code += f"        {point_id}: np.array([{x:.6f}, {y:.6f}, 0]),\n"
    
    manim_code += "    }\n\n"
    
    # Component creation
    manim_code += "    # Create components\n"
    manim_code += "    points = {}\n"
    manim_code += "    labels = {}\n\n"
    
    for point_id in manim_data['points'].keys():
        label = label_map.get(point_id, f"P{point_id}")
        manim_code += f"    points[{point_id}] = Dot(point_coords[{point_id}], color=YELLOW, radius=0.06)\n"
        manim_code += f"    labels[{point_id}] = Text('{label}', font_size=20, color=WHITE).next_to(points[{point_id}], UP+RIGHT, buff=0.12)\n"
    
    manim_code += "\n    lines = []\n"
    for i, line in enumerate(manim_data['lines']):
        start_id = line['start']
        end_id = line['end']
        manim_code += f"    lines.append(Line(point_coords[{start_id}], point_coords[{end_id}], color=WHITE, stroke_width=2))\n"
    
    manim_code += "\n    circles = []\n"
    for i, circle in enumerate(manim_data['circles']):
        center_id = circle['center']
        radius = circle['radius']
        manim_code += f"    circles.append(Circle(radius={radius:.6f}, color=WHITE, stroke_width=2).move_to(point_coords[{center_id}]))\n"
    
    manim_code += """
    return {
        'points': points,
        'labels': labels,
        'lines': lines,
        'circles': circles,
        'point_coords': point_coords
    }


class GeometryScene(Scene):
    \"\"\"
    Main scene class that can be run directly.
    Run with: manim -pql geometry_scene.py GeometryScene
    \"\"\"
    
    def construct(self):
        # Create title
        title = Text("Geometry from GeoSolver", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        
        # Get the complete geometry as a VGroup
        geometry = create_geometry_from_geosolver()
        
        # Animation sequence
        self.play(Write(title))
        self.wait(1)
        
        # Get individual components for animated construction
        components = get_geometry_components()
        
        # Animate points and labels first
        point_animations = [Create(point) for point in components['points'].values()]
        label_animations = [Write(label) for label in components['labels'].values()]
        
        self.play(*point_animations, run_time=1.5)
        self.play(*label_animations, run_time=1.0)
        self.wait(0.5)
        
        # Animate lines
        for line in components['lines']:
            self.play(Create(line), run_time=0.8)
            self.wait(0.2)
        
        # Animate circles
        for circle in components['circles']:
            self.play(Create(circle), run_time=1.2)
            self.wait(0.3)
        
        # Final wait
        self.wait(2)


# Example of how to use in other files:
\"\"\"
# In your other Manim file:
from geometry_scene import create_geometry_from_geosolver, get_geometry_components

class MyCustomScene(Scene):
    def construct(self):
        # Option 1: Use complete geometry as VGroup
        geometry = create_geometry_from_geosolver()
        geometry.scale(0.8)  # Scale it down
        geometry.to_edge(LEFT)  # Move to left side
        self.add(geometry)
        
        # Option 2: Use individual components
        components = get_geometry_components()
        self.add(*components['points'].values())
        self.add(*components['lines'])
        # ... etc
        
        # Add your own content
        my_text = Text("My additional content")
        my_text.to_edge(RIGHT)
        self.add(my_text)
\"\"\"
"""
    
    # Write to file
    with open(filename, 'w') as f:
        f.write(manim_code)
    
    print(f"Reusable Manim scene saved to: {filename}")


def print_improved_manim_summary(manim_data):
    """Print detailed summary of extracted Manim data with scaling info"""
    print("\n" + "="*70)
    print("REUSABLE MANIM EXPORT SUMMARY:")
    print("="*70)
    
    scale_info = manim_data['scale_info']
    print(f"Scaling factor: {scale_info['scale_factor']:.6f}")
    print(f"Center offset: ({scale_info['center_offset'][0]:.3f}, {scale_info['center_offset'][1]:.3f})")
    
    raw_bounds = scale_info['raw_bounds']
    print(f"Original bounds: ({raw_bounds['min'][0]:.1f}, {raw_bounds['min'][1]:.1f}) to ({raw_bounds['max'][0]:.1f}, {raw_bounds['max'][1]:.1f})")
    
    print(f"\nGeometry extracted:")
    print(f"  Points: {len(manim_data['points'])}")
    print(f"  Lines: {len(manim_data['lines'])}")
    print(f"  Circles: {len(manim_data['circles'])}")
    
    print(f"\nFinal Manim coordinates (centered and scaled):")
    label_map = {0: "D", 1: "C", 2: "B", 3: "O", 4: "A", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I"}
    
    # Calculate bounds of final coordinates
    final_coords = np.array(list(manim_data['points'].values()))
    min_x, min_y = np.min(final_coords, axis=0)
    max_x, max_y = np.max(final_coords, axis=0)
    
    print(f"Final bounds: ({min_x:.3f}, {min_y:.3f}) to ({max_x:.3f}, {max_y:.3f})")
    print(f"Final size: {max_x - min_x:.3f} x {max_y - min_y:.3f}")
    
    print(f"\nPoint coordinates:")
    for point_id, (x, y) in manim_data['points'].items():
        label = label_map.get(point_id, f"P{point_id}")
        print(f"  {label:>2} (point_{point_id}): ({x:>7.3f}, {y:>7.3f})")
    
    print(f"\nUsage examples:")
    print(f"  Direct run: manim -pql geometry_scene.py GeometryScene")
    print(f"  In other files: from geometry_scene import create_geometry_from_geosolver")


# ====== ORIGINAL FUNCTIONS (UPDATED) ======

def test_local_diagram_step_by_step():
    """Test with local diagram image - step by step to isolate the error"""
    image_path = "geosolver/images/Circle-question-300x269.png"
    print(f"Processing image: {image_path}")
    
    try:
        print("Step 1: Opening image...")
        image = open_image(image_path)
        print(f"Image shape: {image.shape}")
        
        print("Step 2: Parsing image segments...")
        image_segment_parse = parse_image_segments(image)
        print("Image segments parsed successfully")
        
        print("Step 3: Parsing primitives...")
        primitive_parse = parse_primitives(image_segment_parse)
        print("Primitives parsed successfully")
        
        print("Step 4: Selecting primitives...")
        selected = select_primitives(primitive_parse)
        print("Primitives selected successfully")
        
        print("Step 5: Parsing core...")
        core_parse = parse_core(selected)
        print("Core parsed successfully")
        
        print("Step 6: Displaying points...")
        core_parse.display_points()
        print("Points displayed successfully")
        
        print("Step 7: Parsing graph...")
        graph_parse = parse_graph(core_parse)
        print("Graph parsed successfully")
        
        print("Step 8: Getting confident formulas...")
        confident_formulas = parse_confident_formulas(graph_parse)
        print("Confident information in the diagram:")
        for variable_node in confident_formulas:
            print(variable_node)
            
    except Exception as e:
        print(f"Error at step: {e}")
        print("Full traceback:")
        traceback.print_exc()


def test_local_diagram_with_reusable_manim_export():
    """Complete test with reusable Manim export - MAIN FUNCTION"""
    image_path = "geosolver/images/Circle-question-300x269.png"
    print(f"Processing image: {image_path}")
    
    try:
        print("Step 1: Opening image...")
        image = open_image(image_path)
        print(f"Image shape: {image.shape}")
        
        print("Step 2: Parsing image segments...")
        image_segment_parse = parse_image_segments(image)
        print("Image segments parsed successfully")
        
        print("Step 3: Parsing primitives...")
        primitive_parse = parse_primitives(image_segment_parse)
        print("Primitives parsed successfully")
        
        print("Step 4: Selecting primitives...")
        selected = select_primitives(primitive_parse)
        print("Primitives selected successfully")
        
        print("Step 5: Parsing core...")
        core_parse = parse_core(selected)
        print("Core parsed successfully")
        
        print("Step 6: Parsing graph...")
        graph_parse = parse_graph(core_parse)
        print("Graph parsed successfully")
        
        print("Step 7: Getting confident formulas...")
        confident_formulas = parse_confident_formulas(graph_parse)
        print("GeoSolver analysis completed successfully!")
        
        # ====== REUSABLE MANIM EXPORT ======
        print("\n" + "="*70)
        print("STARTING REUSABLE MANIM EXPORT...")
        print("="*70)
        
        # Export to Manim format with improved scaling
        manim_data = export_to_manim_improved(graph_parse)
        
        # Print detailed summary
        print_improved_manim_summary(manim_data)
        
        # Save reusable Manim file
        output_filename = "geometry_scene.py"
        save_reusable_manim_file(manim_data, output_filename)
        
        print(f"\n✅ SUCCESS! Reusable Manim scene saved to: {output_filename}")
        print("\n" + "="*70)
        print("USAGE OPTIONS:")
        print("="*70)
        print("1. Direct run: manim -pql geometry_scene.py GeometryScene")
        print("2. Import in other files:")
        print("   from geometry_scene import create_geometry_from_geosolver")
        print("   geometry = create_geometry_from_geosolver()")
        print("   self.add(geometry)")
        print("3. Use components:")
        print("   from geometry_scene import get_geometry_components")
        print("   components = get_geometry_components()")
        print("="*70)
        
        # Also show the confident formulas
        print(f"\nGeometric relationships found:")
        for formula in confident_formulas:
            print(f"  {formula}")
            
        return manim_data
            
    except Exception as e:
        print(f"Error: {e}")
        print("Full traceback:")
        traceback.print_exc()
        return None


def test_just_image_segments():
    """Test just the image segmentation step"""
    image_path = "geosolver/images/Circle-question-300x269.png"
    print(f"Testing just image segments for: {image_path}")
    
    try:
        image = open_image(image_path)
        print(f"Image loaded successfully, shape: {image.shape}")
        
        image_segment_parse = parse_image_segments(image)
        print("Image segments parsed successfully")
        print(f"Number of label segments: {len(image_segment_parse.label_image_segments)}")
        
        # Try to display the segmented image
        image_segment_parse.diagram_image_segment.display_binarized_segmented_image()
        
    except Exception as e:
        print(f"Error in image segmentation: {e}")
        traceback.print_exc()


def test_just_primitives():
    """Test just up to primitives parsing"""
    image_path = "geosolver/images/Circle-question-300x269.png"
    print(f"Testing primitives parsing for: {image_path}")
    
    try:
        image = open_image(image_path)
        image_segment_parse = parse_image_segments(image)
        print("Image segments OK")
        
        primitive_parse = parse_primitives(image_segment_parse)
        print("Primitives parsed successfully")
        
        primitive_parse.display_primitives()
        
    except Exception as e:
        print(f"Error in primitives parsing: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    print("="*70)
    print("REUSABLE GEOSOLVER TO MANIM PIPELINE")
    print("="*70)
    
    # Run the complete pipeline with reusable Manim export
    print("Running complete pipeline with reusable Manim export...")
    # test_local_diagram_with_reusable_manim_export()
    
    # Uncomment these if you want to test individual steps
    # print("\n=== Testing just image segments ===")
    # test_just_image_segments()
    
    # print("\n=== Testing up to primitives ===")
    # test_just_primitives()
    
    # print("\n=== Testing step by step ===")
    test_local_diagram_step_by_step()