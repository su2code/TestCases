//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {0, 0.013, 0, 1.0};
//+
Point(3) = {0.007, 0.013, 0, 1.0};
//+
Point(4) = {0.025, 0.013, 0, 1.0};
//+
Point(5) = {0.025, 0, 0, 1.0};
//+
Point(6) = {0.025, 0.002, 0, 1.0};
//+
Point(7) = {0.025, 0.011, 0, 1.0};
//+
Point(8) = {0.007, 0, 0, 1.0};
//+
Point(9) = {0, 0.002, 0, 1.0};
//+
Point(10) = {0, 0.011, 0, 1.0};
//+
Point(11) = {0.007, 0.011, 0, 1.0};
//+
Point(12) = {0.007, 0.002, 0, 1.0};
//+
Line(1) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 7};
//+
Line(5) = {7, 6};
//+
Line(6) = {6, 5};
//+
Line(7) = {1, 8};
//+
Line(8) = {8, 5};
//+
Line(9) = {10, 11};
//+
Line(10) = {11, 7};
//+
Line(11) = {3, 11};
//+
Line(12) = {11, 12};
//+
Line(13) = {12, 8};
//+
Line(14) = {9, 12};
//+
Line(15) = {12, 6};
//+
Line(16) = {1, 9};
//+
Line(17) = {9, 10};
//+
Line(18) = {10, 2};
//+
Curve Loop(1) = {7, -13, -14, -16};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {17, 9, 12, -14};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {18, 1, 11, -9};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {3, 4, -10, -11};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {12, 15, -5, -10};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {13, 8, -6, -15};
//+
Plane Surface(6) = {6};
//+
Physical Curve("inlet_fuel", 19) = {7};
//+
Physical Curve("inlet_oxidizer", 20) = {1};
//+
Physical Curve("outlet", 21) = {5};
//+
Physical Curve("wall_fuel", 22) = {8};
//+
Physical Curve("wall_oxidizer", 23) = {3};
//+
Physical Curve("symmetry", 24) = {16, 17, 18};
//+
Physical Surface("interior", 25) = {2, 3, 4, 5, 6, 1};
//+
Transfinite Curve {7, 14, 9, 1} = 30 Using Progression 1;
//+
Transfinite Curve {8, 15, 10, 3} = 60 Using Progression 1;
//+
Transfinite Curve {16, 13, 6} = 30 Using Progression 1;
//+
Transfinite Curve {18, 11, 4} = 30 Using Progression 1;
//+
Transfinite Curve {17, 12, 5} = 60 Using Progression 1;
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {3};
//+
Transfinite Surface {4};
//+
Transfinite Surface {5};
//+
Transfinite Surface {6};
//+
Recombine Surface {3, 2, 1, 6, 5, 4};
//+
Physical Curve("wall_out_top", 26) = {4};
//+
Physical Curve("wall_out_bottom", 27) = {6};
