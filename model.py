# conventions:

# tag = [i][j][j][a][a]
    
# [a][a] for nodes:
# central nodes: 00
# main joint nodes: 01-04
# zeroLengh nodes for hinge beam      05-08
# zeroLengh nodes for hinge column    09,10
# additional joint nodes              11-18


# [a][a] for elements:
# beams:                        01-03
# columns:                      04
# zeroLengh for hinge beam      05,06
# zeroLengh for hinge column    07,08
# joint:                        10-21


from openseespy.opensees import *
import numpy as np
#import openseespy.postprocessing.Get_Rendering as opp
import math
from ISection import ISection
from defineHingeEle2D import defineHingeEle2D
from computeHingeRBSBeam import computeHingeRBSBeam
from computeHingeWColumn import computeHingeWColumn
from GuptaJointMat import GuptaJointMat
import os

#iModel = 5

wipe()
model('basic', '-ndm', 2)


exec(open('randomVariables/randomVariables(%d).py' % (iModel)).read())
exec(open('params.py').read())


if matType == 'steel':
    Emat = Es


nBay = len(LBayList)
nStory = len(HStoryList)

x = np.zeros(nBay+1)
for i in range(1, nBay+1):
    x[i] = x[i-1] + LBayList[i-1]

y = np.zeros(nStory+1)
for j in range(1, nStory+1):
    y[j] = y[j-1] + HStoryList[j-1]
    

# define nodes
for j in range(1,nStory+1):
    for i in range(nBay+1):
        
        if i < nBay:
            secName = beamSec[j-1,i]
            fileName = '%s/%s.py' % (sectionFolder, secName)
            exec(open(fileName).read())
            db = d
        
        secName = colSec[j-1,i]
        fileName = '%s/%s.py' % (sectionFolder, secName)
        exec(open(fileName).read())
        dc = d
        
        nd1 = int(i*1e4 + j*1e2 + 1)
        nd2 = int(i*1e4 + j*1e2 + 2)
        nd3 = int(i*1e4 + j*1e2 + 3)
        nd4 = int(i*1e4 + j*1e2 + 4)
        node(nd1, x[i], y[j]-db/2)
        node(nd2, x[i]+dc/2, y[j])
        node(nd3, x[i], y[j]+db/2)
        node(nd4, x[i]-dc/2, y[j])

roofNode = int(0*1e4 + nStory*1e2 + 3)
baseNode = int(0*1e4 + 0*1e2 + 3)


# define constraints
j = 0
for i in range(nBay+1):
    nodeTag = int(i*1e4 + j*1e2 + 3)
    node(nodeTag, x[i], y[j])
    
    if isBaseFixed:
        fix(nodeTag, 1, 1, 1)
    else:
        fix(nodeTag, 1, 1, 0)


# geometric transformation
transfTagBeam = 1
geomTransf('PDelta', transfTagBeam)

transfTagCol = 2
geomTransf('PDelta', transfTagCol)

transfTagRigid = 3
geomTransf('Linear', transfTagRigid)


# define materials
steelMatTag = 1
uniaxialMaterial('Steel02', steelMatTag, Fy, Emat, hardeningRatio, 15, 0.925, 0.15)

averageSec = colSec[0,0]
fileName = '%s/%s.py' % (sectionFolder, averageSec)
exec(open(fileName).read())
IAverage = I33
AAverage = ASec

rigidMatTag = 2
KRigid = 100*Emat*IAverage
uniaxialMaterial('Elastic', rigidMatTag, KRigid)

elasticMatTag = 3
uniaxialMaterial('Elastic', elasticMatTag, Emat)

# calculate Pg

PgMat = np.zeros([nStory,nBay+1])
for j in range(nStory):
    PgMat[j,:] = np.sum(nodalLoad[j:,:],axis=0)


# define sections
secId = 1
if beamType == 'fiber':
    beamSecId = np.zeros([nStory,nBay])
    for j in range(nStory):
        for i in range(nBay):
            secName = beamSec[j,i]
            fileName = '%s/%s.py' % (sectionFolder, secName)
            exec(open(fileName).read())
            ISection(secId, steelMatTag, d, tw, bf, tf, numSubdivWebL, numSubdivFlangeT)
            beamIntegration('Lobatto', secId, secId, numIntgrPts)
            beamSecId[j,i] = secId
            secId += 1

