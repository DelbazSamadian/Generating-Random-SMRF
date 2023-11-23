# #########################################################
# This code is part of an OpenSees course and could be
# used for research purpose, however using this code 
# without purchasing the course is forbidden.
#
# developed by:
# 				Hadi Eslamnia
# 				Amirkabir University of Technology
# 
# contact us:
# 				Website: 			eslamnia.com
# 				Instagram: 			@eslamnia.ir
#				Telegram channel:	@eslamnia
# 				WhatsApp: 			+989101858874
# #########################################################

# parameters:
# R22: radius of gyration in the weak-axis
# Lb: unbraced length
# cUnitL: coefficient to convert inch to other units
# cUnitFy: coefficient to convert ksi to other units

# if length unit is:
# inch  >> inchToCurrUnit = 1.
# meter >> inchToCurrUnit = 0.0254
# cm    >> inchToCurrUnit = 2.54
# mm    >> inchToCurrUnit = 25.4

# if Fy unit is:
# ksi  			>> ksiToCurrUnit = 1.
# N/m2			>> ksiToCurrUnit = 6894757.
# N/mm2 (MPa) 	>> ksiToCurrUnit = 6.894757
# kgf/cm2     	>> ksiToCurrUnit = 70.30696

from openseespy.opensees import *


def computeHingeWColumn(matTag, d, tw, bf, tf, I33, Z33, R22, Lmem, Lb, Es, Fy, nFac, inchToCurrUnit, kipsToCurrUnit, isA992Gr50, ASec, Pg):
    

    ksiToCurrUnit = kipsToCurrUnit/inchToCurrUnit**2
    
    # calculate thetaP, thetaPC and lambda
    hw = d-2*tf
    LShear = Lmem/2
    L = LShear
    Pg = abs(Pg)
    Py = Fy*ASec
    
    thetaP = min((294 * (hw/tw)**-1.7 * (Lb/R22)**-0.7 * (1-Pg/Py)**1.6) , 0.2)
    thetaPC = min((90 * (hw/tw)**-0.8 * (Lb/R22)**-0.8 * (1-Pg/Py)**2.5) , 0.3)
    
    if isA992Gr50:
        Lambda = 85 * (hw/tw)**-1.26 * (bf/tf/2)**-0.525 * (Lb/R22)**-0.13 * (Es/Fy)**0.291
    else:
        Lambda = 500 * (hw/tw)**-1.34 * (bf/tf/2)**-0.595 * (Fy/50/ksiToCurrUnit)**-0.36
    
    if Pg/Py > 0.6:
        print('Warning: Pg/Pye > 0.6: current hinge model for columns may not be suitable')
        print('columns need to be treated as force-controlled elements')
        print('see computeHingeWColumn.tcl file and ASCE/SEI 41-17')
    
    
 	# calculate effective yield moment(My)
    beta = 1.2
    Myp = Z33*Fy
    My = beta*Myp
    
 	# calculate effective yield moment reduced by the applied load (My)
 	# it is showed by My* in the references
    if Pg/Py <= 0.2:
        My = 1.15*Z33*Fy*(1-Pg/Py)
    else:
        My = 1.15*Z33*Fy*(9/8)*(1-Pg/Py)
    
    
 	# calculate peak moment (Mu) to effective yield moment (My) ratio
    alpha = 12.5 * (hw/tw)**-0.2 * (Lb/R22)**-0.4 * (1-Pg/Py)**0.4  
    if alpha < 1:
        alpha = 1
    elif alpha > 1.3:
        alpha = 1.3
    
    MuMyFac = alpha
 	# define some parameters
    c = 1
    D = 1
    KResidual = 0.5-0.4*Pg/Py
    thetaU = 0.15
    
 	# calculate member stiffness and strain hardening coefficient
    ke = 6*Es*I33/Lmem
    asRatio = My*(MuMyFac-1)/(ke*thetaP)
    
    # print(My, ke)
    
    # print('Bilin', matTag, ke, asRatio, asRatio, My, -My, Lambda, Lambda, 10000, Lambda, c, c, c, c, thetaP, thetaP, thetaPC, thetaPC, KResidual, KResidual, thetaU, thetaU, D, D, nFac)
    uniaxialMaterial('Bilin', matTag, ke, asRatio, asRatio, My, -My, Lambda, Lambda, 10000, Lambda, c, c, c, c, thetaP, thetaP, thetaPC, thetaPC, KResidual, KResidual, thetaU, thetaU, D, D, nFac)
    return thetaP, thetaPC, asRatio
    