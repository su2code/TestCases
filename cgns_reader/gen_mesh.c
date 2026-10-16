/* Writes mesh_channel_sections.cgns, the mesh of the test cgns_reader/channel_sections.cfg.
 * Build with the CGNS library of SU2, e.g. from the build folder of SU2:
 *   mpicc gen_mesh.c -I<SU2>/externals/cgns -Iexternals/cgns externals/cgns/libcgns.a externals/cgns/hdf5/libsu2hdf5.a -lz -lm -ldl
 */
/* Small 3D channel with hexahedra (x < 1) and prisms (x > 1), written as a mesher would:
 * the boundaries are split in sections by element type or by block, and the ZoneBC groups them.
 *   inlet               : no BC covers it        -> marker named after the section ("inlet")
 *   upper_side          : BC "upper", no family  -> marker named after the BC ("upper")
 *   lower_1, lower_2    : BC "lower_wall", family "lower"  -> one marker "lower"
 *   quad_back, tri_back : BC "back", family "back"         -> one marker "back"
 *   quad_front,tri_front: BC "front", family "front"       -> one marker "front"
 *   outlet              : BC "outlet", family "outlet"     -> marker "outlet"
 */
#include <stdio.h>
#include <stdlib.h>
#include "cgnslib.h"

#define NI 9
#define NJ 5
#define NK 3
#define NH 4 /* hexahedra for i < NH, prisms after */

static cgsize_t n(int i, int j, int k) { return 1 + i + NI * (j + NJ * k); }

#define CHK(x) if (x) { printf("%s\n", cg_get_error()); exit(1); }

int fn, B, Z, S;
cgsize_t next = 1;
cgsize_t conn[4096];

static cgsize_t section(const char* name, CGNS_ENUMT(ElementType_t) type, int ne) {
  cgsize_t first = next;
  CHK(cg_section_write(fn, B, Z, name, type, first, first + ne - 1, 0, conn, &S));
  next += ne;
  return first;
}

static void bc(const char* name, const char* family, CGNS_ENUMT(BCType_t) type, cgsize_t first, cgsize_t last) {
  int bc;
  cgsize_t range[2] = {first, last};
  CHK(cg_boco_write(fn, B, Z, name, type, CGNS_ENUMV(PointRange), 2, range, &bc));
  CHK(cg_boco_gridlocation_write(fn, B, Z, bc, CGNS_ENUMV(FaceCenter)));
  if (family) {
    CHK(cg_goto(fn, B, "Zone_t", Z, "ZoneBC_t", 1, "BC_t", bc, "end"));
    CHK(cg_famname_write(family));
  }
}

