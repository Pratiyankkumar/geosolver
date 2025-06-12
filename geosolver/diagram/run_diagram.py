import sys
import traceback
import numpy as np

from geosolver.diagram.computational_geometry import normalize_angle, horizontal_angle, area_of_polygon
from geosolver.diagram.get_instances import get_all_instances
from geosolver.diagram.parse_confident_formulas import parse_confident_formulas, get_point_coordinates
from geosolver.diagram.parse_core import parse_core
from geosolver.diagram.parse_graph import parse_graph
from geosolver.diagram.parse_image_segments import parse_image_segments
from geosolver.diagram.parse_primitives import parse_primitives
from geosolver.diagram.select_primitives import select_primitives
from geosolver.utils.prep import open_image

__author__ = 'minjoon'

def generate_manim_from_image(image_path, output_filename="geometry_scene.py"):
    """
    Generate Manim code from a geometry image
    
    Args:
        image_path: Path to the geometry image
        output_filename: Name of the output Manim file
    
    Returns:
        Dictionary with Manim data or None if failed
    """
    print(f"Generating Manim code from: {image_path}")
    
    try:
        # Complete GeoSolver pipeline
        print("Step 1: Opening image...")
        image = open_image(image_path)
        
        print("Step 2: Parsing image segments...")
        image_segment_parse = parse_image_segments(image)
        
        print("Step 3: Enhanced primitive detection...")
        primitive_parse = parse_primitives(image_segment_parse)
        
        print("Step 4: Selecting primitives...")
        selected = select_primitives(primitive_parse)
        
        print("Step 5: Parsing core...")
        core_parse = parse_core(selected)
        
        print("Step 6: Parsing graph...")
        graph_parse = parse_graph(core_parse)
        
        print("Step 7: Getting confident formulas...")
        confident_formulas = parse_confident_formulas(graph_parse)
        
        # Export to Manim format
        print("\nExporting to Manim...")
        manim_data = _export_to_manim_improved(graph_parse)
        
        # Save Manim file
        _save_manim_file(manim_data, output_filename)
        
        print(f"\n✅ SUCCESS! Manim scene saved to: {output_filename}")
        print(f"Run with: manim -pql {output_filename} GeometryScene")
        
        # Show summary
        print(f"\nDetected geometry:")
        print(f"  Points: {len(manim_data['points'])}")
        print(f"  Lines: {len(manim_data['lines'])}")
        print(f"  Circles: {len(manim_data['circles'])}")
        
        return manim_data
        
    except Exception as e:
        print(f"Error generating Manim code: {e}")
        traceback.print_exc()
        return None


def show_detected_points(image_path):
    """
    Show the detected points overlaid on the original image
    
    Args:
        image_path: Path to the geometry image
    """
    print(f"Detecting and displaying points from: {image_path}")
    
    try:
        # Run GeoSolver pipeline up to point detection
        print("Step 1: Opening image...")
        image = open_image(image_path)
        
        print("Step 2: Parsing image segments...")
        image_segment_parse = parse_image_segments(image)
        
        print("Step 3: Enhanced primitive detection...")
        primitive_parse = parse_primitives(image_segment_parse)
        
        # Show detection results
        print(f"\nPrimitive detection results:")
        print(f"  Lines detected: {len(primitive_parse.lines)}")
        print(f"  Circles detected: {len(primitive_parse.circles)}")
        
        # Show circle details
        for idx, circle in primitive_parse.circles.items():
            from geosolver.diagram.parse_primitives import get_circle_metadata
            metadata = get_circle_metadata(circle)
            arc_type = metadata.get('arc_type', 'full_circle')
            detection_method = metadata.get('detection_method', 'unknown')
            print(f"  Circle {idx}: center=({circle.center.x:.1f}, {circle.center.y:.1f}), "
                  f"radius={circle.radius:.1f}, type={arc_type}, method={detection_method}")
        
        print("Step 4: Selecting primitives...")
        selected = select_primitives(primitive_parse)
        
        print("Step 5: Parsing core...")
        core_parse = parse_core(selected)
        
        print(f"\nFinal detected points: {len(core_parse.intersection_points)}")
        for key, point in core_parse.intersection_points.items():
            print(f"  Point {key}: ({point.x:.1f}, {point.y:.1f})")
        
        # Display the points on the image
        print("\nDisplaying points on image...")
        core_parse.display_points()
        
        return core_parse.intersection_points
        
    except Exception as e:
        print(f"Error detecting points: {e}")
        traceback.print_exc()
        return None


# ====== HELPER FUNCTIONS ======

