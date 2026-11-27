#!/usr/bin/env python3
"""Inlet profile of the Morse swirling jet at x/D = 0.5 for the SU2 wedge mesh.

Fills the template that SU2 writes (example_inlet_jet.dat) with the measured axial, radial and swirl velocity of
station 1 (morse1.dat: r/x, r/r05, U/Ucl, V/Ucl, W/Wmax, ...), converted to Cartesian components on the wedge
face. The eddy viscosity follows from the measured shear stress, nu_t = -u'v' / (dU/dr), and nu_tilde from
nu_t = nu_tilde f_v1.
"""

import numpy as np

DATA = "morse1.dat"
TEMPLATE = "example_inlet_jet.dat"
OUTPUT = "inlet_jet.dat"
DIAMETER = 0.0246  # m
X_OVER_D = 0.5  # station of the profile
U_CL = 34.10  # centreline velocity at the station, m/s
W_MAX = 16.50  # maximum swirl velocity at the station, m/s
NU = 1.82e-5 / 1.2  # kinematic viscosity, m^2/s
STRAIN_FRACTION = 0.1  # u'v' is used where |dU/dr| exceeds this fraction of its maximum


def nu_tilde_from_nu_t(nu_t):
    """Invert nu_t = nu_tilde chi^3 / (chi^3 + 7.1^3) for nu_tilde by Newton iteration on chi."""
    target = nu_t / NU
    chi = np.maximum(target, 1.0)
    for _ in range(50):
        f = chi**4 / (chi**3 + 7.1**3) - target
        df = (chi**6 + 4 * 7.1**3 * chi**3) / (chi**3 + 7.1**3) ** 2
        chi = np.maximum(chi - f / df, 1e-6)
    return chi * NU


data = np.loadtxt(DATA, comments="#")
r_data = data[:, 0] * X_OVER_D * DIAMETER
U_data, V_data, W_data = data[:, 2] * U_CL, data[:, 3] * U_CL, data[:, 4] * W_MAX
uv_data = data[:, 8] * U_CL**2

with open(TEMPLATE) as f:
    lines = f.read().splitlines()
is_row = [l[:1].isdigit() or l[:1] == "-" for l in lines]
head = [l for l, row in zip(lines, is_row) if not row]
rows = np.array([[float(v) for v in l.split()] for l, row in zip(lines, is_row) if row])
r, th = np.hypot(rows[:, 1], rows[:, 2]), np.arctan2(rows[:, 2], rows[:, 1])

U = np.interp(r, r_data, U_data)
V = np.interp(r, r_data, V_data)
W = np.interp(r, r_data, W_data)
vel = np.column_stack([U, V * np.cos(th) - W * np.sin(th), V * np.sin(th) + W * np.cos(th)])
mag = np.linalg.norm(vel, axis=1)
rows[:, 4] = mag
rows[:, 5:8] = vel / mag[:, None]

# nu_t = -u'v' / (dU/dr) where the shear is large, dV/dx neglected; held at the nearest value elsewhere.
dU_dr = np.gradient(U_data, r_data)
sheared = np.abs(dU_dr) >= STRAIN_FRACTION * np.abs(dU_dr).max()
nu_t = np.maximum(np.interp(r, r_data[sheared], -uv_data[sheared] / dU_dr[sheared]), NU)
rows[:, 8] = nu_tilde_from_nu_t(nu_t)

with open(OUTPUT, "w") as f:
    f.write("\n".join(head) + "\n")
    for row in rows:
        f.write("\t".join(f"{v:.15e}" for v in row) + "\n")
print(f"{OUTPUT}: {len(rows)} points, |U| in [{mag.min():.2f}, {mag.max():.2f}] m/s, "
      f"nu_t/nu in [{nu_t.min() / NU:.1f}, {nu_t.max() / NU:.1f}]")
