from manim import *
import numpy as np

class GeometricFigure(Scene):
    def construct(self):
        # Define all points from the data
        points_data = {
            0: (118.19510598822515, 130.3946414223313),
            1: (993.1588105641695, 705.7859324852091),
            2: (-826.3877905853565, 127.2407753235882),
            3: (-51.169145470926765, 986.2086908309657),
            4: (448.67734562924363, 253.28771230768206),
            5: (292.099656094765, 482.87634696217043),
            6: (62.86396192837576, 409.98829857431366),
            7: (301.5393408477641, 131.00680915141157),
            8: (531.5482306391398, 131.77478541114905),
            9: (143.9861078099516, 0.07019858865169226),
            10: (232, 571),
            11: (588, 49),
            12: (0, 130),
            13: (599, 132),
            14: (31, 571),
            15: (180, 30),
            16: (547, 335),
            17: (0, 390),
            18: (412, 521)
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
        
        # Main structural lines based on confident collinear relationships
        main_lines = [
            (0, 3),   # Line with points 6, 14 collinear
            (12, 13), # Horizontal line with points 0, 7, 8 collinear
            (3, 9),   # Line with points 0, 6, 14 collinear
            (9, 1),   # Line with points 4, 7, 15, 16 collinear
            (6, 1),   # Line with points 5, 18 collinear
            (17, 18), # Line with points 5, 6 collinear
            (3, 11),  # Line with points 4, 5, 8, 10 collinear
        ]
        
        # Create line objects
        line_objects = []
        for start_idx, end_idx in main_lines:
            start_point = manim_points[start_idx]
            end_point = manim_points[end_idx]
            
            # Extend the main structural lines
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
        
        # Create organized groups
        lines_group = VGroup(*line_objects)
        points_group = VGroup(*point_dots.values())
        labels_group = VGroup(*point_labels.values())
        
        # Combine all objects
        all_objects = VGroup(lines_group, points_group, labels_group)
        
        # Add to scene
        self.add(all_objects)
        
        self.wait(2)