def _export_to_manim_improved(graph_parse):
    """Convert graph_parse to Manim-ready data with optimal scaling"""
    # Extract raw pixel coordinates
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
    scale_factor, center_offset_x, center_offset_y = _calculate_scaling(raw_points)
    
    # Apply scaling and centering
    points_data = {}
    for point_key, (x, y) in raw_points.items():
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
            'center_offset': (center_offset_x, center_offset_y)
        }
    }


def _calculate_scaling(points_data, canvas_width=14, canvas_height=8, margin=1.5):
    """Calculate optimal scaling and centering for Manim canvas"""
    if not points_data:
        return 0.01, 0, 0
    
    coords = np.array(list(points_data.values()))
    min_x, min_y = np.min(coords, axis=0)
    max_x, max_y = np.max(coords, axis=0)
    
    width = max_x - min_x if max_x != min_x else 1
    height = max_y - min_y if max_y != min_y else 1
    
    available_width = canvas_width - 2 * margin
    available_height = canvas_height - 2 * margin
    
    scale_factor = min(available_width / width, available_height / height)
    
    geometry_center_x = (min_x + max_x) / 2
    geometry_center_y = (min_y + max_y) / 2
    
    center_offset_x = -geometry_center_x * scale_factor
    center_offset_y = geometry_center_y * scale_factor
    
    return scale_factor, center_offset_x, center_offset_y


def _save_manim_file(manim_data, filename):
    """Save Manim code to file using the exact template provided"""
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
        manim_code += f"    labels[{point_id}] = Text('{label}', font_size=20, color=BLACK).next_to(points[{point_id}], UP+RIGHT, buff=0.12)\n"
    
    manim_code += "\n    # Create lines\n"
    manim_code += "    lines = []\n"
    for i, line in enumerate(manim_data['lines']):
        start_id = line['start']
        end_id = line['end']
        manim_code += f"    lines.append(Line(point_coords[{start_id}], point_coords[{end_id}], color=BLACK, stroke_width=2))\n"
    
    manim_code += "\n    # Create circles\n"
    manim_code += "    circles = []\n"
    for i, circle in enumerate(manim_data['circles']):
        center_id = circle['center']
        radius = circle['radius']
        manim_code += f"    circles.append(Circle(radius={radius:.6f}, color=BLACK, stroke_width=2).move_to(point_coords[{center_id}]))\n"
    
    # Create the VGroup - EXACT TEMPLATE STRUCTURE
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
        manim_code += f"    labels[{point_id}] = Text('{label}', font_size=20, color=BLACK).next_to(points[{point_id}], UP+RIGHT, buff=0.12)\n"
    
    manim_code += "\n    lines = []\n"
    for i, line in enumerate(manim_data['lines']):
        start_id = line['start']
        end_id = line['end']
        manim_code += f"    lines.append(Line(point_coords[{start_id}], point_coords[{end_id}], color=BLACK, stroke_width=2))\n"
    
    manim_code += "\n    circles = []\n"
    for i, circle in enumerate(manim_data['circles']):
        center_id = circle['center']
        radius = circle['radius']
        manim_code += f"    circles.append(Circle(radius={radius:.6f}, color=BLACK, stroke_width=2).move_to(point_coords[{center_id}]))\n"
    
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
        title = Text("Geometry from GeoSolver", font_size=36, color=BLACK)
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


# ====== MAIN EXECUTION ======

if __name__ == "__main__":
    print("="*60)
    print("GEOSOLVER MAIN FUNCTIONS")
    print("="*60)
    
    # Default image path
    default_image = "geosolver/images/image.png"
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        # Check if custom image path is provided
        image_path = sys.argv[2] if len(sys.argv) > 2 else default_image
        
        if command == "manim":
            # Option 1: Generate Manim code from image
            print(f"Running Manim generation with image: {image_path}")
            generate_manim_from_image(image_path, "geometry_scene.py")
            
        elif command == "display":
            # Option 2: Show detected points on image
            print(f"Running point detection and display with image: {image_path}")
            show_detected_points(image_path)
            
        else:
            print(f"Unknown command: {command}")
            print("Usage:")
            print("  python -m geosolver.diagram.run_diagram manim [image_path]    # Generate Manim code")
            print("  python -m geosolver.diagram.run_diagram display [image_path]  # Show detected points")
            print("  If no image_path is provided, uses default: geosolver/images/image.png")
            sys.exit(1)
    else:
        # Default behavior (no arguments) - run display
        print("No command specified, running point detection and display...")
        print("Usage:")
        print("  python -m geosolver.diagram.run_diagram manim [image_path]    # Generate Manim code")
        print("  python -m geosolver.diagram.run_diagram display [image_path]  # Show detected points")
        print("  If no image_path is provided, uses default: geosolver/images/image.png")
        print(f"\nRunning default (display) with image: {default_image}...")
        show_detected_points(default_image)
    
    print("\n" + "="*60)
    print("DONE")
    print("="*60)