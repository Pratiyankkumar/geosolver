from manim import *
import numpy as np

class GeometricFigure(Scene):
    def construct(self):
        # Define all points from the data
        points_data = {
            0: (125.93589743589745, 98.6698717948718),
            1: (94.20211839602094, 56.436006979328575),
            2: (61.08736805203911, 98.32493280878745),
            3: (90.94624926166568, 98.48375664500885),
            4: (0, 56),
            5: (189, 56),
            6: (0, 98),
            7: (188, 99),
            8: (47, 0),
            9: (155, 135),
            10: (32, 136),
            11: (137, 0)
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
        
        # All confident collinear relationships from the data
        confident_lines = [
            # Line through points 0, 2, 3, 6, 7 (nearly horizontal line)
            (6, 7),   # Main line 6-7
            
            # Line through points 4, 1, 5 (horizontal line at y≈56)
            (4, 5),   # Main line 4-5
            
            # Line through points 8, 0, 1, 9 (diagonal line)
            (8, 9),   # Main line 8-9
            
            # Line through points 10, 1, 2, 11 (diagonal line)
            (10, 11), # Main line 10-11
            
            # Additional lines to show all relationships
            (0, 2),   # Line segment 0-2
            (2, 3),   # Line segment 2-3
            (0, 8),   # Line segment 0-8
            (1, 9),   # Line segment 1-9
            (1, 10),  # Line segment 1-10
            (2, 11),  # Line segment 2-11
        ]
        
        # Create line objects
        line_objects = []
        for start_idx, end_idx in confident_lines:
            start_point = manim_points[start_idx]
            end_point = manim_points[end_idx]
            
            # For main structural lines, extend them
            if (start_idx, end_idx) in [(6, 7), (4, 5), (8, 9), (10, 11)]:
                direction = end_point - start_point
                if np.linalg.norm(direction) > 0:
                    direction = direction / np.linalg.norm(direction)
                    extended_start = start_point - direction * 1.5
                    extended_end = end_point + direction * 1.5
                    line = Line(extended_start, extended_end, color=GRAY, stroke_width=2)
                else:
                    line = Line(start_point, end_point, color=GRAY, stroke_width=2)
            else:
                # For connecting segments, don't extend
                line = Line(start_point, end_point, color=LIGHT_GRAY, stroke_width=1.5)
            
            line_objects.append(line)
        
        # Add all lines first
        for line in line_objects:
            self.add(line)
        
        # Add all points and labels
        for dot in point_dots.values():
            self.add(dot)
        for label in point_labels.values():
            self.add(label)
        
        self.wait(2)