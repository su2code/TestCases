N=0.00002;
dy=5e-5;
//+
Point(1) = {0, 0, 0, N};
Point(2) = {0.01, 0, 0, 0.2*N};
Point(3) = {0.01, dy, 0, 0.2*N};
Point(4) = {0.0, dy, 0, N};
Point(9) = {0.0100+dy, 2*dy, 0, N};
Point(10) = {0.010, 2*dy, 0, N};
Point(11) = {0.0100+dy, 9*dy, 0, N};
Point(13) = {0.0100+8*dy, 0.00, 0, N};
Point(14) = {0.0100+8*dy, 2*dy, 0, N};
//+
Line(1) = {1, 4};
Line(2) = {4, 3};
Line(3) = {3, 2};
Line(4) = {2, 1};
Line(6) = {9, 11};
Line(10) = {13, 14};
Line(11) = {2, 13};
//+
Circle(5) = {3, 10, 9};
Circle(9) = {14, 9, 11};
//+
Transfinite Curve {3, 1} = 2 Using Progression 1;
Transfinite Curve {4, 2} = 1000 Using Progression 1;
//+
//+
Physical Curve("inlet", 12) = {1};
Physical Curve("symmetry_bottom", 13) = {4, 11};
Physical Curve("outlet", 14) = {9, 10};
Physical Curve("wall", 15) = {6, 5, 2};
//+
Curve Loop(1) = {2, 3, 4, 1};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {6, -9, -10, -11, -3, 5};
//+
Plane Surface(2) = {2};
//+
Transfinite Surface {1};
//+
Physical Surface("interior", 16) = {1, 2};
//+
Recombine Surface {1, 2};
