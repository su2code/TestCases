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
//Top block, solid zone
Point(11) = {0, channel_height, 0, gridsize};
Point(12) = {0, channel_height+block_height, 0, gridsize};
Point(13) = {channel_length, channel_height+block_height, 0, gridsize};
Point(14) = {channel_length,channel_height , 0, gridsize};
Point(15) = {top_dist, channel_height+block_height, 0, gridsize};
Point(16) = {top_dist, channel_height, 0, gridsize};

Line(11) = {11,12};
Line(12) = {12,15};
Line(13) = {15,13};
Line(14) = {13,14};
Line(15) = {14,16};
Line(16) = {16,11};
Line(17) = {15,16};

Line Loop(11) = {11,12,17,16};
Line Loop(12) = {-17,13,14,15};
Plane Surface(11) = {11};
Plane Surface(12) = {12};

//make structured blocks
//left
Transfinite Line{11,-17,-14} = Ny_block Using Progression Ry_block;
Transfinite Line{12,16} = Nx/2+1;
Transfinite Surface{11};
Recombine Surface{11};
//right
Transfinite Line{-14,-17} = Ny_block Using Progression Ry_block;
Transfinite Line{13,15} = Nx/2+1;
Transfinite Surface{12};
Recombine Surface{12};

//Physical Groups
Physical Line("top_block_walls") = {11,14};
Physical Line("top_block_fluid_interface") = {16,15};
Physical Line("top_block_topleft") = {12};
Physical Line("top_block_topright") = {13};
//-------------------------------------------------------------------------------------//
