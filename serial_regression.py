#!/usr/bin/env python

## \file serial_regression.py
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
    os.environ['SU2_HOME'] = '/home/ale11/.cruise/projects/serial_regression/work/SU2'
    os.environ['SU2_RUN'] = '/home/ale11/.cruise/projects/serial_regression/work/SU2/bin'
    os.environ['PATH'] = os.environ['PATH'] + ':' + os.environ['SU2_RUN']

    # sync SU2 repo
    os.chdir( os.environ['SU2_HOME'] )
    os.system('git pull')

    # Build SU2_CFD in serial using autoconf
    os.system('./configure --prefix=$SU2_HOME CXXFLAGS="-O3"')
    os.system('make clean')
    os.system('make -j 24 install')

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
    channel.test_vals = [-2.489827,2.821844,0.008730,0.053947]
    channel.su2_exec  = "SU2_CFD"
    channel.timeout   = 1600
    channel.tol       = 0.00001
    test_list.append(channel)

    # NACA0012 
    naca0012           = TestCase('naca0012')
    naca0012.cfg_dir   = "euler/naca0012"
    naca0012.cfg_file  = "inv_NACA0012_Roe.cfg"
    naca0012.test_iter = 100
    naca0012.test_vals = [-3.751809,-3.271265,0.136604,0.066791]
    naca0012.su2_exec  = "SU2_CFD"
    naca0012.timeout   = 1600
    naca0012.tol       = 0.00001
    test_list.append(naca0012)

    # Supersonic wedge 
    wedge           = TestCase('wedge')
    wedge.cfg_dir   = "euler/wedge"
    wedge.cfg_file  = "inv_wedge_HLLC.cfg"
    wedge.test_iter = 100
    wedge.test_vals = [-2.717009,3.183742,-0.252144,0.044399]
    wedge.su2_exec  = "SU2_CFD"
    wedge.timeout   = 1600
    wedge.tol       = 0.00001
    test_list.append(wedge)

    # ONERA M6 Wing
    oneram6           = TestCase('oneram6')
    oneram6.cfg_dir   = "euler/oneram6"
    oneram6.cfg_file  = "inv_ONERAM6_JST.cfg"
    oneram6.test_iter = 10
    oneram6.test_vals = [-4.819422,-4.284121,0.290066,0.015809]
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
    flatplate.test_vals = [-5.225114,0.270273,0.020536,0.012860]
    flatplate.su2_exec  = "SU2_CFD"
    flatplate.timeout   = 1600
    flatplate.tol       = 0.00001
    test_list.append(flatplate)


    # Laminar cylinder (steady)
    cylinder           = TestCase('cylinder')
    cylinder.cfg_dir   = "navierstokes/cylinder"
    cylinder.cfg_file  = "lam_cylinder.cfg"
    cylinder.test_iter = 25
    cylinder.test_vals = [-6.781338,-1.335300,-0.025054,0.974312]
    cylinder.su2_exec  = "SU2_CFD"
    cylinder.timeout   = 1600
    cylinder.tol       = 0.00001
    test_list.append(cylinder)

    ##########################
    ### Compressible RANS  ###
    ##########################

    # RAE2822
    rae2822           = TestCase('rae2822')
    rae2822.cfg_dir   = "rans/rae2822"
    rae2822.cfg_file  = "turb_SA_RAE2822.cfg"
    rae2822.test_iter = 100
    rae2822.test_vals = [-3.559272,-5.452676,0.884380,0.024162] #last 4 columns
    rae2822.su2_exec  = "SU2_CFD"
    rae2822.timeout   = 1600
    rae2822.tol       = 0.00001
    test_list.append(rae2822)

    # Flat plate
    turb_flatplate           = TestCase('turb_flatplate')
    turb_flatplate.cfg_dir   = "rans/flatplate"
    turb_flatplate.cfg_file  = "turb_SA_flatplate.cfg"
    turb_flatplate.test_iter = 100
    turb_flatplate.test_vals = [-5.074224,-7.332708,0.000505,0.010354] #last 4 columns
    turb_flatplate.su2_exec  = "SU2_CFD"
    turb_flatplate.timeout   = 1600
    turb_flatplate.tol       = 0.00001
    test_list.append(turb_flatplate)

    # ONERA M6 Wing
    turb_oneram6           = TestCase('turb_oneram6')
    turb_oneram6.cfg_dir   = "rans/oneram6"
    turb_oneram6.cfg_file  = "turb_ONERAM6.cfg"
    turb_oneram6.test_iter = 10
    turb_oneram6.test_vals = [-2.343659,-6.584583,0.230390,0.155769]#last 4 columns
    turb_oneram6.su2_exec  = "SU2_CFD"
    turb_oneram6.timeout   = 3200
    turb_oneram6.tol       = 0.00001
    test_list.append(turb_oneram6)

    # NACA0012
    turb_naca0012           = TestCase('turb_naca0012')
    turb_naca0012.cfg_dir   = "rans/naca0012"
    turb_naca0012.cfg_file  = "turb_NACA0012.cfg"
    turb_naca0012.test_iter = 20
    turb_naca0012.test_vals = [-2.824671,-7.364141,-0.000026,0.803047] #last 4 columns
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
    inc_turb_naca0012.test_vals = [-4.714938,-10.911748,-0.000001,0.255901] #last 4 columns
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
    contadj_naca0012.test_iter = 100
    contadj_naca0012.test_vals = [-4.882472,-10.149505,0.006059,0.519590] #last 4 columns
    contadj_naca0012.su2_exec  = "SU2_CFD"
    contadj_naca0012.timeout   = 1600
    contadj_naca0012.tol       = 0.00001
    test_list.append(contadj_naca0012)

    # Inviscid RAM-C (To be validated with finite differences)
    contadj_ram_c           = TestCase('contadj_ram_c')
    contadj_ram_c.cfg_dir   = "cont_adj_euler/ram_c"
    contadj_ram_c.cfg_file  = "inv_RAMC.cfg"
    contadj_ram_c.test_iter = 100
    contadj_ram_c.test_vals = [0.776609,-7.308868,-0.001885,0.080464] #last 4 columns
    contadj_ram_c.su2_exec  = "SU2_CFD"
    contadj_ram_c.timeout   = 1600
    contadj_ram_c.tol       = 0.00001
    test_list.append(contadj_ram_c)

    ###################################
    ### Cont. adj. compressible N-S ###
    ###################################

    # Adjoint laminar cylinder
    contadj_ns_cylinder           = TestCase('contadj_ns_cylinder')
    contadj_ns_cylinder.cfg_dir   = "cont_adj_navierstokes/cylinder"
    contadj_ns_cylinder.cfg_file  = "lam_cylinder.cfg"
    contadj_ns_cylinder.test_iter = 100
    contadj_ns_cylinder.test_vals = [2.467226,-2.105465,0.555930,93.625000] #last 4 columns
    contadj_ns_cylinder.su2_exec  = "SU2_CFD"
    contadj_ns_cylinder.timeout   = 1600
    contadj_ns_cylinder.tol       = 0.00001
    test_list.append(contadj_ns_cylinder)

    # Adjoint laminar naca0012
    contadj_ns_naca0012           = TestCase('contadj_ns_naca0012')
    contadj_ns_naca0012.cfg_dir   = "cont_adj_navierstokes/naca0012"
    contadj_ns_naca0012.cfg_file  = "lam_NACA0012.cfg"
    contadj_ns_naca0012.test_iter = 100
    contadj_ns_naca0012.test_vals = [-0.012901,-5.322715,0.896630,-0.045627] #last 4 columns
    contadj_ns_naca0012.su2_exec  = "SU2_CFD"
    contadj_ns_naca0012.timeout   = 1600
    contadj_ns_naca0012.tol       = 0.00001
    test_list.append(contadj_ns_naca0012)

    #######################################################
    ### Cont. adj. compressible RANS (frozen viscosity) ###
    #######################################################

    # Adjoint turbulent NACA0012 (To be validated with finite differences)
    contadj_rans_naca0012           = TestCase('contadj_rans_naca0012')
    contadj_rans_naca0012.cfg_dir   = "cont_adj_rans/naca0012"
    contadj_rans_naca0012.cfg_file  = "turb_nasa.cfg"
    contadj_rans_naca0012.test_iter = 100
    contadj_rans_naca0012.test_vals = [-5.356749,-8.622049,18.310000,-0.000000] #last 4 columns
    contadj_rans_naca0012.su2_exec  = "SU2_CFD"
    contadj_rans_naca0012.timeout   = 1600
    contadj_rans_naca0012.tol       = 0.00001
    test_list.append(contadj_rans_naca0012)

    #######################################
    ### Cont. adj. incompressible Euler ###
    #######################################

    # Adjoint Incompressible Inviscid NACA0012
    contadj_incomp_NACA0012           = TestCase('contadj_incomp_NACA0012')
    contadj_incomp_NACA0012.cfg_dir   = "cont_adj_incomp_euler/naca0012"
    contadj_incomp_NACA0012.cfg_file  = "incomp_NACA0012.cfg"
    contadj_incomp_NACA0012.test_iter = 140
    contadj_incomp_NACA0012.test_vals = [-7.644867,-7.179288,0.011112,0.000000] #last 4 columns
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
    contadj_incomp_cylinder.test_vals = [-9.002576,-10.097248,0.048091,0.000000] #last 4 columns
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
    ramc.test_vals = [-4.638119,2.854417,-4.439634,0.000188]
    ramc.su2_exec  = "SU2_CFD"
    ramc.timeout   = 1600
    ramc.tol       = 0.00001
    test_list.append(ramc)

    ######################################
    ### Spectral Method                ###
    ######################################
    spectral           = TestCase('spectral')
    spectral.cfg_dir   = "spectral_method"
    spectral.cfg_file  = "spectral.cfg"
    spectral.test_iter = 25
    spectral.test_vals = [-1.621870,3.852164,0.007465,0.084358]
    spectral.su2_exec  = "SU2_CFD"
    spectral.timeout   = 1600
    spectral.tol       = 0.00001
    test_list.append(spectral)


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
