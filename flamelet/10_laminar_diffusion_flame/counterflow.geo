// Sung, Liu, Law, Structural response of counterflow diffusion flames to strain rate variations
// Combustion and Flame 102 (1995)
//+
Point(1) = {0, 0, 0, 1.0};
Point(2) = {0, 0.013, 0, 1.0};
Point(3) = {0.007, 0.013, 0, 1.0};


Point(8) = {0.007, 0, 0, 1.0};
Point(9) = {0, 0.003, 0, 1.0};
Point(10) = {0, 0.010, 0, 1.0};
Point(11) = {0.007, 0.010, 0, 1.0};
Point(12) = {0.007, 0.003, 0, 1.0};

Point(17) = {0.020, 0.0, 0, 1.0};
Point(18) = {0.020, 0.013, 0, 1.0};
Point(19) = {0.020, 0.004, 0, 1.0};
Point(20) = {0.020, 0.009, 0, 1.0};

Point(21) = {0.0, -0.005, 0, 1.0};
Point(22) = {0.007, -0.005, 0, 1.0};
//
Point(23) = {0.0, 0.018, 0, 1.0};
Point(24) = {0.007, 0.018, 0, 1.0};



//+
Line(1) = {2, 3};
Line(7) = {1, 8};
Line(9) = {10, 11};
Line(11) = {3, 11};
Line(12) = {11, 12};
Line(13) = {12, 8};
Line(14) = {9, 12};
Line(16) = {1, 9};
Line(17) = {9, 10};
Line(18) = {10, 2};

//+
Line(26) = {3, 18};
//+
Line(27) = {8, 17};
//+
Line(28) = {3, 18};
//+
Line(29) = {8, 17};
//+
Line(30) = {18, 20};
//+
Line(31) = {20, 19};
//+
Line(32) = {19, 17};
//+
Line(33) = {12, 19};
//+
Line(34) = {11, 20};


//+
Line(35) = {1, 21};
//+
Line(36) = {8, 22};
//+
Line(37) = {23, 2};
//+
Line(38) = {24, 3};
//+
Line(39) = {21, 22};
//+
Line(40) = {23, 24};

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
Curve Loop(4) = {26, 30, -34, -11};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {12, 33, -31, -34};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {13, 27, -32, -33};
//+
Plane Surface(6) = {6};
//+

//+
Curve Loop(13) = {40, 38, -1, -37};
//+
Plane Surface(13) = {13};
//+
Curve Loop(14) = {35, 39, -36, -7};
//+
Plane Surface(14) = {14};

//+
Physical Curve("inlet_fuel", 19) = {39};
Physical Curve("inlet_oxidizer", 20) = {40};
Physical Curve("wall_outlet", 25) = {30,32};
Physical Curve("outlet", 21) = {31};
Physical Curve("wall_fuel", 22) = {27,36};
Physical Curve("wall_oxidizer", 23) = {26,38};
Physical Curve("symmetry", 24) = {16, 17, 18,35,37};

Physical Surface("interior", 25) = {1,2,3,4,5,6,13,14};

//+ horizontal 1
Transfinite Curve {7, 14, 9, 1,39,40} = 30 Using Progression 1;
//+ horizontal 2
Transfinite Curve {27, 33, 34, 26} = 30 Using Progression 1;
//+ horizontal 3
Transfinite Curve {8, 15, 10, 3} = 40 Using Progression 1;
//+ horizontal 
Transfinite Curve {35,36} = 25 Using Progression 1;
//+ horizontal 
Transfinite Curve {37,38} = 25 Using Progression 1;
//+
Transfinite Curve {16, 13, 32, 6,25} = 20 Using Progression 1;
//+
Transfinite Curve {18, 11, 30, 4, 23} = 20 Using Progression 1;
//+
Transfinite Curve {17, 12, 31, 5, 24} =75 Using Progression 1;
//+
Transfinite Curve {19, 20, 21, 22} = 30 Using Progression 1;
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
Transfinite Surface {7};
//+
Transfinite Surface {8};
//+
Transfinite Surface {9};
//+
Transfinite Surface {10};
//+
Transfinite Surface {11};
//+
Transfinite Surface {12};
//+
Transfinite Surface {13};
//+
Transfinite Surface {14};
//+

//+
Recombine Surface {13, 3, 2, 1, 14, 6, 5, 4, 7, 8, 9, 12, 11, 10};
//+
Rotate {{0, 0, 1}, {0, 0, 0}, Pi/2} {
  Surface{13}; Surface{3}; Surface{4}; Surface{5}; Surface{2}; Surface{1}; Surface{14}; Surface{6}; 
}