if colType == 'fiber':
    colSecId = np.zeros([nStory,nBay+1])
    for j in range(nStory):
        for i in range(nBay+1):
            secName = colSec[j,i]
            fileName = '%s/%s.py' % (sectionFolder, secName)
            exec(open(fileName).read())
            ISection(secId, steelMatTag, d, tw, bf, tf, numSubdivWebL, numSubdivFlangeT)
            beamIntegration('Lobatto', secId, secId, numIntgrPts)
            colSecId[j,i] = secId
            secId += 1

matId = 10
thetaPBeam = []
thetaPCBeam = []
asRatioBeam = []
if beamType == 'hinge':
    beamMatId = np.zeros([nStory,nBay])
    for j in range(1,nStory+1):
        for i in range(nBay):
            secName = beamSec[j-1,i]
            fileName = '%s/%s.py' % (sectionFolder, secName)
            exec(open(fileName).read())
            
            iNode = int(i*1e4 + j*1e2 + 2)
            jNode = int((i+1)*1e4 + j*1e2 + 4)
            Xi = nodeCoord(iNode, 1)
            Xj = nodeCoord(jNode, 1)
            
            aRBS = 0.625*bf;				# distance from face of column to start of RBS cut
            bRBS = 0.75*d;					# length of RBS cut
            cRBS = 0.25*bf; 				# depth of cut at center of RBS
            shRBS = aRBS+bRBS/2;  			# length from face of column to the center of RBS
            LRatio = 1.
            Lmem = abs(Xj-Xi)-2*shRBS
            # print('%d %d' % (j, i), end='  ')
            beamHingeParams = computeHingeRBSBeam (matId, d, tw, bf, tf, I33, Z33, R22, Lmem, LbBeam, Es, Fy, nFac, inchToCurrUnit, kipsToCurrUnit, isA992Gr50, cRBS, LRatio)
            if i == 0:
                thetaPBeam.append(beamHingeParams[0])
                thetaPCBeam.append(beamHingeParams[1])
                asRatioBeam.append(beamHingeParams[2])
                
            beamMatId[j-1,i] = matId
            matId += 1

thetaPExCol = []
thetaPCExCol = []
asRatioExCol = []
thetaPIntCol = []
thetaPCIntCol = []
asRatioIntCol = []

if colType == 'hinge':
    colMatId = np.zeros([nStory,nBay+1])
    for j in range(1,nStory+1):
        for i in range(nBay+1):
            secName = colSec[j-1,i]
            fileName = '%s/%s.py' % (sectionFolder, secName)
            exec(open(fileName).read())
            
            iNode = int(i*1e4 + (j-1)*1e2 + 3)
            jNode = int(i*1e4 + j*1e2 + 1)
            Yi = nodeCoord(iNode, 2)
            Yj = nodeCoord(jNode, 2)
            Lmem = abs(Yj-Yi)
            Pg = PgMat[j-1,i]
            # print('%d %d' % (j, i), end='  ')
            colHingeParams = computeHingeWColumn(matId, d, tw, bf, tf, I33, Z33, R22, Lmem, LbCol, Es, Fy, nFac, inchToCurrUnit, kipsToCurrUnit, isA992Gr50, ASec, Pg)
            if i == 0:
                thetaPExCol.append(colHingeParams[0])
                thetaPCExCol.append(colHingeParams[1])
                asRatioExCol.append(colHingeParams[2])
            elif i == 1:
                thetaPIntCol.append(colHingeParams[0])
                thetaPCIntCol.append(colHingeParams[1])
                asRatioIntCol.append(colHingeParams[2])
                    
            colMatId[j-1,i] = matId
            matId += 1


