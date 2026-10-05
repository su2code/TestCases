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
import sys, math
out, deg, ncirc, nsect, nr, nz = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
r0 = float(sys.argv[7]) if len(sys.argv) > 7 else 0.0
R, Lz = 1.0, 2.0
M = ncirc * nsect                      # cells in the circumferential direction
full = abs(nsect * deg - 360.0) < 1e-9
axis = r0 == 0.0
X, ijk = [], []
def add(x, y, z, j, i, k): X.append((x, y, z)); ijk.append((j, i, k)); return len(X) - 1
A = [add(0.0, 0.0, Lz*k/nz, 0, 0, k) for k in range(nz+1)] if axis else None
i0 = 1 if axis else 0
nj = M if full else M + 1              # node lines in the circumferential direction
P = [[[None]*(nz+1) for _ in range(nr+1)] for _ in range(nj)]
for j in range(nj):
    th = math.radians(deg) * j / ncirc
    for i in range(i0, nr+1):
        r = r0 + (R-r0)*i/nr
        for k in range(nz+1): P[j][i][k] = add(r*math.cos(th), r*math.sin(th), Lz*k/nz, j, i, k)
E, Mk = [], {"per1": [], "per2": [], "inlet": [], "outlet": [], "wall": []}
if full: del Mk["per1"], Mk["per2"]
if not axis: Mk["hub"] = []
for k in range(nz):
    for j in range(M):
        a, b = P[j], P[(j+1) % nj]
        if axis: E.append((13, A[k], a[1][k], b[1][k], A[k+1], a[1][k+1], b[1][k+1]))
        else: Mk["hub"].append((9, a[0][k], b[0][k], b[0][k+1], a[0][k+1]))
        for i in range(i0, nr):
            E.append((12, a[i][k], a[i+1][k], b[i+1][k], b[i][k], a[i][k+1], a[i+1][k+1], b[i+1][k+1], b[i][k+1]))
        Mk["wall"].append((9, a[nr][k], b[nr][k], b[nr][k+1], a[nr][k+1]))
    if not full:
        for j, m in ((0, "per1"), (M, "per2")):
            if axis: Mk[m].append((9, A[k], P[j][1][k], P[j][1][k+1], A[k+1]))
            for i in range(i0, nr): Mk[m].append((9, P[j][i][k], P[j][i+1][k], P[j][i+1][k+1], P[j][i][k+1]))
for k, m in ((0, "inlet"), (nz, "outlet")):
    for j in range(M):
        a, b = P[j], P[(j+1) % nj]
        if axis: Mk[m].append((5, A[k], a[1][k], b[1][k]))
        for i in range(i0, nr): Mk[m].append((9, a[i][k], a[i+1][k], b[i+1][k], b[i][k]))
L = ["NDIME= 3", "NELEM= %d" % len(E)] + [" ".join(map(str, e)) + " %d" % n for n, e in enumerate(E)]
L += ["NPOIN= %d" % len(X)] + ["%.17g %.17g %.17g %d" % (x[0], x[1], x[2], n) for n, x in enumerate(X)]
L += ["NMARK= %d" % len(Mk)]
for m, f in Mk.items(): L += ["MARKER_TAG= " + m, "MARKER_ELEMS= %d" % len(f)] + [" ".join(map(str, e)) for e in f]
open(out, "w").write("\n".join(L) + "\n")
open(out + ".map", "w").write("\n".join("%d %d %d %d" % ((n,) + t) for n, t in enumerate(ijk)) + "\n")
print(out, "points", len(X), "elements", len(E), "axis nodes", len(A) if axis else 0, "full" if full else "sector")
