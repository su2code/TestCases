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
//Top block 1, solid zone
Point(11) = {0, channel_height, 0, gridsize};
Point(12) = {0, channel_height+block_height, 0, gridsize};
Point(13) = {block_length, channel_height+block_height, 0, gridsize};
Point(14) = {block_length, channel_height, 0, gridsize};

Line(11) = {11,12};
Line(12) = {12,13};
Line(13) = {13,14};
Line(14) = {14,11};

Line Loop(11) = {11,12,13,14};
Plane Surface(11) = {11};

//make structured block
Transfinite Line{11,-13} = Ny_block Using Progression Ry_block;
Transfinite Line{12,14} = Nx_block;
Transfinite Surface{11};
Recombine Surface{11};

//Physical Groups
Physical Line("block_1_walls") = {11,13};
Physical Line("block_1_top") = {12};
Physical Line("block_1_interface") = {14};
Physical Surface("block_1_body") = {11};
