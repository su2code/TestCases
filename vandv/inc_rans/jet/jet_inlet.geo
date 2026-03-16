// axisymmetric round jet, to reproduce the results of 
// Wygnanski & Fiedler or Hussein
// diameter = 1 inch
D = 0.0254;
R = 0.5*D;

N = 200*D;
H = 50*D;
L = 30*D;
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {0, R, 0, 1.0};
// 
Point(3) = {0, H, 0, 1.0};
//+
Point(4) = {N, H, 0, 1.0};
//+
Point(5) = {N, 8*R, 0, 1.0};
//+
Point(6) = {N, 0.0, 0, 1.0};
//+
Point(7) = {-L, 0, 0, 1.0};
//+
Point(8) = {-L, R, 0, 1.0};
//+ thickness of the nozzle
Point(9) = {0, 1.1*D, 0, 1.0};
//+
Line(1) = {1, 6};
//+
Line(2) = {6, 5};
//+
Line(3) = {5, 4};
//+
Line(4) = {3, 4};
//+
Line(5) = {2, 9};
Line(11) = {9, 3};
//+
Line(6) = {2, 1};
//+
Line(7) = {2, 5};
//+
Line(8) = {7, 1};
//+
Line(9) = {2, 8};
//+
Line(10) = {8, 7};
//+
Curve Loop(1) = {1, 2, -7, 6};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {-4, -11, -5, 7, 3};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {8, -6, 9, 10};
//+
Plane Surface(3) = {3};
//+ COARSE
//Transfinite Curve {1} = 400 Using Progression 1.006;
//Transfinite Curve {4} = 400 Using Progression 1.006;
//Transfinite Curve {7} = 400 Using Progression 1.006;
//+
//Transfinite Curve {5} = 11 Using Progression 1.06;
//Transfinite Curve {11} = 40 Using Progression 1.10;

//Transfinite Curve {3} = 50 Using Progression 1.00;

//Transfinite Curve {6} = 20 Using Progression 1.20;
//Transfinite Curve {10} = 20 Using Progression 1.20;
//Transfinite Curve {2} = 20 Using Progression 1;
//Transfinite Curve {9, 8} = 300 Using Bump 0.5;
//
//
//
//+ MEDIUM
Transfinite Curve {1} = 600 Using Progression 1.004;
Transfinite Curve {4} = 600 Using Progression 1.004;
Transfinite Curve {7} = 600 Using Progression 1.004;
Transfinite Curve {5} = 21 Using Progression 1.06;
Transfinite Curve {11} = 60 Using Progression 1.08;
Transfinite Curve {3} = 80 Using Progression 1.00;
Transfinite Curve {6} = 30 Using Progression 1.15;
Transfinite Curve {2} = 30 Using Progression 1;
Transfinite Curve {10} = 30 Using Progression 1.15;
Transfinite Curve {9, 8} = 500 Using Bump 0.5;
//
//+ FINE
//Transfinite Curve {1} = 1000 Using Progression 1.0045;
//Transfinite Curve {4} = 1000 Using Progression 1.0045;
//Transfinite Curve {7} = 1000 Using Progression 1.0045;
//+
//Transfinite Curve {5} = 31 Using Progression 1.08;
//Transfinite Curve {11} = 90 Using Progression 1.07;
//Transfinite Curve {3} = 120 Using Progression 1.00;

//Transfinite Curve {6} = 45 Using Progression 1.15;
//Transfinite Curve {2} = 45 Using Progression 1;
//Transfinite Curve {10} = 45 Using Progression 1.15;
//Transfinite Curve {9, 8} = 700 Using Bump 0.5;
//+
Transfinite Surface {3};
Transfinite Surface {2}={5,4,3,2};
Transfinite Surface {1};
//+
Recombine Surface {3, 2, 1};
//+
Physical Curve("inlet_coflow", 9) = {11};
Physical Curve("freestream", 11) = {4};
Physical Curve("outlet", 12) = {2, 3};
Physical Curve("inlet_jet", 8) = {10};
Physical Curve("wall", 14) = {9};
Physical Curve("wall_edge", 15) = {5};
Physical Curve("symmetry", 10) = {1,8};
Physical Surface("interior", 13) = {3, 2, 1};

