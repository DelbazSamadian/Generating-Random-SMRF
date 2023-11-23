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

from openseespy.opensees import *

def GuptaJointMat(matTag, db, tf_b, dc, tp, bf_c, tf_c, ASecCol, Es, nus, Fy, Pg):
    # uniaxialMaterial('Elastic', matTag, KRigid)
    # calculate Vy and Vp
    Py = ASecCol*Fy
    Pr = Pg
    
    Vy = 0.6*Fy*dc*tp
    if Pr <=(0.4*Py) :
        Vy = Vy
    else :
        Vy = Vy*(1.4-(Pr/Py))
    Vp = 0.6*Fy*dc*tp*(1.+3.*bf_c*tf_c**2/(db*dc*tp))
    if Pr <=(0.75*Py) :
        Vp = Vp
    else :
        Vp = Vp*(1.9-(1.2*Pr/Py))
    # calculate gamma and M
    
    G = Es/(2.*(1.+nus))
    Apz = tp*dc
    Ke = G*Apz
	
    gammaY= Vy/Ke
    My = Vy*(db-tf_b)
	
    gammaP = 4.0*gammaY
    Mp = Vp*(db-tf_b)
    
    gammaU = 100.0*gammaY
    as0 =  0.02
    Vu = Vp + as0*Ke*(gammaU-gammaP)
    Mu = Vu*(db-tf_b)
    
    uniaxialMaterial('Hysteretic',matTag, My, gammaY, Mp,gammaP, Mu, gammaU, -My, -gammaY, -Mp, -gammaP, -Mu, -gammaU, 1, 1, 0., 0., 0.)

