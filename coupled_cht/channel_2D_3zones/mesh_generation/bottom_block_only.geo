//Kattmann, 04.05.2018, Channel with blocks on top and bottom
//-------------------------------------------------------------------------------------//
//Geometric inputs
channel_height = 1e-3;
channel_length = 5e-3;
block_height = 0.2e-3;

//fixed, do not change
top_dist = channel_length/2;
bottom_dist = channel_length/2;

//Mesh inputs
gridsize = 0.0001;
Nx = 51; //must be odd!
Ny_channel = 51; //should be odd
Ry_channel = 0.1; //Bump

Ny_block = 11; //should be odd as well
Ry_block = 1.3; //Progression

//Each zone is completely self-sufficient (i.e. points, lines, etc.)
//-------------------------------------------------------------------------------------//
//Bottom  block, solid zone
Point(21) = {0, 0, 0, gridsize};
Point(22) = {channel_length, 0, 0, gridsize};
Point(23) = {channel_length, -block_height, 0, gridsize};
Point(24) = {0, -block_height, 0, gridsize};
Point(25) = {bottom_dist, 0, 0, gridsize};
Point(26) = {bottom_dist, -block_height, 0, gridsize};

Line(21) = {21,25};
Line(22) = {25,22};
Line(23) = {22,23};
Line(24) = {23,26};
Line(25) = {26,24};
Line(26) = {24,21};
Line(27) = {25,26};

Line Loop(21) = {21,27,25,26};
Line Loop(22) = {22,23,24,-27};
Plane Surface(21) = {21};
Plane Surface(22) = {22};

//make structured blocks
//left
Transfinite Line{-26,27} = Ny_block Using Progression Ry_block;
Transfinite Line{21,25} = Nx/2+1;
Transfinite Surface{21};
Recombine Surface{21};
//right
Transfinite Line{27,23} = Ny_block Using Progression Ry_block;
Transfinite Line{22,24} = Nx/2+1;
Transfinite Surface{22};
Recombine Surface{22};

//Physical Groups
Physical Line("bottom_block_walls") = {26,23};
Physical Line("bottom_block_fluid_interface") = {21,22};
Physical Line("bottom_block_bottomleft") = {25};
Physical Line("bottom_block_bottomright") = {24};
