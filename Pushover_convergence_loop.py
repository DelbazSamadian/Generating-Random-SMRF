from openseespy.opensees import *
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------------------------------
# Performance Based Earthquake Engineering Laboratory (PBEE Lab) (https://faculty.sites.uci.edu/pbee/)
# Department of Civil and Environmental Engineering
# University of California, Irvine
# Irvine, CA 92697
# ------------------------------------------------------------------------------------------------------------------------
# Original OpenseesTCL Model: Peyman Kaviani. 2010.
# Extended OpenseesTCL Model: Roshanak Omrani, Bahareh Mobasher. 2013.
# Modified and Extended OpenseesTCL Model: Jawad Fayaz. 2017 (https://jfayaz.github.io/)
# Converted OpenseesPY Model: Daniella Ginocchio and Jawad Fayaz. 2020. (https://jfayaz.github.io/)
# ------------------------------------------------------------------------------------------------------------------------
# Primary Citations:
# Jawad Fayaz, Mayssa Dabaghi, and Farzin Zareian (2020). "Utilization of Site-Based Simulated Ground Motions for Hazard-Targeted Seismic Demand Estimation: application for Ordinary Bridges in Southern California". ASCE- Journal of Bridge Engineering, Vol. 25, Issue 11
# ------------------------------------------------------------------------------------------------------------------------

# modelR   = direct+'/Results'
# modelDir = direct+ '/Model'
# exec(open(modelDir+'/CF1U_Model.py').read())

# print('PERFORMING PUSHOVER IN TRANSVERSE DIRECTION')


# #----------------maintain constant gravity loads and reset time to zero
# loadConst('-time', 0.0)

# modelR = directory+ '/Results'
# if not os.path.exists(modelR+'/PushOverTrans'):
#         os.mkdir(modelR+'/PushOverTrans')
# if not os.path.exists(modelR+'/PushOverTrans/'+str(skew)):
#         os.mkdir(modelR+'/PushOverTrans/'+str(skew))


# #Define RECORDERS
# recorder('Node', '-file', './Results/PushOverTrans/'+str(skew)+'/AbutNode100disp.txt', '-time', '-node', 100, '-dof', 1,2,3,4,5,6,'disp')
# recorder('Node', '-file', './Results/PushOverTrans/'+str(skew)+'/AbutNode110disp.txt', '-time', '-node', 110, '-dof', 1,2,3,4,5,6,'disp')
# recorder('Node', '-file', './Results/PushOverTrans/'+str(skew)+'/AbutNode115disp.txt', '-time', '-node', 115, '-dof', 1,2,3,4,5,6,'disp')
# recorder('Node', '-file', './Results/PushOverTrans/'+str(skew)+'/AbutNode120disp.txt', '-time', '-node', 120, '-dof', 1,2,3,4,5,6,'disp')
# recorder('Node', '-file', './Results/PushOverTrans/'+str(skew)+'/AbutNode130disp.txt', '-time', '-node', 130, '-dof', 1,2,3,4,5,6,'disp')

# recorder('Node', '-file', './Results/PushOverTrans/'+str(skew)+'/ColNode1012disp.txt', '-time', '-node', 1012, '-dof', 1,2,3,4,5,6,'disp')
# recorder('Node', '-file', './Results/PushOverTrans/'+str(skew)+'/ColNode2012disp.txt', '-time', '-node', 2012, '-dof', 1,2,3,4,5,6,'disp')
# recorder('Node', '-file', './Results/PushOverTrans/'+str(skew)+'/ColNode3012disp.txt', '-time', '-node', 3012, '-dof', 1,2,3,4,5,6,'disp')
# recorder('Node', '-file', './Results/PushOverTrans/'+str(skew)+'/ColNode1022disp.txt', '-time', '-node', 1022, '-dof', 1,2,3,4,5,6,'disp')
# recorder('Node', '-file', './Results/PushOverTrans/'+str(skew)+'/ColNode2022disp.txt', '-time', '-node', 2022, '-dof', 1,2,3,4,5,6,'disp')
# recorder('Node', '-file', './Results/PushOverTrans/'+str(skew)+'/ColNode3022disp.txt', '-time', '-node', 3022, '-dof', 1,2,3,4,5,6,'disp')

# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/ColEle1010force.txt', '-time', '-ele', 1010, 'globalForce')
# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/ColEle2010force.txt', '-time', '-ele', 2010, 'globalForce')
# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/ColEle3010force.txt', '-time', '-ele', 3010, 'globalForce')
# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/ColEle1020force.txt', '-time', '-ele', 1020, 'globalForce')
# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/ColEle2020force.txt', '-time', '-ele', 2020, 'globalForce')
# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/ColEle3020force.txt', '-time', '-ele', 3020, 'globalForce')


# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/SK1Spring907force.txt', '-time', '-ele', 907, 'force')
# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/SK1Spring908force.txt', '-time', '-ele', 908, 'force')
# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/SK4Spring909force.txt', '-time', '-ele', 909, 'force')
# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/SK4Spring910force.txt', '-time', '-ele', 910, 'force')

# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/SK1Spring907deform.txt', '-time', '-ele', 907, 'deformation')
# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/SK1Spring908deform.txt', '-time', '-ele', 908, 'deformation')
# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/SK4Spring909deform.txt', '-time', '-ele', 909, 'deformation')
# recorder('Element', '-file', './Results/PushOverTrans/'+str(skew)+'/SK4Spring910deform.txt', '-time', '-ele', 910, 'deformation')




# STATIC PUSHOVER ANALYSIS 
#
# Setting up parameters that are particular to the model.
IDctrlNode = roofNode
IDctrlDOF = 1
Dmax = targetDrift*HStructure
Dincr = incr

# # Creating load pattern for lateral pushover load
# Hload = 1
# tag3 = 200
# timeSeries('Linear', 29)
# pattern('Plain', tag3, 29)
# load(115, 0.0, -Hload, 0.0, 0.0, 0.0, 0.0)





# ----------- Set up Analysis Parameters  ---------- 


# CONSTRAINTS handler - Determines how the constraint equations are enforced in the analysis 
# Plain Constraints - Removes constrained degrees of freedom from the system of equations (only for homogeneous equations)
# Lagrange Multipliers - Uses the method of Lagrange multipliers to enforce constraints 
# Penalty Method - Uses penalty numbers to enforce constraints --good for static analysis with non-homogeneous eqns (rigidDiaphragm)
# Transformation Method - Performs a condensation of constrained degrees of freedom 
wipeAnalysis()
constraints('Transformation')


# DOF NUMBERER (number the degrees of freedom in the domain) - determines the mapping between equation numbers and degrees-of-freedom
# Plain - Uses the numbering provided by the user 
# RCM - Renumbers the DOF to minimize the matrix band-width using the Reverse Cuthill-McKee algorithm 
numberer('RCM')




# SYSTEM
# Linear Equation Solvers (how to store and solve the system of equations in the analysis) - provide the solution of the linear system of equations Ku = P. Each solver is tailored to a specific matrix topology. 
# ProfileSPD - Direct profile solver for symmetric positive definite matrices 
# BandGeneral - Direct solver for banded unsymmetric matrices 
# BandSPD - Direct solver for banded symmetric positive definite matrices 
# SparseGeneral - Direct solver for unsymmetric sparse matrices 
# SparseSPD - Direct solver for symmetric sparse matrices 
# UmfPack - Direct UmfPack solver for unsymmetric matrices 
system('BandGen')



# TEST: # convergence test to 
# Accept the current state of the domain as being on the converged solution path 
# determine if convergence has been achieved at the end of an iteration step
# NormUnbalance -- Specifies a tolerance on the norm of the unbalanced load at the current iteration 
# NormDispIncr -- Specifies a tolerance on the norm of the displacement increments at the current iteration 
# EnergyIncr-- Specifies a tolerance on the inner product of the unbalanced load and displacement increments at the current iteration
Tol = 1.e-5
maxNumIter = 5000
printFlag = 0
TestType = 'EnergyIncr'
test(TestType, Tol, maxNumIter, printFlag)

# Solution ALGORITHM: - Iterate from the last time step to the current 
# Linear - Uses the solution at the first iteration and continues 
# Newton - Uses the tangent at the current iteration to iterate to convergence 
# ModifiedNewton - Uses the tangent at the first iteration to iterate to convergence
algorithmType = 'KrylovNewton'
algorithm(algorithmType)



# Static INTEGRATOR: - determine the next time step for an analysis  
# LoadControl - Specifies the incremental load factor to be applied to the loads in the domain 
# DisplacementControl - Specifies the incremental displacement at a specified DOF in the domain 
# Minimum Unbalanced Displacement Norm - Specifies the incremental load factor such that the residual displacement norm in minimized 
# Arc Length - Specifies the incremental arc-length of the load-displacement path 
# Transient INTEGRATOR: - determine the next time step for an analysis including inertial effects 
# Newmark - The two parameter time-stepping method developed by Newmark 
# HHT - The three parameter Hilbert-Hughes-Taylor time-stepping method 
# Central Difference - Approximates velocity and acceleration by centered finite differences of displacement
integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)




