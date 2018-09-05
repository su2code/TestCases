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
//Top block 3, solid zone
Point(31) = {block_length*3, channel_height, 0, gridsize};
Point(32) = {block_length*3, channel_height+block_height, 0, gridsize};
Point(33) = {block_length*3 + block_length, channel_height+block_height, 0, gridsize};
Point(34) = {block_length*3 + block_length, channel_height, 0, gridsize};

Line(31) = {31,32};
Line(32) = {32,33};
Line(33) = {33,34};
Line(34) = {34,31};

Line Loop(31) = {31,32,33,34};
Plane Surface(31) = {31};

//make structured block
Transfinite Line{31,-33} = Ny_block Using Progression Ry_block;
Transfinite Line{32,34} = Nx_block;
Transfinite Surface{31};
Recombine Surface{31};

//Physical Groups
Physical Line("block_3_walls") = {31,33};
Physical Line("block_3_top") = {32};
Physical Line("block_3_interface") = {34};
Physical Surface("block_3_body") = {31};
