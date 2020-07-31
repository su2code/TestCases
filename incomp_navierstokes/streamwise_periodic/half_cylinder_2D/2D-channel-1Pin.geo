// ----------------------------------------------------------------------------------- //
// T. Kattmann, 13.05.2018, Channel with 1 Pin
// Create the mesh by calling this geo file with 'gmsh <this>.geo'.
// For multizone mesh the zonal meshes have to be created using the first 
// option 'Which_Mesh_Part' below and have to be married appropriatley.
// ----------------------------------------------------------------------------------- //

// Which domain part should be handled
Which_Mesh_Part= 1;// 0=all, 1=Fluid, 2=Solid
// Evoque Meshing Algorithm?
Do_Meshing= 1; // 0=false, 1=true
// Write Mesh files in .su2 format
Write_mesh= 1; // 0=false, 1=true
// Translation in streamwise direction
number_duplicates = 0;

//Geometric inputs, ch: channel, Pin center is origin
//ch_height > pin_outer_r + ch_box
ch_height = 2e-3;
//ch_front & ch_back > pin_outer_r + ch_box
ch_front = 3e-3; // front length
ch_back = 5e-3; // back length
ch_box = 0.5e-3; // for extension of pin mesh

pin_outer_r = 1e-3;
pin_inner_r = 0.25e-3;

// Derived Parameters
domain_length= ch_front+ch_back;

Printf("===================================");
Printf("Free parameters:");
Printf("-> outer pin diameter: %g", pin_outer_r);
Printf("-> inner pin diameter: %g", pin_inner_r);
Printf("-> channel height: %g", ch_height);
Printf("-> channel lenght: %g", domain_length);
Printf("-> #duplicates: %g", number_duplicates);
Printf("===================================");

// ----------------------------------------------------------------------------------- //
//Mesh inputs
gridsize = 0.1; // unimportant one everything is structured

//ch_box 
Nch_box = 30;
Rch_box = 1.1;

Nch_front = 30;
Nch_back = 60;

//upper wall
Nupper_wall = 20;
Rupper_wall = 1.1;

//Pin in radial direction
Npin_radial = 20; // for all pin segments
Rpin_radial = 1.2;
//Pin in circumferential direction
Npin1_circ = 40; 
Npin2_circ = 2*Npin1_circ;
Npin3_circ = Npin1_circ;

// Each zone is self-sufficient (i.e. has all of its own Points/Lines etc.)
// ----------------------------------------------------------------------------------- //
// Fluid zone
If (Which_Mesh_Part == 0 || Which_Mesh_Part == 1)

    //Points
    Point(1) = {0, 0, 0, gridsize};
    Point(2) = {-pin_outer_r, 0, 0, gridsize};
    Point(3) = {-pin_outer_r*Cos(45*Pi/180), pin_outer_r*Sin(45*Pi/180), 0, gridsize};
    Point(4) = {pin_outer_r*Cos(45*Pi/180), pin_outer_r*Sin(45*Pi/180), 0, gridsize};
    Point(5) = {pin_outer_r, 0, 0, gridsize};

    Point(6) = {-(pin_outer_r+ch_box), 0, 0, gridsize};
    Point(7) = {-(pin_outer_r+ch_box), pin_outer_r+ch_box, 0, gridsize};
    Point(8) = {pin_outer_r+ch_box, pin_outer_r+ch_box, 0, gridsize};
    Point(9) = {pin_outer_r+ch_box, 0, 0, gridsize};

    Point(10) = {-ch_front, 0, 0, gridsize};
    Point(11) = {-ch_front, pin_outer_r+ch_box, 0, gridsize};
    Point(12) = {-ch_front, ch_height, 0, gridsize};
    Point(13) = {-(pin_outer_r+ch_box), ch_height, 0, gridsize};
    Point(14) = {(pin_outer_r+ch_box), ch_height, 0, gridsize};
    Point(15) = {ch_back, ch_height, 0, gridsize};
    Point(16) = {ch_back, pin_outer_r+ch_box, 0, gridsize};
    Point(17) = {ch_back, 0, 0, gridsize};

    //Lines
    Circle(1) = {2, 1, 3};
    Circle(2) = {3, 1, 4};
    Circle(3) = {4, 1, 5};

    Line(4) = {6,2};
    Line(5) = {10,6};
    Line(6) = {10,11};
    Line(7) = {11,12};
    Line(8) = {12,13};
    Line(9) = {11,7};
    Line(10) = {13,7};
    Line(11) = {6,7};
    Line(12) = {7,3};
    Line(13) = {13,14};
    Line(14) = {7,8};
    Line(15) = {8,4};
    Line(16) = {5,9};
    Line(17) = {9,8};
    Line(18) = {14,8};
    Line(19) = {14,15};
    Line(20) = {8,16};
    Line(21) = {9,17};
    Line(22) = {17,16};
    Line(23) = {15,16};

    //Lineloops and surfaces
    Line Loop(1) = {-4, 11, 12, -1}; Plane Surface(1) = {1};
    Line Loop(2) = {-2, -12, 14, 15}; Plane Surface(2) = {2};
    Line Loop(3) = {-16, -3, -15, -17}; Plane Surface(3) = {3};
    Line Loop(4) = {-5, 6, 9, -11}; Plane Surface(4) = {4};
    Line Loop(5) = {-9, 7, 8, 10}; Plane Surface(5) = {5};
    Line Loop(6) = {-14, -10, 13, 18}; Plane Surface(6) = {6};
    Line Loop(7) = {-20, -18, 19, 23}; Plane Surface(7) = {7};
    Line Loop(8) = {-21, 17, 20, -22}; Plane Surface(8) = {8};

    //make structured mesh with transfinite lines
    //ch_box
    Transfinite Line{1, 11, 6} = Npin1_circ;
    Transfinite Line{2, 14, 13} = Npin2_circ;
    Transfinite Line{3, -17, -22} = Npin3_circ;
    Transfinite Line{-4, -12, -15, 16} = Nch_box Using Progression Rch_box;
    //
    Transfinite Line{-7, 10, 18, 23} = Nupper_wall Using Progression Rupper_wall;
    Transfinite Line{5, 9, 8} = Nch_front;
    Transfinite Line{21, 20, 19} = Nch_back;

    //Physical Groups
    Physical Line("inlet") = {6, 7};
    If (number_duplicates == 0) 
        Physical Line("outlet") = {22, 23}; 
    EndIf
    Physical Line("fluid_top") = {8, 13, 19};
    Physical Line("fluid_pin_interface") = {1, 2, 3};
    Physical Line("fluid_sym") = {5, 4, 16, 21};
    Physical Surface("fluid_body") = {1,2,3,4,5,6,7,8};

