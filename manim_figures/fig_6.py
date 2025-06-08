from manim import *
import numpy as np

class GeometricFigure(Scene):
    def construct(self):
        # Define all points from the data
        points_data = {
            0: (330.4946382511304, 74.51558764299868),
            1: (115.42989571263115, 240.48088064889953),
            2: (319.4837696353113, 309.2127155245504),
            3: (0.7460485210335216, 175.55510910517174),
            4: (183.16196388261852, 185.32308126410834),
            5: (227.17830882352882, 270.9577205882349),
            6: (131.90638805132812, 136.20012621835713),
            7: (-54.97936210131411, 194.00562851782342),
            8: (301.4534412955454, 291.21457489878503),
            9: (129.77541272972576, 229.38701415567857),
            10: (264, 281),
            11: (286, 287)
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
        
        # Create point objects with consistent sizing
        point_dots = {}
        point_labels = {}
        
        for i, coord in manim_points.items():
            dot = Dot(coord, radius=0.05, color=BLUE, fill_opacity=1.0)
            point_dots[i] = dot
            
            label = Text(str(i), font_size=16, color=WHITE)
            label.next_to(dot, UP + RIGHT, buff=0.1)
            point_labels[i] = label
        
        # Main structural lines based on confident collinear relationships
        main_lines = [
            (0, 1),   # Line with points 4, 9 collinear
            (3, 7),   # Line with points 0, 6 collinear  
            (1, 8),   # Line with points 5, 10, 11 collinear
            (3, 2),   # Line with points 5, 9 collinear
            (6, 2),   # Line with points 4, 8 collinear
        ]
        
        # Create line objects with consistent styling
        line_objects = []
        for start_idx, end_idx in main_lines:
            start_point = manim_points[start_idx]
            end_point = manim_points[end_idx]
            
            # Extend lines for better visibility
            direction = end_point - start_point
            length = np.linalg.norm(direction)
            if length > 0:
                direction = direction / length
                extended_start = start_point - direction * 1.2
                extended_end = end_point + direction * 1.2
                line = Line(extended_start, extended_end, color=GRAY_C, stroke_width=1.8)
            else:
                line = Line(start_point, end_point, color=GRAY_C, stroke_width=1.8)
            line_objects.append(line)
        
        # Create circle centered at point 4 with consistent styling
        center_point = manim_points[4]
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
        
        # Apply 180-degree rotation
        all_objects.rotate(PI)
        
        # Add to scene
        self.add(all_objects)
        
        self.wait(2)