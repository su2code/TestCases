#!/usr/bin/env python3
"""wedge.py <out.su2> <angle deg> <ncirc> <nsect> <nr> <nz> [r0]
3D pipe (radius 1, length 2, axis = z) made of nsect sectors of <angle> degrees with ncirc cells each in the
circumferential direction. If nsect * angle = 360 the mesh is the full pipe (no periodic markers), otherwise the
markers per1 (theta = 0) and per2 (theta = nsect * angle) are written.
r0 = 0 (default): the mesh contains the axis (prisms at the axis, the axis nodes lie on both periodic markers);
r0 > 0: annular mesh without axis nodes (marker hub at r = r0).
Markers: per1, per2, inlet (z = 0), outlet (z = 2), wall (r = 1) [, hub].
Also writes <out.su2>.map with one line per node: node, j (circumferential index), i (radial index), k (axial
index); axis nodes have j = 0, i = 0. Nodes with the same (j, i, k) are the same node in a sector and in the full pipe."""

import math
import sys

output = sys.argv[1]
sector_angle = float(sys.argv[2])
circumferential_cells_per_sector = int(sys.argv[3])
sectors = int(sys.argv[4])
radial_cells = int(sys.argv[5])
axial_cells = int(sys.argv[6])
inner_radius = float(sys.argv[7]) if len(sys.argv) > 7 else 0.0
radius, length = 1.0, 2.0
circumferential_cells = circumferential_cells_per_sector * sectors
full_pipe = abs(sectors * sector_angle - 360.0) < 1e-9
includes_axis = inner_radius == 0.0
points, node_indices = [], []


def add_point(x, y, z, j, i, k):
    points.append((x, y, z))
    node_indices.append((j, i, k))
    return len(points) - 1


# All circumferential node lines share a single axial line at r = 0.
axis_nodes = []
if includes_axis:
    axis_nodes = [add_point(0.0, 0.0, length * k / axial_cells, 0, 0, k)
                  for k in range(axial_cells + 1)]
first_radial_index = 1 if includes_axis else 0
circumferential_node_lines = circumferential_cells if full_pipe else circumferential_cells + 1
node_ids = [[[None] * (axial_cells + 1) for _ in range(radial_cells + 1)]
            for _ in range(circumferential_node_lines)]
for j in range(circumferential_node_lines):
    theta = math.radians(sector_angle) * j / circumferential_cells_per_sector
    for i in range(first_radial_index, radial_cells + 1):
        r = inner_radius + (radius - inner_radius) * i / radial_cells
        for k in range(axial_cells + 1):
            node_ids[j][i][k] = add_point(r * math.cos(theta), r * math.sin(theta),
                                        length * k / axial_cells, j, i, k)

elements = []
markers = {"per1": [], "per2": [], "inlet": [], "outlet": [], "wall": []}
if full_pipe:
    del markers["per1"], markers["per2"]
if not includes_axis:
    markers["hub"] = []

# SU2 element types: triangle = 5, quadrilateral = 9, hexahedron = 12, prism = 13.
for k in range(axial_cells):
    for j in range(circumferential_cells):
        # Wrap the last node line onto the first one only for the full pipe.
        left = node_ids[j]
        right = node_ids[(j + 1) % circumferential_node_lines]
        if includes_axis:
            elements.append((13, axis_nodes[k], left[1][k], right[1][k],
                             axis_nodes[k + 1], left[1][k + 1], right[1][k + 1]))
        else:
            markers["hub"].append((9, left[0][k], right[0][k], right[0][k + 1], left[0][k + 1]))
        for i in range(first_radial_index, radial_cells):
            elements.append((12, left[i][k], left[i + 1][k], right[i + 1][k], right[i][k],
                             left[i][k + 1], left[i + 1][k + 1], right[i + 1][k + 1], right[i][k + 1]))
        markers["wall"].append((9, left[radial_cells][k], right[radial_cells][k],
                                right[radial_cells][k + 1], left[radial_cells][k + 1]))
    if not full_pipe:
        for j, marker in ((0, "per1"), (circumferential_cells, "per2")):
            nodes = node_ids[j]
            if includes_axis:
                markers[marker].append((9, axis_nodes[k], nodes[1][k], nodes[1][k + 1], axis_nodes[k + 1]))
            for i in range(first_radial_index, radial_cells):
                markers[marker].append((9, nodes[i][k], nodes[i + 1][k], nodes[i + 1][k + 1], nodes[i][k + 1]))

for k, marker in ((0, "inlet"), (axial_cells, "outlet")):
    for j in range(circumferential_cells):
        left = node_ids[j]
        right = node_ids[(j + 1) % circumferential_node_lines]
        if includes_axis:
            markers[marker].append((5, axis_nodes[k], left[1][k], right[1][k]))
        for i in range(first_radial_index, radial_cells):
            markers[marker].append((9, left[i][k], left[i + 1][k], right[i + 1][k], right[i][k]))

with open(output, "w") as mesh_file:
    mesh_file.write("NDIME= 3\nNELEM= %d\n" % len(elements))
    for element_id, element in enumerate(elements):
        mesh_file.write(" ".join(map(str, element)) + " %d\n" % element_id)
    mesh_file.write("NPOIN= %d\n" % len(points))
    for node_id, (x, y, z) in enumerate(points):
        mesh_file.write("%.17g %.17g %.17g %d\n" % (x, y, z, node_id))
    mesh_file.write("NMARK= %d\n" % len(markers))
    for marker, faces in markers.items():
        mesh_file.write("MARKER_TAG= %s\nMARKER_ELEMS= %d\n" % (marker, len(faces)))
        for face in faces:
            mesh_file.write(" ".join(map(str, face)) + "\n")

with open(output + ".map", "w") as map_file:
    for node_id, indices in enumerate(node_indices):
        map_file.write("%d %d %d %d\n" % ((node_id,) + indices))

print(output, "points", len(points), "elements", len(elements), "axis nodes", len(axis_nodes),
      "full" if full_pipe else "sector")