EndIf

// ----------------------------------------------------------------------------------- //
// Pin zone
If (Which_Mesh_Part == 0 || Which_Mesh_Part == 2)

    // Points
    Point(31) = {0, 0, 0, gridsize};

    Point(32) = {-pin_inner_r, 0, 0, gridsize};
    Point(33) = {-pin_outer_r, 0, 0, gridsize};
    Point(34) = {-pin_outer_r*Cos(45*Pi/180), pin_outer_r*Sin(45*Pi/180), 0, gridsize};
    Point(35) = {-pin_inner_r*Cos(45*Pi/180), pin_inner_r*Sin(45*Pi/180), 0, gridsize};

    Point(36) = {pin_outer_r*Cos(45*Pi/180), pin_outer_r*Sin(45*Pi/180), 0, gridsize};
    Point(37) = {pin_inner_r*Cos(45*Pi/180), pin_inner_r*Sin(45*Pi/180), 0, gridsize};

    Point(38) = {pin_outer_r, 0, 0, gridsize};
    Point(39) = {pin_inner_r, 0, 0, gridsize};

    // Lines
    Line(31) = {32, 33};
    Circle(32) = {33, 31, 34};
    Line(33) = {34, 35};
    Circle(34) = {35, 31, 32};

    Circle(35) = {34, 31, 36};
    Line(36) = {36, 37};
    Circle(37) = {37, 31, 35};

    Circle(38) = {36, 31, 38};
    Line(39) = {38, 39};
    Circle(40) = {39, 31, 37};

    //Lineloops and surfaces
    //segment 1
    Line Loop(31) = {31, 32, 33, 34}; Plane Surface(31) = {31};
    //segment 2
    Line Loop(32) = {37, -33, 35, 36}; Plane Surface(32) = {32};
    //segment 3
    Line Loop(33) = {39, 40, -36, 38}; Plane Surface(33) = {33};

    //make structured mesh with transfinite lines
    //segment 1 Transfinite Line{-31, 33} = Npin_radial Using Progression Rpin_radial;
    Transfinite Line{32, -34} = Npin1_circ;

    //segment 2
    Transfinite Line{-31, 33, 36, 39} = Npin_radial Using Progression Rpin_radial;
    Transfinite Line{35, -37} = Npin2_circ;

    //segement 3
    //Transfinite Line{36, 39} = Npin_radial Using Progression Rpin_radial;
    Transfinite Line{38, -40} = Npin3_circ;

    //Physical Groups
    Physical Line("pin_fluid_interface") = {32, 35, 38};
    Physical Line("pin_sym") = {31, 39};
    Physical Line("pin_inner") = {34, 37, 40};
    Physical Surface("pin_body") = {31, 32, 33};

EndIf

// ------------------------------------------------------------------------- //
// Scale by a factor, everything beyond point position definition is just 
// connection and therefor independent of the scale
//scale_factor= 10;
//all_points[] = Point '*';
//all_lines[] = Line '*';
//Dilate {{0, 0, 0}, {scale_factor, scale_factor, scale_factor}} {
//    Point{all_points[]}; // Select all Points
//    Line{all_lines[]};
//}

