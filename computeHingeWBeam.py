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


def computeHingeWBeam(matTag, d, tw, bf, tf, I33, Z33, R22, Lmem, Lb, Es, Fy, nFac, inchToCurrUnit, kipsToCurrUnit, isA992Gr50,fileId):
    

    ksiToCurrUnit = kipsToCurrUnit/inchToCurrUnit**2
    
    # calculate thetaP, thetaPC and lambda
    hw = d-2*tf
    LShear = Lmem/2
    L = LShear
    # 
    if isA992Gr50:
        thetaP = 0.07 * (hw/tw)**-0.3 * (bf/tf/2)**-0.1 * (L/d)**0.3 * (d/21/inchToCurrUnit)**-0.7
        thetaPC = 4.6 * (hw/tw)**-0.5 * (bf/tf/2)**-0.8 * (d/21/inchToCurrUnit)**-0.3
        Lambda = 85 * (hw/tw)**-1.26 * (bf/tf/2)**-0.525 * (Lb/R22)**-0.13 * (Es/Fy)**0.291
    else:
        thetaP = 0.087 * (hw/tw)**-0.365 * (bf/tf/2)**-0.14 * (L/d)**0.34 * (d/21/inchToCurrUnit)**-0.721 * (Fy/50/ksiToCurrUnit)
        thetaPC = 4.6 * (hw/tw)**-0.5 * (bf/tf/2)**-0.8 * (d/21/inchToCurrUnit)**-0.3
        Lambda = 85 * (hw/tw)**-1.26 * (bf/tf/2)**-0.525 * (Lb/R22)**-0.13 * (Es/Fy)**0.291
        
	# calculate effective yield moment(My)
    beta = 1.2
    Myp = Z33*Fy
    My = beta*Myp
    
	# define peak moment (Mu) to effective yield moment (My) ratio
    MuMyFac = 1.1
    
	# define some parameters
    c = 1
    D = 1
    KResidual = 0.4
    thetaU = 0.2
    
	# calculate member stiffness and strain hardening coefficient
    ke = 6*Es*I33/Lmem
    # print(Es,I33,Lmem)
    asRatio = My*(MuMyFac-1)/(ke*thetaP)
    # print('Bilin', matTag, ke, asRatio, asRatio, My, -My, Lambda, Lambda, 10000, Lambda, c, c, c, c, thetaP, thetaP, thetaPC, thetaPC, KResidual, KResidual, thetaU, thetaU, D, D, nFac)
    uniaxialMaterial('Bilin', matTag, ke, asRatio, asRatio, My, -My, Lambda, Lambda, 10000, Lambda, c, c, c, c, thetaP, thetaP, thetaPC, thetaPC, KResidual, KResidual, thetaU, thetaU, D, D, nFac)
    fileId.write("uniaxialMaterial('Bilin', %d, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f,%.3f, %.3f, %.3f, %.3f, %.3f , %.3f , %.3f , %.3f, %.3f, %.3f)\n" % (matTag, ke, asRatio, asRatio, My, -My, Lambda, Lambda, 10000, Lambda, c, c, c, c, thetaP, thetaP, thetaPC, thetaPC, KResidual, KResidual, thetaU, thetaU, D, D, nFac))