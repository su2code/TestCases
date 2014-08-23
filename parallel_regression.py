#!/usr/bin/env python 

## \file parallel_regression.py
#  \brief Python script for automated regression testing of SU2 examples
#  \author Aniket C. Aranake, Alejandro Campos, Thomas D. Economon, Trent Lukaczyk
#  \version 3.2
#
# Stanford University Unstructured (SU2) Code
# Copyright (C) 2012-2014 Aerospace Design Laboratory
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys,time, os, subprocess, datetime, signal, os.path
from TestCase import TestCase    

def main():
    '''This program runs SU^2 and ensures that the output matches specified values. 
       This will be used to do nightly checks to make sure nothing is broken. '''

    workdir = os.getcwd()

    # environment variables for SU2
    os.environ['SU2_HOME'] = '/home/ale11/.cruise/projects/parallel_regression/work/SU2'
    os.environ['SU2_RUN'] = '/home/ale11/.cruise/projects/parallel_regression/work/SU2/bin'
    os.environ['PATH'] = os.environ['PATH'] + ':' + os.environ['SU2_RUN']

    # sync SU2 repo
    os.chdir( os.environ['SU2_HOME'] )
    os.system('git pull')  

    # Build SU2_CFD in parallel using autoconf
    os.system('./configure --prefix=$SU2_HOME --with-MPI=mpicxx CXXFLAGS="-O3"')
    os.system('make clean')
    os.system('make install')

    os.chdir(os.environ['SU2_RUN'])
    if not os.path.exists("./SU2_CFD"):
        print 'Could not build SU2_CFD'
        sys.exit(1)

    if not os.path.exists("./SU2_PRT"):
        print 'Could not build SU2_PRT'
        sys.exit(1)

    os.chdir(workdir)  
    test_list = []

    ##########################
    ### Compressible Euler ###
    ##########################

    # Channel
    channel           = TestCase('channel')
    channel.cfg_dir   = "euler/channel"
    channel.cfg_file  = "inv_channel_RK.cfg"
    channel.test_iter = 100
    channel.test_vals = [-2.413232,2.965227,0.007590,0.051651]
    channel.su2_exec  = "parallel_computation.py -f"
    channel.timeout   = 1600
    channel.tol       = 0.00001
    test_list.append(channel)

    # NACA0012 
    naca0012           = TestCase('naca0012')
    naca0012.cfg_dir   = "euler/naca0012"
    naca0012.cfg_file  = "inv_NACA0012_Roe.cfg"
    naca0012.test_iter = 100
    naca0012.test_vals = [-6.149012,-5.528869,0.334821,0.022212]
    naca0012.su2_exec  = "parallel_computation.py -f"
    naca0012.timeout   = 1600
    naca0012.tol       = 0.00001
    test_list.append(naca0012)

    # Supersonic wedge 
    wedge           = TestCase('wedge')
    wedge.cfg_dir   = "euler/wedge"
    wedge.cfg_file  = "inv_wedge_HLLC.cfg"
    wedge.test_iter = 100
    wedge.test_vals = [-2.680761,3.156839,-0.252403,0.044445]
    wedge.su2_exec  = "parallel_computation.py -f"
    wedge.timeout   = 1600
    wedge.tol       = 0.00001
    test_list.append(wedge)

    # ONERA M6 Wing
    oneram6           = TestCase('oneram6')
    oneram6.cfg_dir   = "euler/oneram6"
    oneram6.cfg_file  = "inv_ONERAM6_JST.cfg"
    oneram6.test_iter = 10
    oneram6.test_vals = [-4.830407,-4.275436,0.288842,0.016334]
    oneram6.su2_exec  = "parallel_computation.py -f"
    oneram6.timeout   = 3200
    oneram6.tol       = 0.00001
    test_list.append(oneram6)

    ##########################
    ###  Compressible N-S  ###
    ##########################

    # Laminar flat plate
    flatplate           = TestCase('flatplate')
    flatplate.cfg_dir   = "navierstokes/flatplate"
    flatplate.cfg_file  = "lam_flatplate.cfg"
    flatplate.test_iter = 100
    flatplate.test_vals = [-5.234581,0.260131,-0.167010,0.012885]
    flatplate.su2_exec  = "parallel_computation.py -f"
    flatplate.timeout   = 1600
    flatplate.tol       = 0.00001
    test_list.append(flatplate)


    # Laminar cylinder (steady)
    cylinder           = TestCase('cylinder')
    cylinder.cfg_dir   = "navierstokes/cylinder"
    cylinder.cfg_file  = "lam_cylinder.cfg"
    cylinder.test_iter = 25
    cylinder.test_vals = [-6.748270,-1.281365,0.096480,-1.541539]
    cylinder.su2_exec  = "parallel_computation.py -f"
    cylinder.timeout   = 1600
    cylinder.tol       = 0.00001
    test_list.append(cylinder)

    ##########################
    ### Compressible RANS  ###
    ##########################

    # RAE2822 SA
    rae2822_sa           = TestCase('rae2822_sa')
    rae2822_sa.cfg_dir   = "rans/rae2822"
    rae2822_sa.cfg_file  = "turb_SA_RAE2822.cfg"
    rae2822_sa.test_iter = 100
    rae2822_sa.test_vals = [-3.634245,-5.433694,0.886579,0.024338] #last 4 columns
    rae2822_sa.su2_exec  = "parallel_computation.py -f"
    rae2822_sa.timeout   = 1600
    rae2822_sa.tol       = 0.00001
    test_list.append(rae2822_sa)
    
    # RAE2822 SST
    rae2822_sst           = TestCase('rae2822_sst')
    rae2822_sst.cfg_dir   = "rans/rae2822"
    rae2822_sst.cfg_file  = "turb_SST_RAE2822.cfg"
    rae2822_sst.test_iter = 100
    rae2822_sst.test_vals = [-1.214299,4.029754,0.888047,0.024408] #last 4 columns
    rae2822_sst.su2_exec  = "parallel_computation.py -f"
    rae2822_sst.timeout   = 1600
    rae2822_sst.tol       = 0.00001
    test_list.append(rae2822_sst)

    # Flat plate
    turb_flatplate           = TestCase('turb_flatplate')
    turb_flatplate.cfg_dir   = "rans/flatplate"
    turb_flatplate.cfg_file  = "turb_SA_flatplate.cfg"
    turb_flatplate.test_iter = 100
    turb_flatplate.test_vals = [-5.057473,-7.347789,-0.187197,0.010819] #last 4 columns
    turb_flatplate.su2_exec  = "parallel_computation.py -f"
    turb_flatplate.timeout   = 1600
    turb_flatplate.tol       = 0.00001
    test_list.append(turb_flatplate)

    # ONERA M6 Wing
    turb_oneram6           = TestCase('turb_oneram6')
    turb_oneram6.cfg_dir   = "rans/oneram6"
    turb_oneram6.cfg_file  = "turb_ONERAM6.cfg"
    turb_oneram6.test_iter = 10
    turb_oneram6.test_vals = [-2.327518,-6.563377,0.230436,0.155816] #last 4 columns
    turb_oneram6.su2_exec  = "parallel_computation.py -f"
    turb_oneram6.timeout   = 3200
    turb_oneram6.tol       = 0.00001
    test_list.append(turb_oneram6)

    # NACA0012
    turb_naca0012           = TestCase('turb_naca0012')
    turb_naca0012.cfg_dir   = "rans/naca0012"
    turb_naca0012.cfg_file  = "turb_NACA0012.cfg"
    turb_naca0012.test_iter = 20
    turb_naca0012.test_vals = [-2.826348,-7.364208,-0.000065,0.803130] #last 4 columns
    turb_naca0012.su2_exec  = "parallel_computation.py -f"
    turb_naca0012.timeout   = 3200
    turb_naca0012.tol       = 0.00001
    test_list.append(turb_naca0012)

    ############################
    ### Incompressible RANS  ###
    ############################

    # NACA0012
    inc_turb_naca0012           = TestCase('inc_turb_naca0012')
    inc_turb_naca0012.cfg_dir   = "incomp_rans/naca0012"
    inc_turb_naca0012.cfg_file  = "naca0012.cfg"
    inc_turb_naca0012.test_iter = 20
    inc_turb_naca0012.test_vals = [-4.709964,-11.007318,0.000012,0.211084] #last 4 columns
    inc_turb_naca0012.su2_exec  = "parallel_computation.py -f"
    inc_turb_naca0012.timeout   = 1600
    inc_turb_naca0012.tol       = 0.00001
    test_list.append(inc_turb_naca0012)

    #####################################
    ### Cont. adj. compressible Euler ###
    #####################################

    # Inviscid NACA0012
    contadj_naca0012           = TestCase('contadj_naca0012')
    contadj_naca0012.cfg_dir   = "cont_adj_euler/naca0012"
    contadj_naca0012.cfg_file  = "inv_NACA0012.cfg"
    contadj_naca0012.test_iter = 5
    contadj_naca0012.test_vals = [-12.135515,-16.000000,0.005483,0.536870] #last 4 columns
    contadj_naca0012.su2_exec  = "parallel_computation.py -f"
    contadj_naca0012.timeout   = 1600
    contadj_naca0012.tol       = 0.00001
    test_list.append(contadj_naca0012)

    # Inviscid ONERA M6
    contadj_oneram6           = TestCase('contadj_oneram6')
    contadj_oneram6.cfg_dir   = "cont_adj_euler/oneram6"
    contadj_oneram6.cfg_file  = "inv_ONERAM6.cfg"
    contadj_oneram6.test_iter = 5
    contadj_oneram6.test_vals = [-6.352088,-6.532237,-0.000023,0.147720] #last 4 columns
    contadj_oneram6.su2_exec  = "parallel_computation.py -f"
    contadj_oneram6.timeout   = 1600
    contadj_oneram6.tol       = 0.00001
    test_list.append(contadj_oneram6)

    ###################################
    ### Cont. adj. compressible N-S ###
    ###################################

    # Adjoint laminar cylinder
    contadj_ns_cylinder           = TestCase('contadj_ns_cylinder')
    contadj_ns_cylinder.cfg_dir   = "cont_adj_navierstokes/cylinder"
    contadj_ns_cylinder.cfg_file  = "lam_cylinder.cfg"
    contadj_ns_cylinder.test_iter = 100
    contadj_ns_cylinder.test_vals = [-0.586316,-6.050120,-0.032305,25.115000] #last 4 columns
    contadj_ns_cylinder.su2_exec  = "parallel_computation.py -f"
    contadj_ns_cylinder.timeout   = 1600
    contadj_ns_cylinder.tol       = 0.00001
    test_list.append(contadj_ns_cylinder)

    # Adjoint laminar naca0012 subsonic
    contadj_ns_naca0012_sub           = TestCase('contadj_ns_naca0012_sub')
    contadj_ns_naca0012_sub.cfg_dir   = "cont_adj_navierstokes/naca0012_sub"
    contadj_ns_naca0012_sub.cfg_file  = "lam_NACA0012.cfg"
    contadj_ns_naca0012_sub.test_iter = 100
    contadj_ns_naca0012_sub.test_vals = [-4.234330,-9.705736,0.005161,0.398940] #last 4 columns
    contadj_ns_naca0012_sub.su2_exec  = "parallel_computation.py -f"
    contadj_ns_naca0012_sub.timeout   = 1600
    contadj_ns_naca0012_sub.tol       = 0.00001
    test_list.append(contadj_ns_naca0012_sub)
    
    # Adjoint laminar naca0012 transonic
    contadj_ns_naca0012_trans           = TestCase('contadj_ns_naca0012_trans')
    contadj_ns_naca0012_trans.cfg_dir   = "cont_adj_navierstokes/naca0012_trans"
    contadj_ns_naca0012_trans.cfg_file  = "lam_NACA0012.cfg"
    contadj_ns_naca0012_trans.test_iter = 100
    contadj_ns_naca0012_trans.test_vals = [-1.810435,-6.920519,0.014614,1.020100] #last 4 columns
    contadj_ns_naca0012_trans.su2_exec  = "parallel_computation.py -f"
    contadj_ns_naca0012_trans.timeout   = 1600
    contadj_ns_naca0012_trans.tol       = 0.00001
    test_list.append(contadj_ns_naca0012_trans)

    #######################################################
    ### Cont. adj. compressible RANS (frozen viscosity) ###
    #######################################################

    # Adjoint turbulent NACA0012
    contadj_rans_naca0012           = TestCase('contadj_rans_naca0012')
    contadj_rans_naca0012.cfg_dir   = "cont_adj_rans/naca0012"
    contadj_rans_naca0012.cfg_file  = "turb_nasa.cfg"
    contadj_rans_naca0012.test_iter = 100
    contadj_rans_naca0012.test_vals = [-4.351102,-8.919996,-1.275200,-2.541400] #last 4 columns
    contadj_rans_naca0012.su2_exec  = "parallel_computation.py -f"
    contadj_rans_naca0012.timeout   = 1600
    contadj_rans_naca0012.tol       = 0.00001
    test_list.append(contadj_rans_naca0012)
    
    # Adjoint turbulent RAE2822
    contadj_rans_rae2822           = TestCase('contadj_rans_rae822')
    contadj_rans_rae2822.cfg_dir   = "cont_adj_rans/rae2822"
    contadj_rans_rae2822.cfg_file  = "turb_SA_RAE2822.cfg"
    contadj_rans_rae2822.test_iter = 100
    contadj_rans_rae2822.test_vals = [-2.872467,-8.347153,4.525800,0.360080] #last 4 columns
    contadj_rans_rae2822.su2_exec  = "parallel_computation.py -f"
    contadj_rans_rae2822.timeout   = 1600
    contadj_rans_rae2822.tol       = 0.00001
    test_list.append(contadj_rans_rae2822)

    #######################################
    ### Cont. adj. incompressible Euler ###
    #######################################

    # Adjoint Incompressible Inviscid NACA0012
    contadj_incomp_NACA0012           = TestCase('contadj_incomp_NACA0012')
    contadj_incomp_NACA0012.cfg_dir   = "cont_adj_incomp_euler/naca0012"
    contadj_incomp_NACA0012.cfg_file  = "incomp_NACA0012.cfg"
    contadj_incomp_NACA0012.test_iter = 140
    contadj_incomp_NACA0012.test_vals = [-7.501598,-7.335538,0.010910,0.000000] #last 4 columns
    contadj_incomp_NACA0012.su2_exec  = "parallel_computation.py -f"
    contadj_incomp_NACA0012.timeout   = 1600
    contadj_incomp_NACA0012.tol       = 0.00001
    test_list.append(contadj_incomp_NACA0012)

    #####################################
    ### Cont. adj. incompressible N-S ###
    #####################################

    # Adjoint Incompressible Viscous Cylinder
    contadj_incomp_cylinder           = TestCase('contadj_incomp_cylinder')
    contadj_incomp_cylinder.cfg_dir   = "cont_adj_incomp_navierstokes/cylinder"
    contadj_incomp_cylinder.cfg_file  = "lam_incomp_cylinder.cfg"
    contadj_incomp_cylinder.test_iter = 25
    contadj_incomp_cylinder.test_vals = [-2.471178,-2.957206,-0.048458,0.000000] #last 4 columns
    contadj_incomp_cylinder.su2_exec  = "parallel_computation.py -f"
    contadj_incomp_cylinder.timeout   = 1600
    contadj_incomp_cylinder.tol       = 0.00001
    test_list.append(contadj_incomp_cylinder)

    ######################################
    ### Thermochemical Nonequilibrium  ###
    ######################################

    # RAM-C II Sphere-Cone -- 61km Altitude
    ramc           = TestCase('ramc')
    ramc.cfg_dir   = "tne2/ramc"
    ramc.cfg_file  = "ramc61km.cfg"
    ramc.test_iter = 25
    ramc.test_vals = [-4.638119,2.854417,-4.439628,0.000188]
    ramc.su2_exec  = "parallel_computation.py -f"
    ramc.timeout   = 1600
    ramc.tol       = 0.00001
    test_list.append(ramc)

    ######################################
    ### Moving Wall                    ###
    ######################################

    # Lid-driven cavity
    cavity           = TestCase('cavity')
    cavity.cfg_dir   = "moving_wall/cavity"
    cavity.cfg_file  = "lam_cavity.cfg"
    cavity.test_iter = 25
    cavity.test_vals = [-5.739930,-0.277880,-0.151798,-3.745224]
    cavity.su2_exec  = "parallel_computation.py -f"
    cavity.timeout   = 1600
    cavity.tol       = 0.00001
    test_list.append(cavity)

    # Spinning cylinder
    spinning_cylinder           = TestCase('spinning_cylinder')
    spinning_cylinder.cfg_dir   = "moving_wall/spinning_cylinder"
    spinning_cylinder.cfg_file  = "spinning_cylinder.cfg"
    spinning_cylinder.test_iter = 25
    spinning_cylinder.test_vals = [-6.621605,-1.171604,8.512933,0.300307]
    spinning_cylinder.su2_exec  = "parallel_computation.py -f"
    spinning_cylinder.timeout   = 1600
    spinning_cylinder.tol       = 0.00001
    test_list.append(spinning_cylinder)

    ######################################
    ### Unsteady                       ###
    ######################################

    # Square cylinder
    square_cylinder           = TestCase('square_cylinder')
    square_cylinder.cfg_dir   = "unsteady/square_cylinder"
    square_cylinder.cfg_file  = "turb_square.cfg"
    square_cylinder.test_iter = 3
    square_cylinder.test_vals = [-1.542162,0.048674,1.398952,2.196894]
    square_cylinder.su2_exec  = "parallel_computation.py -f"
    square_cylinder.timeout   = 1600
    square_cylinder.tol       = 0.00001
    test_list.append(square_cylinder)

    ######################################
    ### RUN TESTS                      ###
    ######################################

    pass_list = [ test.run_test() for test in test_list ]

    if all(pass_list):
        sys.exit(0)
    else:
        sys.exit(1)
    # done

if __name__ == '__main__':
    main()
