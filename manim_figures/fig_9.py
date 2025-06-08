from manim import *
import numpy as np

class GeometricFigure(Scene):
    def construct(self):
        # Define all points from the data
        points_data = {
            0: (66.34928138445139, 136.8249295604618),
            1: (88.0072344832056, 1.9549489000378486),
            2: (16.103913640381823, 27.280521818717578),
            3: (-80.61538461538521, 14.38461538461479),
            4: (134.679929154378, 43.090657220583736),
            5: (8.0, 103.0),
            6: (72.5, 67.5),
            7: (82.51834206765126, 36.135778942353504),
            8: (35.0, 130.0),
            9: (62.955974842766864, 157.95597484276686)
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
            (0, 1), (0, 7), (0, 8),
            (1, 6), (1, 7), (1, 9),
            (7, 2), (7, 4), (7, 6), (7, 9),
            (8, 5),
            (9, 5),
            (2, 4)
        ]
        
        # Create line objects
        line_objects = []
        for start_idx, end_idx in lines_from_data:
            start_point = manim_points[start_idx]
            end_point = manim_points[end_idx]
            line = Line(start_point, end_point, color=GRAY_C, stroke_width=1.5)
            line_objects.append(line)
        
        # Create circle centered at point 6 passing through points 0, 1, 2, 4, 8
        center_point = manim_points[6]
        radius_point = manim_points[0]
        radius = np.linalg.norm(radius_point - center_point)
        circle = Circle(radius=radius, color=RED_C, stroke_width=2.0, fill_opacity=0)
        circle.move_to(center_point)
        
        # Create organized groups
        lines_group = VGroup(*line_objects)
        points_group = VGroup(*point_dots.values())
        labels_group = VGroup(*point_labels.values())
        
        # Combine all objects
        all_objects = VGroup(lines_group, circle, points_group, labels_group)
        
        # Add to scene
        self.add(all_objects)
        
        self.wait(2)