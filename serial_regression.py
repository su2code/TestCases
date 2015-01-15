#!/usr/bin/env python

## \file serial_regression.py
#  \brief Python script for automated regression testing of SU2 examples
#  \author A. Aranake, A. Campos, T. Economon, T. Lukaczyk
#  \version 3.2.7.1 "eagle"
#
# Copyright (C) 2012-2015 SU2 Core Developers.
#
# SU2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# SU2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with SU2. If not, see <http://www.gnu.org/licenses/>.

import sys,time, os, subprocess, datetime, signal, os.path
from TestCase import TestCase

def main():
    '''This program runs SU2 and ensures that the output matches specified values. 
       This will be used to do nightly checks to make sure nothing is broken. '''

    workdir = os.getcwd()

    # environment variables for SU2
    os.environ['TEST_HOME'] = '/home/ale11/.cruise/projects/serial_regression/work'
    os.environ['SU2_HOME'] = '/home/ale11/.cruise/projects/serial_regression/work/SU2'
    os.environ['SU2_RUN'] = '/home/ale11/.cruise/projects/serial_regression/work/SU2/bin'
    os.environ['PATH'] = os.environ['PATH'] + ':' + os.environ['SU2_RUN']

    # sync Test Cases repo
    os.chdir( os.environ['TEST_HOME'] )
    os.system('git fetch')
    os.system('git checkout develop')
    os.system('git pull origin develop')
    
    # sync SU2 repo
    os.chdir( os.environ['SU2_HOME'] )
    os.system('git fetch')
    os.system('git checkout develop')
    os.system('git pull origin develop')

    # Build SU2_CFD in serial using autoconf
    os.system('./configure --prefix=$SU2_HOME CXXFLAGS="-O3"')
    os.system('make clean')
    os.system('make install')

    os.chdir(os.environ['SU2_RUN'])
    if not os.path.exists("./SU2_CFD"):
        print 'Could not build SU2_CFD'
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
    channel.test_vals = [-3.110240, 2.263506, 0.008686, 0.029098]
    channel.su2_exec  = "SU2_CFD"
    channel.timeout   = 1600
    channel.tol       = 0.00001
    test_list.append(channel)

    # NACA0012 
    naca0012           = TestCase('naca0012')
    naca0012.cfg_dir   = "euler/naca0012"
    naca0012.cfg_file  = "inv_NACA0012_Roe.cfg"
    naca0012.test_iter = 100
    naca0012.test_vals = [-6.198509, -5.577694, 0.334810, 0.022197]
    naca0012.su2_exec  = "SU2_CFD"
    naca0012.timeout   = 1600
    naca0012.tol       = 0.00001
    test_list.append(naca0012)

    # Supersonic wedge 
    wedge           = TestCase('wedge')
    wedge.cfg_dir   = "euler/wedge"
    wedge.cfg_file  = "inv_wedge_HLLC.cfg"
    wedge.test_iter = 100
    wedge.test_vals = [-1.711318, 3.913749, -0.252131, 0.044402]
    wedge.su2_exec  = "SU2_CFD"
    wedge.timeout   = 1600
    wedge.tol       = 0.00001
    test_list.append(wedge)

    # ONERA M6 Wing
    oneram6           = TestCase('oneram6')
    oneram6.cfg_dir   = "euler/oneram6"
    oneram6.cfg_file  = "inv_ONERAM6_JST.cfg"
    oneram6.test_iter = 10
    oneram6.test_vals = [-4.715342, -4.148920, 0.271678, 0.018869]
    oneram6.su2_exec  = "SU2_CFD"
    oneram6.timeout   = 9600
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
    flatplate.test_vals = [-5.231916, 0.261866, -0.166832, 0.012717]
    flatplate.su2_exec  = "SU2_CFD"
    flatplate.timeout   = 1600
    flatplate.tol       = 0.00001
    test_list.append(flatplate)


    # Laminar cylinder (steady)
    cylinder           = TestCase('cylinder')
    cylinder.cfg_dir   = "navierstokes/cylinder"
    cylinder.cfg_file  = "lam_cylinder.cfg"
    cylinder.test_iter = 25
    cylinder.test_vals = [-6.765426, -1.297422, 0.019496, 0.310082]
    cylinder.su2_exec  = "SU2_CFD"
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
    rae2822_sa.test_vals = [-3.442525, -5.441383, 0.884279, 0.024730] #last 4 columns
    rae2822_sa.su2_exec  = "SU2_CFD"
    rae2822_sa.timeout   = 1600
    rae2822_sa.tol       = 0.00001
    test_list.append(rae2822_sa)
    
    # RAE2822 SST
    rae2822_sst           = TestCase('rae2822_sst')
    rae2822_sst.cfg_dir   = "rans/rae2822"
    rae2822_sst.cfg_file  = "turb_SST_RAE2822.cfg"
    rae2822_sst.test_iter = 100
    rae2822_sst.test_vals = [-1.186943, 4.023140, 0.886788, 0.024927] #last 4 columns
    rae2822_sst.su2_exec  = "SU2_CFD"
    rae2822_sst.timeout   = 1600
    rae2822_sst.tol       = 0.00001
    test_list.append(rae2822_sst)

    # Flat plate
    turb_flatplate           = TestCase('turb_flatplate')
    turb_flatplate.cfg_dir   = "rans/flatplate"
    turb_flatplate.cfg_file  = "turb_SA_flatplate.cfg"
    turb_flatplate.test_iter = 100
    turb_flatplate.test_vals = [-5.069447, -7.354599, -0.187187, 0.010831] #last 4 columns
    turb_flatplate.su2_exec  = "SU2_CFD"
    turb_flatplate.timeout   = 1600
    turb_flatplate.tol       = 0.00001
    test_list.append(turb_flatplate)

    # ONERA M6 Wing
    turb_oneram6           = TestCase('turb_oneram6')
    turb_oneram6.cfg_dir   = "rans/oneram6"
    turb_oneram6.cfg_file  = "turb_ONERAM6.cfg"
    turb_oneram6.test_iter = 10
    turb_oneram6.test_vals = [-2.327516, -6.563376, 0.230437, 0.155816]#last 4 columns
    turb_oneram6.su2_exec  = "SU2_CFD"
    turb_oneram6.timeout   = 3200
    turb_oneram6.tol       = 0.00001
    test_list.append(turb_oneram6)

    # NACA0012
    turb_naca0012           = TestCase('turb_naca0012')
    turb_naca0012.cfg_dir   = "rans/naca0012"
    turb_naca0012.cfg_file  = "turb_NACA0012.cfg"
    turb_naca0012.test_iter = 20
    turb_naca0012.test_vals = [-2.826353, -7.364860, -0.000019, 0.801902] #last 4 columns
    turb_naca0012.su2_exec  = "SU2_CFD"
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
    inc_turb_naca0012.test_vals = [-4.710052, -11.007500, -0.000001, 0.210445] #last 4 columns
    inc_turb_naca0012.su2_exec  = "SU2_CFD"
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
    contadj_naca0012.test_vals = [-12.215877, -17.724135, 0.300920, 0.536870] #last 4 columns
    contadj_naca0012.su2_exec  = "SU2_CFD"
    contadj_naca0012.timeout   = 1600
    contadj_naca0012.tol       = 0.00001
    test_list.append(contadj_naca0012)

    # Inviscid ONERA M6
    contadj_oneram6           = TestCase('contadj_oneram6')
    contadj_oneram6.cfg_dir   = "cont_adj_euler/oneram6"
    contadj_oneram6.cfg_file  = "inv_ONERAM6.cfg"
    contadj_oneram6.test_iter = 5
    contadj_oneram6.test_vals = [-6.354670, -6.530109, -0.133220, 0.147720] #last 4 columns
    contadj_oneram6.su2_exec  = "SU2_CFD"
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
    contadj_ns_cylinder.test_vals = [-0.601729, -6.067386, -2.056900, 25.115000] #last 4 columns
    contadj_ns_cylinder.su2_exec  = "SU2_CFD"
    contadj_ns_cylinder.timeout   = 1600
    contadj_ns_cylinder.tol       = 0.00001
    test_list.append(contadj_ns_cylinder)

    # Adjoint laminar naca0012 subsonic
    contadj_ns_naca0012_sub           = TestCase('contadj_ns_naca0012_sub')
    contadj_ns_naca0012_sub.cfg_dir   = "cont_adj_navierstokes/naca0012_sub"
    contadj_ns_naca0012_sub.cfg_file  = "lam_NACA0012.cfg"
    contadj_ns_naca0012_sub.test_iter = 100
    contadj_ns_naca0012_sub.test_vals = [-4.234330, -9.705736, 0.516750, 0.398940] #last 4 columns
    contadj_ns_naca0012_sub.su2_exec  = "SU2_CFD"
    contadj_ns_naca0012_sub.timeout   = 1600
    contadj_ns_naca0012_sub.tol       = 0.00001
    test_list.append(contadj_ns_naca0012_sub)
    
    # Adjoint laminar naca0012 transonic
    contadj_ns_naca0012_trans           = TestCase('contadj_ns_naca0012_trans')
    contadj_ns_naca0012_trans.cfg_dir   = "cont_adj_navierstokes/naca0012_trans"
    contadj_ns_naca0012_trans.cfg_file  = "lam_NACA0012.cfg"
    contadj_ns_naca0012_trans.test_iter = 100
    contadj_ns_naca0012_trans.test_vals = [-1.810435, -6.920519, 1.756200, 1.020100] #last 4 columns
    contadj_ns_naca0012_trans.su2_exec  = "SU2_CFD"
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
    contadj_rans_naca0012.test_vals = [-4.351102, -8.919996, -72.511000, -2.541400] #last 4 columns
    contadj_rans_naca0012.su2_exec  = "SU2_CFD"
    contadj_rans_naca0012.timeout   = 1600
    contadj_rans_naca0012.tol       = 0.00001
    test_list.append(contadj_rans_naca0012)
    
    # Adjoint turbulent RAE2822
    contadj_rans_rae2822           = TestCase('contadj_rans_rae2822')
    contadj_rans_rae2822.cfg_dir   = "cont_adj_rans/rae2822"
    contadj_rans_rae2822.cfg_file  = "turb_SA_RAE2822.cfg"
    contadj_rans_rae2822.test_iter = 100
    contadj_rans_rae2822.test_vals = [-2.959224, -8.349094, 354.120000, 0.106450] #last 4 columns
    contadj_rans_rae2822.su2_exec  = "SU2_CFD"
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
    contadj_incomp_NACA0012.test_vals = [-7.326112, -7.153756, 1.892600, 0.000000] #last 4 columns
    contadj_incomp_NACA0012.su2_exec  = "SU2_CFD"
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
    contadj_incomp_cylinder.test_vals = [-2.476381, -2.941665, -3.081400, 0.000000] #last 4 columns
    contadj_incomp_cylinder.su2_exec  = "SU2_CFD"
    contadj_incomp_cylinder.timeout   = 1600
    contadj_incomp_cylinder.tol       = 0.00001
    test_list.append(contadj_incomp_cylinder)

    ######################################
    ### Thermochemical Nonequilibrium  ###
    ######################################
    ramc           = TestCase('ramc')
    ramc.cfg_dir   = "tne2/ramc"
    ramc.cfg_file  = "ramc61km.cfg"
    ramc.test_iter = 25
    ramc.test_vals = [-4.638119, 2.854417, -4.439628, 0.000188]
    ramc.su2_exec  = "SU2_CFD"
    ramc.timeout   = 1600
    ramc.tol       = 0.00001
    test_list.append(ramc)

