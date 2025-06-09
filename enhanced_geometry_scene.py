from manim import *
import numpy as np

def create_geometry_from_geosolver():
    """
    Create a VGroup containing all geometry elements from GeoSolver.
    This function can be imported and used in other Manim files.
    
    Returns:
        VGroup: Contains all points, labels, lines, and circles
    
    Usage in other files:
        from geometry_scene import create_geometry_from_geosolver
        geometry = create_geometry_from_geosolver()
        self.add(geometry)
    """
    
    # Point coordinates (centered and scaled)
    point_coords = {
        0: np.array([0.010701, -0.439377, 0]),
        1: np.array([-1.264682, -0.647303, 0]),
        2: np.array([1.889308, 2.500000, 0]),
        3: np.array([3.833513, -1.310254, 0]),
        4: np.array([-0.586666, 0.370044, 0]),
        5: np.array([-1.939136, -1.323867, 0]),
        6: np.array([0.595873, -1.300146, 0]),
        7: np.array([-3.833513, -2.500000, 0]),
        8: np.array([0.885200, 0.926685, 0]),
        9: np.array([-0.805194, -0.230097, 0]),
        10: np.array([2.255677, -1.305056, 0]),
        11: np.array([-0.535385, -1.299200, 0]),
        12: np.array([-0.335977, 0.016745, 0]),
        13: np.array([-2.308658, -1.697966, 0]),
        14: np.array([0.252997, -0.736461, 0]),
        15: np.array([-0.448830, 0.161863, 0]),
        16: np.array([-0.372090, -0.349215, 0]),
        17: np.array([-0.979347, -0.343102, 0]),
        18: np.array([-1.585474, -1.294068, 0]),
        19: np.array([-1.473599, -0.944814, 0]),
        20: np.array([0.475467, -1.299190, 0]),
        21: np.array([-0.005949, -0.486800, 0]),
        22: np.array([-1.356588, -0.740881, 0]),
        23: np.array([-1.142625, -0.526918, 0]),
        24: np.array([0.044199, -0.513546, 0]),
        25: np.array([-0.497394, -0.329672, 0]),
        26: np.array([-0.143018, -0.409908, 0]),
        27: np.array([-0.724729, -0.346387, 0]),
        28: np.array([0.147837, -0.597125, 0]),
        29: np.array([0.375172, -0.898010, 0]),
        30: np.array([-0.992183, -0.436653, 0]),
    }

    # Create points and labels
    points = {}
    labels = {}

    points[0] = Dot(point_coords[0], color=YELLOW, radius=0.06)
    labels[0] = Text('D', font_size=20, color=WHITE).next_to(points[0], UP+RIGHT, buff=0.12)
    points[1] = Dot(point_coords[1], color=YELLOW, radius=0.06)
    labels[1] = Text('C', font_size=20, color=WHITE).next_to(points[1], UP+RIGHT, buff=0.12)
    points[2] = Dot(point_coords[2], color=YELLOW, radius=0.06)
    labels[2] = Text('B', font_size=20, color=WHITE).next_to(points[2], UP+RIGHT, buff=0.12)
    points[3] = Dot(point_coords[3], color=YELLOW, radius=0.06)
    labels[3] = Text('O', font_size=20, color=WHITE).next_to(points[3], UP+RIGHT, buff=0.12)
    points[4] = Dot(point_coords[4], color=YELLOW, radius=0.06)
    labels[4] = Text('A', font_size=20, color=WHITE).next_to(points[4], UP+RIGHT, buff=0.12)
    points[5] = Dot(point_coords[5], color=YELLOW, radius=0.06)
    labels[5] = Text('E', font_size=20, color=WHITE).next_to(points[5], UP+RIGHT, buff=0.12)
    points[6] = Dot(point_coords[6], color=YELLOW, radius=0.06)
    labels[6] = Text('F', font_size=20, color=WHITE).next_to(points[6], UP+RIGHT, buff=0.12)
    points[7] = Dot(point_coords[7], color=YELLOW, radius=0.06)
    labels[7] = Text('G', font_size=20, color=WHITE).next_to(points[7], UP+RIGHT, buff=0.12)
    points[8] = Dot(point_coords[8], color=YELLOW, radius=0.06)
    labels[8] = Text('H', font_size=20, color=WHITE).next_to(points[8], UP+RIGHT, buff=0.12)
    points[9] = Dot(point_coords[9], color=YELLOW, radius=0.06)
    labels[9] = Text('I', font_size=20, color=WHITE).next_to(points[9], UP+RIGHT, buff=0.12)
    points[10] = Dot(point_coords[10], color=YELLOW, radius=0.06)
    labels[10] = Text('P10', font_size=20, color=WHITE).next_to(points[10], UP+RIGHT, buff=0.12)
    points[11] = Dot(point_coords[11], color=YELLOW, radius=0.06)
    labels[11] = Text('P11', font_size=20, color=WHITE).next_to(points[11], UP+RIGHT, buff=0.12)
    points[12] = Dot(point_coords[12], color=YELLOW, radius=0.06)
    labels[12] = Text('P12', font_size=20, color=WHITE).next_to(points[12], UP+RIGHT, buff=0.12)
    points[13] = Dot(point_coords[13], color=YELLOW, radius=0.06)
    labels[13] = Text('P13', font_size=20, color=WHITE).next_to(points[13], UP+RIGHT, buff=0.12)
    points[14] = Dot(point_coords[14], color=YELLOW, radius=0.06)
    labels[14] = Text('P14', font_size=20, color=WHITE).next_to(points[14], UP+RIGHT, buff=0.12)
    points[15] = Dot(point_coords[15], color=YELLOW, radius=0.06)
    labels[15] = Text('P15', font_size=20, color=WHITE).next_to(points[15], UP+RIGHT, buff=0.12)
    points[16] = Dot(point_coords[16], color=YELLOW, radius=0.06)
    labels[16] = Text('P16', font_size=20, color=WHITE).next_to(points[16], UP+RIGHT, buff=0.12)
    points[17] = Dot(point_coords[17], color=YELLOW, radius=0.06)
    labels[17] = Text('P17', font_size=20, color=WHITE).next_to(points[17], UP+RIGHT, buff=0.12)
    points[18] = Dot(point_coords[18], color=YELLOW, radius=0.06)
    labels[18] = Text('P18', font_size=20, color=WHITE).next_to(points[18], UP+RIGHT, buff=0.12)
    points[19] = Dot(point_coords[19], color=YELLOW, radius=0.06)
    labels[19] = Text('P19', font_size=20, color=WHITE).next_to(points[19], UP+RIGHT, buff=0.12)
    points[20] = Dot(point_coords[20], color=YELLOW, radius=0.06)
    labels[20] = Text('P20', font_size=20, color=WHITE).next_to(points[20], UP+RIGHT, buff=0.12)
    points[21] = Dot(point_coords[21], color=YELLOW, radius=0.06)
    labels[21] = Text('P21', font_size=20, color=WHITE).next_to(points[21], UP+RIGHT, buff=0.12)
    points[22] = Dot(point_coords[22], color=YELLOW, radius=0.06)
    labels[22] = Text('P22', font_size=20, color=WHITE).next_to(points[22], UP+RIGHT, buff=0.12)
    points[23] = Dot(point_coords[23], color=YELLOW, radius=0.06)
    labels[23] = Text('P23', font_size=20, color=WHITE).next_to(points[23], UP+RIGHT, buff=0.12)
    points[24] = Dot(point_coords[24], color=YELLOW, radius=0.06)
    labels[24] = Text('P24', font_size=20, color=WHITE).next_to(points[24], UP+RIGHT, buff=0.12)
    points[25] = Dot(point_coords[25], color=YELLOW, radius=0.06)
    labels[25] = Text('P25', font_size=20, color=WHITE).next_to(points[25], UP+RIGHT, buff=0.12)
    points[26] = Dot(point_coords[26], color=YELLOW, radius=0.06)
    labels[26] = Text('P26', font_size=20, color=WHITE).next_to(points[26], UP+RIGHT, buff=0.12)
    points[27] = Dot(point_coords[27], color=YELLOW, radius=0.06)
    labels[27] = Text('P27', font_size=20, color=WHITE).next_to(points[27], UP+RIGHT, buff=0.12)
    points[28] = Dot(point_coords[28], color=YELLOW, radius=0.06)
    labels[28] = Text('P28', font_size=20, color=WHITE).next_to(points[28], UP+RIGHT, buff=0.12)
    points[29] = Dot(point_coords[29], color=YELLOW, radius=0.06)
    labels[29] = Text('P29', font_size=20, color=WHITE).next_to(points[29], UP+RIGHT, buff=0.12)
    points[30] = Dot(point_coords[30], color=YELLOW, radius=0.06)
    labels[30] = Text('P30', font_size=20, color=WHITE).next_to(points[30], UP+RIGHT, buff=0.12)

    # Create lines
    lines = []
    lines.append(Line(point_coords[0], point_coords[11], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[0], point_coords[14], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[0], point_coords[16], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[0], point_coords[21], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[0], point_coords[25], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[0], point_coords[29], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[5], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[6], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[8], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[10], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[18], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[20], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[21], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[14], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[14], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[14], point_coords[28], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[14], point_coords[29], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[17], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[21], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[25], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[27], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[28], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[7], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[13], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[18], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[20], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[28], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[25], point_coords[17], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[25], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[25], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[25], point_coords[27], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[25], point_coords[28], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[25], point_coords[30], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[29], point_coords[20], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[29], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[29], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[29], point_coords[28], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[1], point_coords[9], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[1], point_coords[17], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[1], point_coords[19], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[1], point_coords[22], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[1], point_coords[23], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[1], point_coords[30], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[9], point_coords[22], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[9], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[17], point_coords[22], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[19], point_coords[18], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[19], point_coords[22], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[19], point_coords[23], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[22], point_coords[18], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[22], point_coords[23], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[22], point_coords[30], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[23], point_coords[5], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[23], point_coords[27], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[23], point_coords[30], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[30], point_coords[27], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[3], point_coords[18], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[18], point_coords[6], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[18], point_coords[10], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[18], point_coords[20], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[18], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[4], point_coords[20], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[20], point_coords[5], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[20], point_coords[12], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[20], point_coords[15], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[20], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[5], point_coords[6], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[26], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[26], point_coords[28], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[24], point_coords[28], color=WHITE, stroke_width=2))

    # Create circles
    circles = []

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
    """
    Get individual components of the geometry for more control.
    
    Returns:
        dict: Contains 'points', 'labels', 'lines', 'circles', 'point_coords'
    """
    
    # Point coordinates
    point_coords = {
        0: np.array([0.010701, -0.439377, 0]),
        1: np.array([-1.264682, -0.647303, 0]),
        2: np.array([1.889308, 2.500000, 0]),
        3: np.array([3.833513, -1.310254, 0]),
        4: np.array([-0.586666, 0.370044, 0]),
        5: np.array([-1.939136, -1.323867, 0]),
        6: np.array([0.595873, -1.300146, 0]),
        7: np.array([-3.833513, -2.500000, 0]),
        8: np.array([0.885200, 0.926685, 0]),
        9: np.array([-0.805194, -0.230097, 0]),
        10: np.array([2.255677, -1.305056, 0]),
        11: np.array([-0.535385, -1.299200, 0]),
        12: np.array([-0.335977, 0.016745, 0]),
        13: np.array([-2.308658, -1.697966, 0]),
        14: np.array([0.252997, -0.736461, 0]),
        15: np.array([-0.448830, 0.161863, 0]),
        16: np.array([-0.372090, -0.349215, 0]),
        17: np.array([-0.979347, -0.343102, 0]),
        18: np.array([-1.585474, -1.294068, 0]),
        19: np.array([-1.473599, -0.944814, 0]),
        20: np.array([0.475467, -1.299190, 0]),
        21: np.array([-0.005949, -0.486800, 0]),
        22: np.array([-1.356588, -0.740881, 0]),
        23: np.array([-1.142625, -0.526918, 0]),
        24: np.array([0.044199, -0.513546, 0]),
        25: np.array([-0.497394, -0.329672, 0]),
        26: np.array([-0.143018, -0.409908, 0]),
        27: np.array([-0.724729, -0.346387, 0]),
        28: np.array([0.147837, -0.597125, 0]),
        29: np.array([0.375172, -0.898010, 0]),
        30: np.array([-0.992183, -0.436653, 0]),
    }

    # Create components
    points = {}
    labels = {}

    points[0] = Dot(point_coords[0], color=YELLOW, radius=0.06)
    labels[0] = Text('D', font_size=20, color=WHITE).next_to(points[0], UP+RIGHT, buff=0.12)
    points[1] = Dot(point_coords[1], color=YELLOW, radius=0.06)
    labels[1] = Text('C', font_size=20, color=WHITE).next_to(points[1], UP+RIGHT, buff=0.12)
    points[2] = Dot(point_coords[2], color=YELLOW, radius=0.06)
    labels[2] = Text('B', font_size=20, color=WHITE).next_to(points[2], UP+RIGHT, buff=0.12)
    points[3] = Dot(point_coords[3], color=YELLOW, radius=0.06)
    labels[3] = Text('O', font_size=20, color=WHITE).next_to(points[3], UP+RIGHT, buff=0.12)
    points[4] = Dot(point_coords[4], color=YELLOW, radius=0.06)
    labels[4] = Text('A', font_size=20, color=WHITE).next_to(points[4], UP+RIGHT, buff=0.12)
    points[5] = Dot(point_coords[5], color=YELLOW, radius=0.06)
    labels[5] = Text('E', font_size=20, color=WHITE).next_to(points[5], UP+RIGHT, buff=0.12)
    points[6] = Dot(point_coords[6], color=YELLOW, radius=0.06)
    labels[6] = Text('F', font_size=20, color=WHITE).next_to(points[6], UP+RIGHT, buff=0.12)
    points[7] = Dot(point_coords[7], color=YELLOW, radius=0.06)
    labels[7] = Text('G', font_size=20, color=WHITE).next_to(points[7], UP+RIGHT, buff=0.12)
    points[8] = Dot(point_coords[8], color=YELLOW, radius=0.06)
    labels[8] = Text('H', font_size=20, color=WHITE).next_to(points[8], UP+RIGHT, buff=0.12)
    points[9] = Dot(point_coords[9], color=YELLOW, radius=0.06)
    labels[9] = Text('I', font_size=20, color=WHITE).next_to(points[9], UP+RIGHT, buff=0.12)
    points[10] = Dot(point_coords[10], color=YELLOW, radius=0.06)
    labels[10] = Text('P10', font_size=20, color=WHITE).next_to(points[10], UP+RIGHT, buff=0.12)
    points[11] = Dot(point_coords[11], color=YELLOW, radius=0.06)
    labels[11] = Text('P11', font_size=20, color=WHITE).next_to(points[11], UP+RIGHT, buff=0.12)
    points[12] = Dot(point_coords[12], color=YELLOW, radius=0.06)
    labels[12] = Text('P12', font_size=20, color=WHITE).next_to(points[12], UP+RIGHT, buff=0.12)
    points[13] = Dot(point_coords[13], color=YELLOW, radius=0.06)
    labels[13] = Text('P13', font_size=20, color=WHITE).next_to(points[13], UP+RIGHT, buff=0.12)
    points[14] = Dot(point_coords[14], color=YELLOW, radius=0.06)
    labels[14] = Text('P14', font_size=20, color=WHITE).next_to(points[14], UP+RIGHT, buff=0.12)
    points[15] = Dot(point_coords[15], color=YELLOW, radius=0.06)
    labels[15] = Text('P15', font_size=20, color=WHITE).next_to(points[15], UP+RIGHT, buff=0.12)
    points[16] = Dot(point_coords[16], color=YELLOW, radius=0.06)
    labels[16] = Text('P16', font_size=20, color=WHITE).next_to(points[16], UP+RIGHT, buff=0.12)
    points[17] = Dot(point_coords[17], color=YELLOW, radius=0.06)
    labels[17] = Text('P17', font_size=20, color=WHITE).next_to(points[17], UP+RIGHT, buff=0.12)
    points[18] = Dot(point_coords[18], color=YELLOW, radius=0.06)
    labels[18] = Text('P18', font_size=20, color=WHITE).next_to(points[18], UP+RIGHT, buff=0.12)
    points[19] = Dot(point_coords[19], color=YELLOW, radius=0.06)
    labels[19] = Text('P19', font_size=20, color=WHITE).next_to(points[19], UP+RIGHT, buff=0.12)
    points[20] = Dot(point_coords[20], color=YELLOW, radius=0.06)
    labels[20] = Text('P20', font_size=20, color=WHITE).next_to(points[20], UP+RIGHT, buff=0.12)
    points[21] = Dot(point_coords[21], color=YELLOW, radius=0.06)
    labels[21] = Text('P21', font_size=20, color=WHITE).next_to(points[21], UP+RIGHT, buff=0.12)
    points[22] = Dot(point_coords[22], color=YELLOW, radius=0.06)
    labels[22] = Text('P22', font_size=20, color=WHITE).next_to(points[22], UP+RIGHT, buff=0.12)
    points[23] = Dot(point_coords[23], color=YELLOW, radius=0.06)
    labels[23] = Text('P23', font_size=20, color=WHITE).next_to(points[23], UP+RIGHT, buff=0.12)
    points[24] = Dot(point_coords[24], color=YELLOW, radius=0.06)
    labels[24] = Text('P24', font_size=20, color=WHITE).next_to(points[24], UP+RIGHT, buff=0.12)
    points[25] = Dot(point_coords[25], color=YELLOW, radius=0.06)
    labels[25] = Text('P25', font_size=20, color=WHITE).next_to(points[25], UP+RIGHT, buff=0.12)
    points[26] = Dot(point_coords[26], color=YELLOW, radius=0.06)
    labels[26] = Text('P26', font_size=20, color=WHITE).next_to(points[26], UP+RIGHT, buff=0.12)
    points[27] = Dot(point_coords[27], color=YELLOW, radius=0.06)
    labels[27] = Text('P27', font_size=20, color=WHITE).next_to(points[27], UP+RIGHT, buff=0.12)
    points[28] = Dot(point_coords[28], color=YELLOW, radius=0.06)
    labels[28] = Text('P28', font_size=20, color=WHITE).next_to(points[28], UP+RIGHT, buff=0.12)
    points[29] = Dot(point_coords[29], color=YELLOW, radius=0.06)
    labels[29] = Text('P29', font_size=20, color=WHITE).next_to(points[29], UP+RIGHT, buff=0.12)
    points[30] = Dot(point_coords[30], color=YELLOW, radius=0.06)
    labels[30] = Text('P30', font_size=20, color=WHITE).next_to(points[30], UP+RIGHT, buff=0.12)

    lines = []
    lines.append(Line(point_coords[0], point_coords[11], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[0], point_coords[14], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[0], point_coords[16], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[0], point_coords[21], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[0], point_coords[25], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[0], point_coords[29], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[5], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[6], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[8], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[10], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[18], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[20], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[11], point_coords[21], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[14], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[14], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[14], point_coords[28], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[14], point_coords[29], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[17], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[21], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[25], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[27], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[16], point_coords[28], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[7], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[13], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[18], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[20], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[21], point_coords[28], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[25], point_coords[17], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[25], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[25], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[25], point_coords[27], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[25], point_coords[28], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[25], point_coords[30], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[29], point_coords[20], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[29], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[29], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[29], point_coords[28], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[1], point_coords[9], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[1], point_coords[17], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[1], point_coords[19], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[1], point_coords[22], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[1], point_coords[23], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[1], point_coords[30], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[9], point_coords[22], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[9], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[17], point_coords[22], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[19], point_coords[18], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[19], point_coords[22], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[19], point_coords[23], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[22], point_coords[18], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[22], point_coords[23], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[22], point_coords[30], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[23], point_coords[5], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[23], point_coords[27], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[23], point_coords[30], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[30], point_coords[27], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[3], point_coords[18], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[18], point_coords[6], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[18], point_coords[10], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[18], point_coords[20], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[18], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[4], point_coords[20], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[20], point_coords[5], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[20], point_coords[12], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[20], point_coords[15], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[20], point_coords[26], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[5], point_coords[6], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[26], point_coords[24], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[26], point_coords[28], color=WHITE, stroke_width=2))
    lines.append(Line(point_coords[24], point_coords[28], color=WHITE, stroke_width=2))

    circles = []

    return {
        'points': points,
        'labels': labels,
        'lines': lines,
        'circles': circles,
        'point_coords': point_coords
    }


class GeometryScene(Scene):
    """
    Main scene class that can be run directly.
    Run with: manim -pql geometry_scene.py GeometryScene
    """
    
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
"""
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
"""