# define beams
for j in range(1,nStory+1):
    for i in range(nBay):
        eleTag = int(i*1e4 + j*1e2 + 1)
        iNode = int(i*1e4 + j*1e2 + 2)
        jNode = int((i+1)*1e4 + j*1e2 + 4)
        
        if beamType == 'elastic':
            secName = beamSec[j-1,i]
            fileName = '%s/%s.py' % (sectionFolder, secName)
            exec(open(fileName).read())
            element('elasticBeamColumn', eleTag, iNode, jNode, ASec, Emat, I33, transfTagBeam)
        
        elif beamType == 'fiber':
            secTag =  int(beamSecId[j-1,i])
            element('forceBeamColumn', eleTag, iNode, jNode, transfTagBeam, secTag)
        
        elif beamType == 'hinge':
            secName = beamSec[j-1,i]
            fileName = '%s/%s.py' % (sectionFolder, secName)
            exec(open(fileName).read())
            firstEleTag = eleTag
            firstZeroEleTag = int(i*1e4 + j*1e2 + 5)
            firstNodeTag = int(i*1e4 + j*1e2 + 5)
            hingeMatTag = int(beamMatId[j-1,i])
            LOffsetRBS = LOffsetRBSList[j-1]
            if matType == 'steel':
                crackFac = 1
            defineHingeEle2D (firstEleTag, iNode, jNode, ASec, Emat, I33, transfTagBeam, firstZeroEleTag, firstNodeTag, rigidMatTag, hingeMatTag, nFac, crackFac, LOffsetRBS)
            # element('elasticBeamColumn', eleTag, iNode, jNode, ASec, Emat, I33, transfTagBeam)

# define columns
for j in range(1,nStory+1):
    for i in range(nBay+1):
        eleTag = int(i*1e4 + j*1e2 + 4)
        iNode = int(i*1e4 + (j-1)*1e2 + 3)
        jNode = int(i*1e4 + j*1e2 + 1)
        
        if colType == 'elastic':
            secName = colSec[j-1,i]
            fileName = '%s/%s.py' % (sectionFolder, secName)
            exec(open(fileName).read())
            element('elasticBeamColumn', eleTag, iNode, jNode, ASec, Emat, I33, transfTagCol)
        
        elif colType == 'fiber':
            secTag =  int(colSecId[j-1,i])
            element('forceBeamColumn', eleTag, iNode, jNode, transfTagCol, secTag)
        
        elif colType == 'hinge':
            secName = colSec[j-1,i]
            fileName = '%s/%s.py' % (sectionFolder, secName)
            exec(open(fileName).read())
            firstEleTag = eleTag
            firstZeroEleTag = int(i*1e4 + j*1e2 + 7)
            firstNodeTag = int(i*1e4 + j*1e2 + 9)
            hingeMatTag = colMatId[j-1,i]
            LOffsetRBS = 0
            if matType == 'steel':
                crackFac = 1
            defineHingeEle2D (firstEleTag, iNode, jNode, ASec, Emat, I33, transfTagCol, firstZeroEleTag, firstNodeTag, rigidMatTag, hingeMatTag, nFac, crackFac, LOffsetRBS)

# define joints
jointMatId = np.zeros([nStory,nBay+1])
for j in range(1,nStory+1):
    for i in range(nBay+1):
        
        if isJointNonlinear:
            # beam
            if i < nBay:
                secName = beamSec[j-1,i]
                fileName = '%s/%s.py' % (sectionFolder, secName)
                exec(open(fileName).read())
                db = d
                tf_b = tf            
            
            # column
            secName = colSec[j-1,i]
            fileName = '%s/%s.py' % (sectionFolder, secName)
            exec(open(fileName).read())
            dc = d
            tp = tw
            bf_c = bf
            tf_c = tf
            ASecCol = ASec
            Pg = 0
            GuptaJointMat(matId, db, tf_b, dc, tp, bf_c, tf_c, ASecCol, Es, nus, Fy, Pg)
            jointMatId[j-1,i] = matId
            matId += 1
        else:
            jointMatId[j-1,i] = rigidMatTag
            
    