#    ######################################
#    ### Spectral Method                ###
#    ######################################
#    spectral           = TestCase('spectral')
#    spectral.cfg_dir   = "spectral_method"
#    spectral.cfg_file  = "spectral.cfg"
#    spectral.test_iter = 25
#    spectral.test_vals = [-1.621870,3.852164,0.007465,0.084358]
#    spectral.su2_exec  = "SU2_CFD"
#    spectral.timeout   = 1600
#    spectral.tol       = 0.00001
#    test_list.append(spectral)

    ######################################
    ### Moving Wall                    ###
    ######################################
    
    # Lid-driven cavity
    cavity           = TestCase('cavity')
    cavity.cfg_dir   = "moving_wall/cavity"
    cavity.cfg_file  = "lam_cavity.cfg"
    cavity.test_iter = 25
    cavity.test_vals = [-5.627934, -0.164470, 0.051972, 2.547034]
    cavity.su2_exec  = "SU2_CFD"
    cavity.timeout   = 1600
    cavity.tol       = 0.00001
    test_list.append(cavity)

    # Spinning cylinder
    spinning_cylinder           = TestCase('spinning_cylinder')
    spinning_cylinder.cfg_dir   = "moving_wall/spinning_cylinder"
    spinning_cylinder.cfg_file  = "spinning_cylinder.cfg"
    spinning_cylinder.test_iter = 25
    spinning_cylinder.test_vals = [-6.854068, -1.410728, 9.092538, 0.060628]
    spinning_cylinder.su2_exec  = "SU2_CFD"
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
    square_cylinder.test_vals = [-1.542156, 0.048662, 1.398952, 2.196893]
    square_cylinder.su2_exec  = "SU2_CFD"
    square_cylinder.timeout   = 1600
    square_cylinder.tol       = 0.00001
    test_list.append(square_cylinder)

    ######################################
    ### Real_Gas                       ###
    ######################################

    # ls89_sa
    ls89_sa           = TestCase('ls89_sa')
    ls89_sa.cfg_dir   = "nicf/LS89"
    ls89_sa.cfg_file  = "turb_SA_PR.cfg"
    ls89_sa.test_iter = 100
    ls89_sa.test_vals = [-7.042592, -12.006909, 0.067512, 0.149691]
    ls89_sa.su2_exec  = "SU2_CFD"
    ls89_sa.timeout   = 1600
    ls89_sa.tol       = 0.00001
    test_list.append(ls89_sa)