# ANALYSIS - defines what type of analysis is to be performed (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/324.htm)
# Static Analysis - solves the KU=R problem, without the mass or damping matrices. 
# Transient Analysis - solves the time-dependent analysis. The time step in this type of analysis is constant. The time step in the output is also constant. 
# variableTransient Analysis - performs the same analysis type as the Transient Analysis object. The time step, however, is variable. This method is used when 
# There are convergence problems with the Transient Analysis object at a peak or when the time step is too small. The time step in the output is also variable.
analysis('Static')





#  ------------- Performing Static Pushover Analysis ----------------------
Nsteps = int(Dmax/Dincr)
ok = analyze(Nsteps)






# ---------------In case of convergence problems
if ok != 0:
    # change some analysis parameters to achieve covergence
    # performance is slower inside this loop
    ok = 0
    controlDisp = 0.0
    D0 = 0.0
    Dstep = (controlDisp-D0)/(Dmax-D0)
    while Dstep < 1.0 and ok == 0:
        controlDisp = nodeDisp(IDctrlNode, IDctrlDOF)
        Dstep = (controlDisp-D0)/(Dmax-D0)
        ok = analyze(1)
        if ok != 0:
            # print('Trying Newton with Initial Tangent...')
            test('NormDispIncr', Tol, 2000, 0)
            algorithm('Newton', '-initial')
            ok = analyze(1)
            test(TestType, Tol, maxNumIter, 0)
            algorithm(algorithmType)
            print('1: %f' , nodeDisp(roofNode, 1))
        
        # if ok != 0:
        #     algorithm('Broyden', 8)
        #     ok = analyze(1)
        #     algorithm(algorithmType)
        #     print('2: %f', nodeDisp(roofNode, 1))
            
        if ok != 0:
            algorithm('NewtonLineSearch', 0.8)
            ok = analyze(1)
            algorithm(algorithmType)
            print('3: %f', nodeDisp(roofNode, 1))
            
        if ok != 0:
            algorithm('NewtonLineSearch', '-Secant')
            ok = analyze(1)
            algorithm(algorithmType)
            print('4: %f', nodeDisp(roofNode, 1))
            
            
        if ok != 0:
            algorithm('NewtonLineSearch', '-Bisection')
            ok = analyze(1)
            algorithm(algorithmType)
            print('5: %f', nodeDisp(roofNode, 1))
            
        if ok != 0:
            algorithm('BFGS')
            ok = analyze(1)
            algorithm(algorithmType)
            print('6: %f', nodeDisp(roofNode, 1))
            
            
        # if ok != 0:
        #     print('Trying OS...')
        #     integrator('AlphaOS', 1.00)
        #     algorithm('Linear')
        #     ok = analyze(1)
        #     algorithm(algorithmType)
            
        if ok != 0:
            algorithm('NewtonLineSearch', '-RegulaFalsi')
            ok = analyze(1)
            algorithm(algorithmType)
            print('7: %f', nodeDisp(roofNode, 1))
            
        if ok != 0:
            algorithm('Newton')
            ok = analyze(1)
            algorithm(algorithmType)
            print('8: %f', nodeDisp(roofNode, 1))
            
        if ok != 0:
            algorithm('SecantNewton')
            ok = analyze(1)
            algorithm(algorithmType)
            print('9: %f', nodeDisp(roofNode, 1))
        
        if ok != 0:
            algorithm('RaphsonNewton')
            ok = analyze(1)
            algorithm(algorithmType)
            print('10: %f', nodeDisp(roofNode, 1))
            
        if ok != 0:
            algorithm('PeriodicNewton')
            ok = analyze(1)
            algorithm(algorithmType)
            print('11: %f', nodeDisp(roofNode, 1))
            
        if ok != 0:
            algorithm('NewtonLineSearch', '-RegulaFalsi')
            ok = analyze(1)
            algorithm('ModifiedNewton')
            print('12: %f', nodeDisp(roofNode, 1))
            
        if ok != 0:
            algorithm('KrylovNewton')
            ok = analyze(1)
            algorithm('ModifiedNewton')
            print('13: %f', nodeDisp(roofNode, 1))
            
        if ok != 0:
            algorithm('SecantNewton')
            ok = analyze(1)
            algorithm('ModifiedNewton')
            print('14: %f', nodeDisp(roofNode, 1))
        
          
      
        
        
            
            
        #end if ok !0
        
        
print('Pushover Done!')