for j in range(1,nStory+1):
    for i in range(nBay+1):
        eleTag = int(i*1e4 + j*1e2 + 10)
        nd1 = int(i*1e4 + j*1e2 + 1)
        nd2 = int(i*1e4 + j*1e2 + 2)
        nd3 = int(i*1e4 + j*1e2 + 3)
        nd4 = int(i*1e4 + j*1e2 + 4)
        ndCenter = int(i*1e4 + j*1e2 + 0)
        element('Joint2D', eleTag, nd1, nd2, nd3, nd4, ndCenter, int(jointMatId[j-1,i]), 0)


# leaning columns
if hasLeaningCol:
    i = nBay+1
    
    # nodes
    xLeaning = x[nBay] + LBayList[0]
    for j in range(nStory+1):
        nodeTag = int(i*1e4 + j*1e2 + 0)
        node(nodeTag, xLeaning, y[j])
    
    # base node
    nodeTag = int(i*1e4 + 0*1e2 + 0)
    fix(nodeTag, 1, 1, 0)
    
    # columns
    for j in range(1,nStory+1):
        eleTag = int(i*1e4 + j*1e2 + 4)
        iNode = int(i*1e4 + (j-1)*1e2 + 0)
        jNode = int(i*1e4 + j*1e2 + 0)
        element('elasticBeamColumn', eleTag, iNode, jNode, AAverage*100, Emat, IAverage/100, transfTagCol)
    
    # rigid links
    for j in range(1,nStory+1):
        eleTag = int(i*1e4 + j*1e2 + 1)
        iNode = int((i-1)*1e4 + j*1e2 + 2)
        jNode = int(i*1e4 + j*1e2 + 0)
        element('Truss', eleTag, iNode, jNode, AAverage*100, elasticMatTag)
    
    # loads
    seriesTag = 1
    timeSeries('Linear', seriesTag) 
    pattern('Plain', 1, seriesTag)
    for j in range(1,nStory+1):
        if j == nStory:
            leaningLoad = leaningLoadRoof
        else:
            leaningLoad = leaningLoadFloor
        
        nodeTag = int(i*1e4 + j*1e2 + 0)
        load(nodeTag, 0, -leaningLoad, 0)
                


# define mass
for j in range(1,nStory+1):
    for i in range(nBay+1):
        nodeTag = int(i*1e4 + j*1e2 + 2)
        
        if j == nStory:
            nodalMass = roofMass/(nBay+1)        
        else:
            nodalMass = floorMass/(nBay+1)        
        
        mass(nodeTag, nodalMass, nodalMass, 1e-10)


# eigen analysis
pi = math.pi
omega2List = eigen(nModePeriod)        
i = 0
T = np.zeros(nModePeriod)
for omega2 in omega2List:
    omega = math.sqrt(omega2)
    T[i] = 2*pi/omega
    #print('T%d= %f' % (i+1, T[i]))
    i += 1

# # old version of postprocessing:
# opp.plot_model('node', 'element')

# gravity analysis
seriesTag = 2
timeSeries('Linear', seriesTag) 
pattern('Plain', 2, seriesTag)

# # elemental loads
# for j in range(1,nStory+1):
#     for i in range(nBay):
#         eleTag = int(i*1e4 + j*1e2 + 1)
#         if j == nStory:
#             beamLoad = roofBeamLoad
#         else:
#             beamLoad = floorBeamLoad
#         eleLoad('-ele', eleTag, '-type', '-beamUniform', -beamLoad)

# nodal loads
for j in range(1,nStory+1):
    for i in range(nBay+1):
        nodeTag = int(i*1e4 + j*1e2 + 3)
        load(nodeTag, 0, -nodalLoad[j-1,i], 0)

        
wipeAnalysis()
constraints('Transformation')
numberer('RCM')
system('BandSPD')
test('NormDispIncr', 1e-6, 100)
algorithm('Newton')
integrator('LoadControl', 0.1)
analysis('Static')
analyze(10)
loadConst('-time', 0)

modalDir = 'modalReport'
if not os.path.exists(modalDir):
    os.makedirs(modalDir)
modalProperties('-file', '%s/%d.txt' % (modalDir, iModel), '-unorm')
