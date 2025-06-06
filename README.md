# geosolver

NOTE: SOME SECTIONS OF THIS README FILE ARE OUT OF DATE! I WILL UPDATE IT AS SOON AS POSSIBLE. THANK YOU!

geosolver is an end-to-end system that solves high school geometry questions.
That is, its input is question text in natural language and diagram in raster graphics,
and its output is the answer to the question.

geosolver is divided into four core parts: diagram praser, text parser, joint parser, and solver.
Text parser transforms the text in natural language into a logical form.
Diagram parser extracts information from the diagram.
Joint parser combines the results of the text parser and the diagram parser and outputs the final logical form.
Solver accepts the logical form from the joint parser and outputs the answer.
This tutorial will first walkthrough each part independently (the modules except the joint parser can be used independently),
and in the last section it will show how to connect them for an end-to-end system.

## Diagram parser

Location: `geosolver.diagram`

Diagram parsing consists of five finer steps: image segment parsing, primitive paring, primitive selecting, core parsing, and graph parsing. We will explain each of them in detail below. You can also refer to `geosolver.diagram.run_diagram` module to see full examples corresponding to these.

### Parsing image segments

Image segment parsing is the task of obtaining the diagram segment (and label segments) from the original image.
For instance, given an original image

![original image]
(https://github.com/seominjoon/geosolver/blob/master/images/original.png)

we obtain the diagram segment

![diagram segment]
(https://github.com/seominjoon/geosolver/blob/master/images/diagram.png)

To do so, obtain a `Question` object (`question`) as shown above and run the following:

```python
from geosolver.diagram.parse_image_segments import parse_image_segments

image_segment_parse = parse_image_segments(open_image(question.diagram_path))
image_segment_parse.diagram_image_segment.display_binarized_segmented_image()
for idx, label_image_segment in image_segment_parse.label_image_segments.iteritems():
  label_image_segment.display_segmented_image()
```

This is equivalent to `geosolver.diagram.run_diagram.test_parse_image_segments`.

### Parsing primitives from the diagram segment

Primitive parsing is the task of obtaining over-gernerated, noisy primitives from the diagram segment.
For instance, given the diagram segment above, we want to obtain

![primitive parse]
(https://github.com/seominjoon/geosolver/blob/master/images/primitives.png)

To do so:

```python
from geosolver.diagram.parse_primitives import parse_primitives

primitive_parse = parse_primitives(image_segment_parse)
primitive_parse.display_primitives()
```

This is equivalent to `geosolver.diagram.run_diagram.test_parse_primitives`.

### Selecting primitives

We want to select a subset of the over-generated primitives that accurately represents the diagram:

![selected primitives]
(https://github.com/seominjoon/geosolver/blob/master/images/selected.png)

To do so:

```python
from geosolver.diagram.select_primitives import select_primitives

selected = select_primitives(primitive_parse)
selected.display_primitives()
```

This is equivalent to `geosolver.diagram.run_diagram.test_select_primitives`.

### Parsing core

_CoreParse_ consists of the critical (intersection) points and the circles in the diagram.
It can be thought as the post-processed parse of the selected primitive parse.
By parsing the core, we obtain:

![core]
(https://github.com/seominjoon/geosolver/blob/master/images/core.png)

in which the blue dots are the intersection points.

To do so:

```python
from geosolver.diagram.parse_core import parse_core

core_parse = parse_core(selected)
core_parse.display_points()
```

This is equivalent to `geosolver.diagram.run_diagram.test_parse_core`.

### Parsing graph

_GraphParse_ contains high level information such as whether a line exists between two points, etc.
To obtain the graph parse, run:

```python
from geosolver.diagram.parse_graph import parse_graph
from geosolver.diagram.get_instances import get_all_instances

graph_parse = parse_graph(diagram_parse)
lines = get_all_instances(graph_parse, 'line')
circles = get_all_instances(graph_parse, 'circle')
arcs = get_all_instances(graph_parse, 'arc')
angles = get_all_instances(graph_parse, 'angle')
print("Displaying lines...")
for key, line in lines.iteritems():
  graph_parse.display_instances([line])
print("Displaying circles...")
for key, circle in circles.iteritems():
  graph_parse.display_instances([circle])
print("Displaying arcs...")
for key, arc in arcs.iteritems():
  graph_parse.display_instances([arc])
print("Displaying angles...")
for key, angle in angles.iteritems():
  graph_parse.display_instances([angle])
```

This is equivalent to `geosolver.diagram.run_diagram.test_parse_graph`.

## Installation

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

Run the following command from the **root directory** of the project:

```bash
python -m geosolver.diagram.run_diagram
```

## Testing Images

There are sample testing images available in the `geosolver/images` directory.

To change the input image, open the `geosolver/diagram/run_diagram.py` file and update the image filename as needed.