// ----------------------------------------------------------------------------------- //

If(number_duplicates > 0)

    //Put all Points, Lines and Surfaces in arrays http://onelab.info/pipermail/gmsh/2017/011186.html
    p[] = Point "*";
    l[] = Line "*";
    s[] = Surface "*";

    //Removal of doubled points at stichted surfaces (in/outlet) http://gmsh.info/doc/texinfo/gmsh.html
    Geometry.AutoCoherence = 0;
    //Keep meshing iformation on duplicated domain https://stackoverflow.com/questions/49197879/duplicate-structured-surface-mesh-in-gmsh/50079210
    Geometry.CopyMeshingMethod = 1;

    //Note that for some lines the prescribed Progression of the Transfinite Line is not CopyMeshingMethod
    //correctly. Simply reversing the Line orientation (i.e. switching points) and reversing the sign in the
    //following definition fixes the problem.
    For i In {1:number_duplicates}

        // Translate all points 
        Translate {i*domain_length, 0, 0} { Duplicata { Point{ p[] }; } }

        If (Which_Mesh_Part == 0 || Which_Mesh_Part == 1)
            // Translate Lines: fluid_top, fluid_pin_interface, fluid_sym and add to Physical Tag name
            new_fluid_top[] = Translate {i*domain_length, 0, 0} { Duplicata { Line{ 8, 13, 19 }; } };
            Physical Line("fluid_top") += { new_fluid_top[] };

            new_fluid_pin_interface[] = Translate {i*domain_length, 0, 0} { Duplicata { Line { 1, 2, 3 }; } };
            Physical Line("fluid_pin_interface") += { new_fluid_pin_interface[] };

            new_fluid_sym[] = Translate {i*domain_length, 0, 0} { Duplicata { Line{ 5, 4, 16, 21 }; } };
            Physical Line("fluid_sym") += { new_fluid_sym[] };

            //If it is the last copy, set the outlet marker
            If (i == number_duplicates)
                new_outlet[] = Translate {i*domain_length, 0, 0} { Duplicata { Line { 22, 23 }; } };
                Physical Line("outlet") = { new_outlet[] };
                Printf("Outlet lines: %g , %g", new_outlet[0], new_outlet[1] );
            EndIf

            //Translate Surface: fluid_body and add to Physical Tag name
            new_fluid_body[] = Translate {i*domain_length, 0, 0} { Duplicata { Surface{ 1,2,3,4,5,6,7,8 }; } };
            Physical Surface("fluid_body") += { new_fluid_body[] };
        EndIf

        // Duplicate Pins
        If (Which_Mesh_Part == 0 || Which_Mesh_Part == 2)

            new_pin_fluid_interface[] = Translate {i*domain_length, 0, 0} { Duplicata { Line{ 32,35,38 }; } };
            Physical Line("pin_fluid_interface") += { new_pin_fluid_interface[] };

            new_pin_sym[] = Translate {i*domain_length, 0, 0} { Duplicata { Line{ 31, 39 }; } };
            Physical Line("pin_sym") += { new_pin_sym[] };

            new_pin_inner[] = Translate {i*domain_length, 0, 0} { Duplicata { Line{ 34, 37, 40 }; } };
            Physical Line("pin_inner") += { new_pin_inner[] };

            new_pin_body[] = Translate {i*domain_length, 0, 0} { Duplicata { Surface{ 31, 32, 33 }; } };
            Physical Surface("pin_body") += { new_pin_body[] };

        EndIf // Solid

    EndFor // Loop duplicates
    Coherence; // Remove all identical entities
EndIf

// ----------------------------------------------------------------------------------- //
// Meshing
Transfinite Surface "*";
Recombine Surface "*";

If (Do_Meshing == 1)
    Mesh 1; Mesh 2;
EndIf

// ----------------------------------------------------------------------------------- //
// Write .su2 meshfile
If (Write_mesh == 1)

    Mesh.Format = 42; // .su2 mesh format, 
    If (Which_Mesh_Part == 1)
        Save "fluid.su2";
    ElseIf (Which_Mesh_Part == 2 && !(number_duplicates > 0))
        Save "solid.su2";
    Else
        Printf("Unvalid Which_Mesh_Part variable.");
        Abort;
    EndIf

EndIf

// ----------------------------------------------------------------------------------- //
// Note to self: I actually don't know if this works for mesh copying so I leave this in for now ... I'll check later 
// See http://tutorial.math.lamar.edu/Classes/CalcIII/EqnsOfPlanes.aspx for explanation of the 4
// Symmetry{...} parameters.
// Note that transfinite lines are currently broken with symmetry
//Symmetry {0, 1, 0, 0} {
//  Duplicata { Surface{4}; Surface{1}; Surface{2}; Surface{31}; Surface{33}; Surface{32}; Surface{3}; Surface{8}; Surface{7}; Surface{6}; Surface{5}; }
//}
//Coherence;
