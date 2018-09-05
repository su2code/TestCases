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
//Top block 2, solid zone
Point(21) = {block_length*3/2, channel_height, 0, gridsize};
Point(22) = {block_length*3/2, channel_height+block_height, 0, gridsize};
Point(23) = {block_length*3/2 + block_length, channel_height+block_height, 0, gridsize};
Point(24) = {block_length*3/2 + block_length, channel_height, 0, gridsize};

Line(21) = {21,22};
Line(22) = {22,23};
Line(23) = {23,24};
Line(24) = {24,21};

Line Loop(21) = {21,22,23,24};
Plane Surface(21) = {21};

//make structured block
Transfinite Line{21,-23} = Ny_block Using Progression Ry_block;
Transfinite Line{22,24} = Nx_block;
Transfinite Surface{21};
Recombine Surface{21};

//Physical Groups
Physical Line("block_2_walls") = {21,23};
Physical Line("block_2_top") = {22};
Physical Line("block_2_interface") = {24};
Physical Surface("block_2_body") = {21};