int main(int argc, char** argv) {
  const char* file = argc > 1 ? argv[1] : "mesh_channel_sections.cgns";
  double x[NI * NJ * NK], y[NI * NJ * NK], z[NI * NJ * NK];
  for (int k = 0; k < NK; k++)
    for (int j = 0; j < NJ; j++)
      for (int i = 0; i < NI; i++) {
        x[n(i, j, k) - 1] = 0.25 * i;
        y[n(i, j, k) - 1] = 0.25 * j;
        z[n(i, j, k) - 1] = 0.125 * k;
      }

  const int nHex = NH * (NJ - 1) * (NK - 1), nPrism = 2 * (NI - 1 - NH) * (NJ - 1) * (NK - 1);
  cgsize_t size[3] = {NI * NJ * NK, nHex + nPrism, 0};
  int C;

  CHK(cg_open(file, CG_MODE_WRITE, &fn));
  CHK(cg_base_write(fn, "Base", 3, 3, &B));
  CHK(cg_zone_write(fn, B, "Channel", size, CGNS_ENUMV(Unstructured), &Z));
  CHK(cg_coord_write(fn, B, Z, CGNS_ENUMV(RealDouble), "CoordinateX", x, &C));
  CHK(cg_coord_write(fn, B, Z, CGNS_ENUMV(RealDouble), "CoordinateY", y, &C));
  CHK(cg_coord_write(fn, B, Z, CGNS_ENUMV(RealDouble), "CoordinateZ", z, &C));

  const char* fams[] = {"lower", "back", "front", "outlet"};
  for (int f = 0; f < 4; f++) {
    int F;
    CHK(cg_family_write(fn, B, fams[f], &F));
  }

  int m;

  /*--- Volume sections. ---*/
  m = 0;
  for (int k = 0; k < NK - 1; k++)
    for (int j = 0; j < NJ - 1; j++)
      for (int i = 0; i < NH; i++) {
        cgsize_t h[8] = {n(i, j, k),     n(i + 1, j, k),     n(i + 1, j + 1, k),     n(i, j + 1, k),
                         n(i, j, k + 1), n(i + 1, j, k + 1), n(i + 1, j + 1, k + 1), n(i, j + 1, k + 1)};
        for (int a = 0; a < 8; a++) conn[m++] = h[a];
      }
  section("HexElements", CGNS_ENUMV(HEXA_8), nHex);

  m = 0;
  for (int k = 0; k < NK - 1; k++)
    for (int j = 0; j < NJ - 1; j++)
      for (int i = NH; i < NI - 1; i++) {
        cgsize_t p[12] = {n(i, j, k),     n(i + 1, j, k),     n(i + 1, j + 1, k),
                          n(i, j, k + 1), n(i + 1, j, k + 1), n(i + 1, j + 1, k + 1),
                          n(i, j, k),     n(i + 1, j + 1, k), n(i, j + 1, k),
                          n(i, j, k + 1), n(i + 1, j + 1, k + 1), n(i, j + 1, k + 1)};
        for (int a = 0; a < 12; a++) conn[m++] = p[a];
      }
  section("PrismElements", CGNS_ENUMV(PENTA_6), nPrism);

  /*--- Boundary sections, the ones of one BC are next to each other. ---*/
  cgsize_t first, mid;

  m = 0;
  for (int k = 0; k < NK - 1; k++)
    for (int j = 0; j < NJ - 1; j++) {
      cgsize_t q[4] = {n(0, j, k), n(0, j, k + 1), n(0, j + 1, k + 1), n(0, j + 1, k)};
      for (int a = 0; a < 4; a++) conn[m++] = q[a];
    }
  section("inlet", CGNS_ENUMV(QUAD_4), m / 4);

  m = 0;
  for (int k = 0; k < NK - 1; k++)
    for (int j = 0; j < NJ - 1; j++) {
      cgsize_t q[4] = {n(NI - 1, j, k), n(NI - 1, j + 1, k), n(NI - 1, j + 1, k + 1), n(NI - 1, j, k + 1)};
      for (int a = 0; a < 4; a++) conn[m++] = q[a];
    }
  first = section("outlet", CGNS_ENUMV(QUAD_4), m / 4);
  bc("outlet", "outlet", CGNS_ENUMV(BCOutflow), first, next - 1);

  for (int part = 0; part < 2; part++) {
    m = 0;
    for (int k = 0; k < NK - 1; k++)
      for (int i = part ? NH : 0; i < (part ? NI - 1 : NH); i++) {
        cgsize_t q[4] = {n(i, 0, k), n(i + 1, 0, k), n(i + 1, 0, k + 1), n(i, 0, k + 1)};
        for (int a = 0; a < 4; a++) conn[m++] = q[a];
      }
    mid = section(part ? "lower_2" : "lower_1", CGNS_ENUMV(QUAD_4), m / 4);
    if (!part) first = mid;
  }
  bc("lower_wall", "lower", CGNS_ENUMV(BCWallInviscid), first, next - 1);

  m = 0;
  for (int k = 0; k < NK - 1; k++)
    for (int i = 0; i < NI - 1; i++) {
      cgsize_t q[4] = {n(i, NJ - 1, k), n(i, NJ - 1, k + 1), n(i + 1, NJ - 1, k + 1), n(i + 1, NJ - 1, k)};
      for (int a = 0; a < 4; a++) conn[m++] = q[a];
    }
  first = section("upper_side", CGNS_ENUMV(QUAD_4), m / 4);
  bc("upper", NULL, CGNS_ENUMV(BCWallInviscid), first, next - 1);

  for (int side = 0; side < 2; side++) {
    const int k = side ? NK - 1 : 0;
    m = 0;
    for (int j = 0; j < NJ - 1; j++)
      for (int i = 0; i < NH; i++) {
        cgsize_t q[4] = {n(i, j, k), n(i + 1, j, k), n(i + 1, j + 1, k), n(i, j + 1, k)};
        for (int a = 0; a < 4; a++) conn[m++] = q[a];
      }
    first = section(side ? "quad_front" : "quad_back", CGNS_ENUMV(QUAD_4), m / 4);
    m = 0;
    for (int j = 0; j < NJ - 1; j++)
      for (int i = NH; i < NI - 1; i++) {
        cgsize_t t[6] = {n(i, j, k), n(i + 1, j, k), n(i + 1, j + 1, k), n(i, j, k), n(i + 1, j + 1, k), n(i, j + 1, k)};
        for (int a = 0; a < 6; a++) conn[m++] = t[a];
      }
    section(side ? "tri_front" : "tri_back", CGNS_ENUMV(TRI_3), m / 3);
    bc(side ? "front" : "back", side ? "front" : "back", CGNS_ENUMV(BCSymmetryPlane), first, next - 1);
  }

  CHK(cg_close(fn));
  printf("Wrote %s: %d hexahedra, %d prisms, %ld elements.\n", file, nHex, nPrism, (long)(next - 1));
  return 0;
}
