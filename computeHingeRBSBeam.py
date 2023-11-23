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

# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 19:34:20 2021

@author: Dear User

"""
from openseespy.opensees import *
# parameters:
# parameters:
# ry: radius of gyration in the weak-axis
# Lb: unbraced length
# inchToCurrUnit: coefficient to convert inch to other units
# ksiToCurrUnit: coefficient to convert ksi to other units

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

def computeHingeRBSBeam (matTag, d, tw, bf, tf, ISec, ZSec, ry, Lmem, Lb, Es, Fy, nFac, inchToCurrUnit, kipsToCurrUnit, isA992Gr50, cRBS, LRatio) :
    
    ksiToCurrUnit = kipsToCurrUnit/(inchToCurrUnit**2)
    # calculate thetaP, thetaPC and lambda
    hw	= d-(2.0*tf)
    LShear =  Lmem/2.0
    L 	= LShear
    if isA992Gr50 == 1 :
         thetaP	= 0.09  *  (hw/tw)**-0.3  *  (bf/tf/2.0)**-0.1  *  (L/d)**0.1  *  (d/21./inchToCurrUnit)**-0.8
         thetaP =  thetaP/LRatio
         thetaPC =	 6.5  *  (hw/tw)**-0.5  *  (bf/tf/2.0)**-0.9
         thetaPC =  thetaPC/LRatio
         Lambda = 49.0  *  (hw/tw)**-1.14  *  (bf/tf/2.0)**-0.632  *  (Lb/ry)**-0.205  *  (Es/Fy)**0.391
    else :
        thetaP	=  0.19 * (hw/tw)**-0.314  *  (bf/tf/2.0)**-0.1  *  (Lb/ry)**-0.1185  *  (L/d)**0.113  *  (d/21./inchToCurrUnit)**-0.76  *  (Fy/50.0/ksiToCurrUnit)**-0.07
        thetaP  =  thetaP/LRatio
        thetaPC	= 9.62  *  (hw/tw)**-0.513  *  (bf/tf/2.0)**-0.863  *  (Lb/ry)**-0.108  *  (Fy/50.0/ksiToCurrUnit)**-0.36
        thetaPC = thetaPC/LRatio
        Lambda = 592.0  *  (hw/tw)**-1.138  *  (bf/tf/2.0)**-0.632  * (Lb/ry)**-0.205 *  (Fy/50.0/ksiToCurrUnit)**-0.391
    # calculate effective yield moment(My)
    beta = 1.1
    ZRBS = ZSec-(2.0*cRBS*tf*(d-tf))
    Myp	 = ZRBS*Fy
    My	=  LRatio*beta*Myp
    
    # define peak moment (Mu) to effective yield moment (My) ratio
    
    MuMyFac	=	1.1
    
   	# define some parameters

    c	=	1.0
    D=	1.0
    
    KResidual=	0.4
    thetaU = 0.2/LRatio
    
    # calculate member stiffness and strain hardening coefficient
    ke = 6.0*Es*(ISec/Lmem)
    asRatio = My*((MuMyFac-1)/(ke*thetaP))
    
	# define bilin material
    uniaxialMaterial('Bilin', matTag, ke, asRatio, asRatio, My, -My, Lambda, Lambda, 10000, Lambda, c, c, c, c, thetaP, thetaP, thetaPC, thetaPC, KResidual, KResidual, thetaU, thetaU, D, D, nFac)
    return thetaP, thetaPC, asRatio

# d = 
# bf = 15.0
# tf = 1.07
# hw = 28.259999999999998
# tw = 0.655
# Radius = 0.78
# ASec = 50.9
# AS2 = 19.91
# AS3 = 26.75
# J = 15.6
# I22 = 598.0
# I33 = 8230.0
# S22 = 79.73
# S33 = 541.45
# Z22 = 123.0
# Z33 = 607.0
# R22 = 3.4276
# R33 = 12.7157


    
# matTag =10
# d =30.4
# tw =0.655
# bf =15.0
# tf =1.07
# ISec = 8230.0
# ZSec  =607.0
# ry  =3.4276
# Lmem = 5.4777000000000005
# Lb =2.0
# Es =2.0e11
# Fy =345.0e6
# nFac = 10.0
# inchToCurrUnit = 0.0254
# kipsToCurrUnit = 4448.2216
# isA992Gr50 =  1
# cRBS= 0.052700000000000004
# LRatio = 1.1387380270563838

# computeHingeRBSBeam(matTag, d, tw, bf, tf, ISec, ZSec, ry, Lmem, Lb, Es, Fy, nFac, inchToCurrUnit, kipsToCurrUnit, isA992Gr50, cRBS, LRatio)

