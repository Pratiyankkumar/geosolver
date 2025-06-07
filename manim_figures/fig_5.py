from manim import *
import numpy as np

class GeometricFigure(Scene):
    def construct(self):
        # Define all points from the data
        points_data = {
            0: (126.37376120136904, 6.767385053914076),
            1: (36.783436689097066, 258.33711571447424),
            2: (154.3323116219668, 258.997190293742),
            3: (95.62088733798605, 97.26994017946161),
            4: (62.70476106732956, 7.938092935156291),
            5: (128.0649304200854, 187.67855865523487),
            6: (62.57934770853218, 186.80939646703138)
        }
        
        # Scale and center the coordinates
        x_coords = [p[0] for p in points_data.values()]
        y_coords = [p[1] for p in points_data.values()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        scale_x = 12 / (x_max - x_min) if x_max != x_min else 1
        scale_y = 6 / (y_max - y_min) if y_max != y_min else 1
        scale = min(scale_x, scale_y) * 0.85
        
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
            dot = Dot(coord, radius=0.06, color=BLUE)
            point_dots[i] = dot
            
            label = Text(str(i), font_size=18, color=WHITE)
            label.next_to(dot, UP + RIGHT, buff=0.08)
            point_labels[i] = label
        
        # Lines exactly from the formulas data
        lines_from_data = [
            (0, 1), (0, 3), (0, 6),
            (1, 2), (1, 3), (1, 6),
            (3, 2), (3, 4), (3, 5), (3, 6),
            (6, 5),
            (2, 4), (2, 5),
            (4, 5)
        ]
        
        # Create line objects
        line_objects = []
        for start_idx, end_idx in lines_from_data:
            start_point = manim_points[start_idx]
            end_point = manim_points[end_idx]
            line = Line(start_point, end_point, color=GRAY, stroke_width=1.5)
            line_objects.append(line)
        
        # Create circle centered at point 3 passing through points 0, 4, 5, 6
        center_point = manim_points[3]
        radius_point = manim_points[0]
        radius = np.linalg.norm(radius_point - center_point)
        circle = Circle(radius=radius, color=RED, stroke_width=2)
        circle.move_to(center_point)
        
        # Create a group containing all objects
        all_objects = VGroup(*line_objects, circle, *point_dots.values(), *point_labels.values())
        
        # Apply 180-degree rotation (upside down)
        all_objects.rotate(PI)
        
        # Add all objects to scene
        self.add(all_objects)
        
        self.wait(2)