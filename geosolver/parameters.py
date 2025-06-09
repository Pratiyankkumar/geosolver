from collections import namedtuple
import numpy as np

__author__ = 'minjoon'

"""
eps is used to segment the line.
It shouldn't be too big; otherwise, off-line will be matched.
"""
HoughLineParameters = namedtuple("HoughLineParameters",
                                 "rho theta threshold max_gap min_length nms_rho nms_theta max_num eps")

hough_line_parameters = HoughLineParameters(rho=1,
                                            theta=np.pi/180,
                                            threshold=30,
                                            max_gap=3,
                                            min_length=20,
                                            nms_rho=2,
                                            nms_theta=np.pi/60,
                                            max_num=40,
                                            eps=2)

HoughCircleParameters = namedtuple("HoughCircleParameters",
                                   "dp minRadius maxRadius param1 param2 minDist max_gap min_length max_num")

hough_circle_parameters = HoughCircleParameters(dp=1,
                                                minRadius=20,
                                                maxRadius=200,
                                                param1=50, #50
                                                param2=30, #30
                                                minDist=2,
                                                max_gap=100,
                                                min_length=20,
                                                max_num=50)

# Enhanced circle detection parameters
class EnhancedCircleParams:
    # Contour-based detection
    min_contour_points = 20
    max_contour_points = 1000
    min_circularity = 0.5
    min_coverage_ratio = 0.3
    max_radius_deviation = 0.15
    
    # Template matching
    template_scales = [0.5, 0.7, 1.0, 1.3, 1.5, 2.0]
    template_confidence_threshold = 0.6
    
    # Circle size constraints
    min_circle_radius = 10
    max_circle_radius = 300
    
    # Duplicate removal
    duplicate_center_threshold = 20
    duplicate_radius_threshold = 10

# Arc detection parameters
class ArcDetectionParams:
    min_arc_points = 15
    max_gap_in_arc = 5
    angle_tolerance = 0.1  # radians
    
    # Arc classification thresholds (in degrees)
    semicircle_min = 170
    semicircle_max = 190
    quarter_circle_min = 80
    quarter_circle_max = 100
    min_arc_span = 30

# These eps determine pixel coverage of each primitive.
LINE_EPS = 3
CIRCLE_EPS = 6
PRIMITIVE_SELECTION_MIN_GAIN = 0

INTERSECTION_EPS = 2
KMEANS_RADIUS_THRESHOLD = 15


ENHANCED_CIRCLE_DETECTION = True
USE_CONTOUR_DETECTION = True
USE_TEMPLATE_MATCHING = True
ENABLE_PARTIAL_CIRCLES = True