from manim import *
import numpy as np

class GeometricFigure(Scene):
    def construct(self):
        # Define all points from the data
        points_data = {
            0: (62.266607510597474, 27.28414930261449),
            1: (131.64188267394275, 145.5231923601641),
            2: (209.02479338842977, 27.0),
            3: (18.51239669421488, 94.0),
            4: (165.28099173553719, 94.0),
            5: (101.25641025641025, 94.0),
            6: (7, 27),
            7: (219, 94),
            8: (147, 122),
            9: (226, 1),
            10: (0, 122),
            11: (80, 1),
            12: (47, 2),
            13: (116, 119)
        }
        
        # Scale and center the coordinates for better visualization
        # Find bounds
        x_coords = [p[0] for p in points_data.values()]
        y_coords = [p[1] for p in points_data.values()]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        # Scale factor to fit in screen
        scale_x = 12 / (x_max - x_min) if x_max != x_min else 1
        scale_y = 6 / (y_max - y_min) if y_max != y_min else 1
        scale = min(scale_x, scale_y) * 0.8  # Use 80% of available space
        
        # Center coordinates
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
            # Create dot
            dot = Dot(coord, radius=0.08, color=BLUE)
            point_dots[i] = dot
            
            # Create label
            label = Text(str(i), font_size=20, color=WHITE)
            label.next_to(dot, UP + RIGHT, buff=0.1)
            point_labels[i] = label
        
        # Define the lines based on the confident relationships
        confident_lines = [
            # Major lines that have multiple collinear points
            (0, 1),   # Line through points 0, 1 (with 5, 13 on it)
            (1, 2),   # Line through points 1, 2 (with 4, 8 on it)
            (1, 9),   # Line through points 1, 9 (with 2, 4, 8 on it)
            (1, 12),  # Line through points 1, 12 (with 0, 5, 13 on it)
            (2, 6),   # Line through points 2, 6 (with 0 on it)
            (2, 8),   # Line through points 2, 8 (with 4 on it)
            (3, 4),   # Line through points 3, 4 (with 5 on it)
            (3, 7),   # Line through points 3, 7 (with 4, 5 on it)
            (3, 11),  # Line through points 3, 11 (with 0 on it)
            (5, 7),   # Line through points 5, 7 (with 4 on it)
            (5, 12),  # Line through points 5, 12 (with 0 on it)
            (10, 11), # Line through points 10, 11 (with 0, 3 on it)
            (12, 13), # Line through points 12, 13 (with 0, 5 on it)
            (9, 4),   # Line through points 9, 4 (with 2 on it)
            (9, 8),   # Line through points 9, 8 (with 2, 4 on it)
        ]
        
        # Create line objects
        line_objects = []
        for start_idx, end_idx in confident_lines:
            start_point = manim_points[start_idx]
            end_point = manim_points[end_idx]
            
            # Extend line beyond the points for better visualization
            direction = end_point - start_point
            if np.linalg.norm(direction) > 0:
                direction = direction / np.linalg.norm(direction)
                extended_start = start_point - direction * 0.5
                extended_end = end_point + direction * 0.5
                
                line = Line(extended_start, extended_end, color=GRAY, stroke_width=1)
                line_objects.append(line)
        
        # Animation sequence
        self.play(
            Write(Text("Geometric Figure Analysis", font_size=36).to_edge(UP)),
            run_time=1
        )
        self.wait(0.5)
        
        # Draw all lines first (in background)
        self.play(
            *[Create(line) for line in line_objects],
            run_time=2
        )
        
        # Add points with labels
        self.play(
            *[Create(dot) for dot in point_dots.values()],
            *[Write(label) for label in point_labels.values()],
            run_time=2
        )
        
        # Highlight some key collinear relationships
        highlight_groups = [
            ([0, 1, 5, 13], RED, "Points 0, 1, 5, 13 are collinear"),
            ([1, 2, 4, 8], YELLOW, "Points 1, 2, 4, 8 are collinear"),
            ([3, 4, 5, 7], GREEN, "Points 3, 4, 5, 7 are collinear"),
            ([0, 10, 11, 3], ORANGE, "Points 0, 10, 11, 3 are collinear"),
        ]
        
        for i, (point_indices, color, description) in enumerate(highlight_groups):
            # Highlight points
            highlighted_dots = [point_dots[idx].copy().set_color(color).scale(1.5) 
                              for idx in point_indices]
            
            # Show description
            desc_text = Text(description, font_size=24, color=color)
            desc_text.to_edge(DOWN).shift(UP * i * 0.5)
            
            self.play(
                *[Transform(point_dots[idx], highlighted_dots[j]) 
                  for j, idx in enumerate(point_indices)],
                Write(desc_text),
                run_time=1.5
            )
            self.wait(1)
            
            # Restore original colors
            self.play(
                *[Transform(point_dots[idx], 
                           Dot(manim_points[idx], radius=0.08, color=BLUE)) 
                  for idx in point_indices],
                FadeOut(desc_text),
                run_time=0.5
            )
        
        # Final overview
        final_text = Text("Complex geometric figure with multiple\ncollinear point relationships", 
                         font_size=28, color=WHITE)
        final_text.to_edge(DOWN)
        
        self.play(Write(final_text))
        self.wait(3)
        
        # Clean fadeout
        self.play(
            *[FadeOut(obj) for obj in [*point_dots.values(), *point_labels.values(), 
                                      *line_objects, final_text]],
            run_time=2
        )
        self.wait(1)