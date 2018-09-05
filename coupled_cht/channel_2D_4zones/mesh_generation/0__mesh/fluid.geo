//Kattmann, 04.05.2018, Channel with blocks on top and bottom
//-------------------------------------------------------------------------------------//
//Geometric inputs
block_height = 0.2e-3;
block_length = 0.5e-3;
channel_height = 0.2e-3;
channel_length = block_length*3 + (block_length/2)*2;

//Mesh inputs
gridsize = 0.0001;

Nx_block = 11; // must be odd
Ny_block = 9;
Ry_block = 1.3;

Nx_channel = 3*Nx_block + 2*((Nx_block-1)/2-1);
Ny_channel = 9;
Ry_channel = 0.7;

//Each zone is completely self-sufficient (i.e. points, lines, etc.)
//-------------------------------------------------------------------------------------//
//Fluid zone, channel
Point(51) = {0, 0, 0, gridsize};
Point(52) = {0, channel_height, 0, gridsize};
Point(53) = {channel_length, channel_height, 0, gridsize};
Point(54) = {channel_length,0 , 0, gridsize};
Point(55) = {block_length, channel_height, 0, gridsize};
Point(56) = {block_length*3/2, channel_height, 0, gridsize};
Point(57) = {block_length*5/2, channel_height, 0, gridsize};
Point(58) = {block_length*3, channel_height, 0, gridsize};
Point(59) = {block_length, 0, 0, gridsize};
Point(60) = {block_length*3/2, 0, 0, gridsize};
Point(61) = {block_length*5/2, 0, 0, gridsize};
Point(62) = {block_length*3, 0, 0, gridsize};

//inlet and outlet
Line(51) = {51,52};
Line(53) = {53,54};
//fluid top
Line(55) = {52,55};
Line(56) = {55,56};
Line(57) = {56,57};
Line(58) = {57,58};
Line(59) = {58,53};
//fluid borrom
Line(60) = {54,62};
Line(61) = {62,61};
Line(62) = {61,60};
Line(63) = {60,59};
Line(64) = {59,51};
//in the domain
Line(65) = {59,55};
Line(66) = {60,56};
Line(67) = {61,57};
Line(68) = {62,58};

Line Loop(51) = {51,55,-65,64};
Line Loop(52) = {65,56,-66,63};
Line Loop(53) = {66,57,-67,62};
Line Loop(54) = {67,58,-68,61};
Line Loop(55) = {68,59,53,60};
Plane Surface(51) = {51};
Plane Surface(52) = {52};
Plane Surface(53) = {53};
Plane Surface(54) = {54};
Plane Surface(55) = {55};

//make structured channel
Transfinite Line{51,65,-53,65,66,67,68,-53} = Ny_channel Using Progression Ry_channel;
Transfinite Line{55,-64,57,59,-62,-60} = Nx_block;
Transfinite Line{56,58,-63,-61} = (Nx_block+1)/2;
Transfinite Surface{51};
Transfinite Surface{52};
Transfinite Surface{53};
Transfinite Surface{54};
Transfinite Surface{55};
Recombine Surface{51};
Recombine Surface{52};
Recombine Surface{53};
Recombine Surface{54};
Recombine Surface{55};

//Physical Groups
Physical Line("inlet") = {51};
Physical Line("outlet") = {53};
Physical Line("fluid_bottom") = {64,63,62,61,60};
Physical Line("fluid_top_walls") = {56,58};
Physical Line("fluid_top_block1") = {55};
Physical Line("fluid_top_block2") = {57};
Physical Line("fluid_top_block3") = {59};
Physical Surface("fluid_body") = {51,52,53,54,55};
