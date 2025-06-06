import os
import cv2
import traceback

from geosolver import geoserver_interface
from geosolver.diagram.computational_geometry import normalize_angle, horizontal_angle, area_of_polygon
from geosolver.diagram.get_instances import get_all_instances
from geosolver.diagram.parse_confident_formulas import parse_confident_formulas
from geosolver.diagram.parse_core import parse_core
from geosolver.diagram.parse_graph import parse_graph
from geosolver.diagram.parse_image_segments import parse_image_segments
from geosolver.diagram.parse_primitives import parse_primitives
from geosolver.diagram.select_primitives import select_primitives
from geosolver.utils.prep import open_image
import numpy as np

__author__ = 'minjoon'

def test_local_diagram_step_by_step():
    """Test with local diagram image - step by step to isolate the error"""
    image_path = "geosolver/images/diagram.png"
    print(f"Processing image: {image_path}")
    
    try:
        print("Step 1: Opening image...")
        image = open_image(image_path)
        print(f"Image shape: {image.shape}")
        
        print("Step 2: Parsing image segments...")
        image_segment_parse = parse_image_segments(image)
        print("Image segments parsed successfully")
        
        print("Step 3: Parsing primitives...")
        primitive_parse = parse_primitives(image_segment_parse)
        print("Primitives parsed successfully")
        
        print("Step 4: Selecting primitives...")
        selected = select_primitives(primitive_parse)
        print("Primitives selected successfully")
        
        print("Step 5: Parsing core...")
        core_parse = parse_core(selected)
        print("Core parsed successfully")
        
        print("Step 6: Displaying points...")
        core_parse.display_points()
        print("Points displayed successfully")
        
        print("Step 7: Parsing graph...")
        graph_parse = parse_graph(core_parse)
        print("Graph parsed successfully")
        
        print("Step 8: Getting confident formulas...")
        confident_formulas = parse_confident_formulas(graph_parse)
        print("Confident information in the diagram:")
        for variable_node in confident_formulas:
            print(variable_node)
            
    except Exception as e:
        print(f"Error at step: {e}")
        print("Full traceback:")
        traceback.print_exc()

def test_just_image_segments():
    """Test just the image segmentation step"""
    image_path = "geosolver/images/diagram.png"
    print(f"Testing just image segments for: {image_path}")
    
    try:
        image = open_image(image_path)
        print(f"Image loaded successfully, shape: {image.shape}")
        
        image_segment_parse = parse_image_segments(image)
        print("Image segments parsed successfully")
        print(f"Number of label segments: {len(image_segment_parse.label_image_segments)}")
        
        # Try to display the segmented image
        image_segment_parse.diagram_image_segment.display_binarized_segmented_image()
        
    except Exception as e:
        print(f"Error in image segmentation: {e}")
        traceback.print_exc()

def test_just_primitives():
    """Test just up to primitives parsing"""
    image_path = "geosolver/images/diagram.png"
    print(f"Testing primitives parsing for: {image_path}")
    
    try:
        image = open_image(image_path)
        image_segment_parse = parse_image_segments(image)
        print("Image segments OK")
        
        primitive_parse = parse_primitives(image_segment_parse)
        print("Primitives parsed successfully")
        
        primitive_parse.display_primitives()
        
    except Exception as e:
        print(f"Error in primitives parsing: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Testing just image segments ===")
    test_just_image_segments()
    
    print("\n=== Testing up to primitives ===")
    test_just_primitives()
    
    # Uncomment this if the primitives test passes
    print("\n=== Testing step by step ===")
    test_local_diagram_step_by_step()