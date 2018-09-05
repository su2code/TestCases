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
//Fluid zone, channel
Point(1) = {0, 0, 0, gridsize};
Point(2) = {0, channel_height, 0, gridsize};
Point(3) = {channel_length, channel_height, 0, gridsize};
Point(4) = {channel_length,0 , 0, gridsize};

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Line Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};

//make structured channel
Transfinite Line{1,-3} = Ny_channel Using Bump Ry_channel;
Transfinite Line{2,4} = Nx;
Transfinite Surface{1};
Recombine Surface{1};

//Physical Groups
Physical Line("inlet") = {1};
Physical Line("outlet") = {3};
Physical Line("fluid_top") = {2};
Physical Line("fluid_bottom") = {4};
//-------------------------------------------------------------------------------------//