#    # ls89_sst
#    ls89_sst           = TestCase('ls89_sst')
#    ls89_sst.cfg_dir   = "nicf/LS89"
#    ls89_sst.cfg_file  = "turb_SST_PR.cfg"
#    ls89_sst.test_iter = 100
#    ls89_sst.test_vals =  [-8.901415, -1.625736, 0.067797, 0.15115]
#    ls89_sst.su2_exec  = "SU2_CFD"
#    ls89_sst.timeout   = 1600
#    ls89_sst.tol       = 0.00001
#    test_list.append(ls89_sst)

    # Rarefaction shock wave edge_VW
    edge_VW           = TestCase('edge_VW')
    edge_VW.cfg_dir   = "nicf/edge"
    edge_VW.cfg_file  = "edge_VW.cfg"
    edge_VW.test_iter = 100
    edge_VW.test_vals = [-5.728637, -3.272400, -0.000046, 0.000000]
    edge_VW.su2_exec  = "SU2_CFD"
    edge_VW.timeout   = 1600
    edge_VW.tol       = 0.00001
    test_list.append(edge_VW)

    # Rarefaction shock wave edge_PPR                                                                                                                                                                                                
    edge_PPR           = TestCase('edge_PPR')
    edge_PPR.cfg_dir   = "nicf/edge"
    edge_PPR.cfg_file  = "edge_PPR.cfg"
    edge_PPR.test_iter = 100
    edge_PPR.test_vals = [-6.278519, -3.849022, -0.000056, 0.000000]
    edge_PPR.su2_exec  = "SU2_CFD"
    edge_PPR.timeout   = 1600
    edge_PPR.tol       = 0.00001
    test_list.append(edge_PPR)

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
