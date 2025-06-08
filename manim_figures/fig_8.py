from manim import *
import numpy as np

class GeometricFigure(Scene):
    def construct(self):
        # Define all points from the data
        points_data = {
            0: (45.993506493506494, 76.5),
            1: (45.300676337678546, 0.8293173551397848),
            2: (0.20175438596491227, 76.33333333333333),
            3: (88.14718614718613, 76.33333333333333)
        }
        
        # Scale and center the coordinates
        x_coords = [p[0] for p in points_data.values()]
        y_coords = [p[1] for p in points_data.values()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        scale_x = 11 / (x_max - x_min) if x_max != x_min else 1
        scale_y = 5.5 / (y_max - y_min) if y_max != y_min else 1
        scale = min(scale_x, scale_y) * 0.9
        
        center_x = (x_min + x_max) / 2
        center_y = (y_min + y_max) / 2
        
        # Transform coordinates to Manim coordinate system
        manim_points = {}
        for i, (x, y) in points_data.items():
            manim_x = (x - center_x) * scale
            manim_y = (y - center_y) * scale
            manim_points[i] = np.array([manim_x, manim_y, 0])
        
        # Create point objects
        point_dots = {}
        point_labels = {}
        
        for i, coord in manim_points.items():
            dot = Dot(coord, radius=0.05, color=BLUE, fill_opacity=1.0)
            point_dots[i] = dot
            
            label = Text(str(i), font_size=16, color=WHITE)
            label.next_to(dot, UP + RIGHT, buff=0.1)
            point_labels[i] = label
        
        # Lines exactly from the formulas data
        lines_from_data = [
            (0, 1), (0, 2), (0, 3),
            (1, 2), (1, 3),
            (2, 3)
        ]
        
        # Create line objects
        line_objects = []
        for start_idx, end_idx in lines_from_data:
            start_point = manim_points[start_idx]
            end_point = manim_points[end_idx]
            line = Line(start_point, end_point, color=GRAY_C, stroke_width=1.5)
            line_objects.append(line)
        
        # Create organized groups
        lines_group = VGroup(*line_objects)
        points_group = VGroup(*point_dots.values())
        labels_group = VGroup(*point_labels.values())
        
        # Combine all objects
        all_objects = VGroup(lines_group, points_group, labels_group)
        
        # Add to scene
        self.add(all_objects)
        
        self.wait(2)