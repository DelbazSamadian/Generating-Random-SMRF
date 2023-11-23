import numpy as np


# variables
# HStory = 156
# LBay = 240

# params
# units: Kips, inch



HStoryList = [1.154*HStory, HStory]
LBayList = [LBay, LBay, LBay]

sectionFolder = 'sections'

# # first row belongs to the first floor
# beamSec = np.array([
    # ['W30x132', 'W30x132','W30x132'],
    # ['W16x31', 'W16x31','W16x31'],
# ])

# colSec = np.array([
    # ['W24x131', 'W24x162','W24x162','W24x131'],
    # ['W24x131', 'W24x162','W24x162','W24x131'],
# ])


beamType = 'hinge';   # elastic, fiber, hinge
colType = 'hinge';   # elastic, fiber, hinge
matType = 'steel';     # steel, concrete

# steel material
# Fy = 50
# Es = 2.9000e+04
nus = 0.3
hardeningRatio = 0.01

# fiber section
numSubdivWebL = 10
numSubdivFlangeT = 2
numIntgrPts = 5

# hinge model
nFac = 10
# first elements belongs to first story
LOffsetRBSList = [17.925, 9.419]
LbBeam = 50
LbCol = HStory
inchToCurrUnit = 1
kipsToCurrUnit = 1
isA992Gr50 = 1


isJointNonlinear = 1

# loads and mass
# floorBeamLoad = 1000
# roofBeamLoad = 800

g = 386.2
# massValue = 2.07263
roofMass = 0.9*massValue
floorMass = massValue

nodalLoad = np.array([
    [70.21, 0, 0, 70.21],
    [61.77, 0, 0, 61.77],
], dtype = float)


hasLeaningCol = 1
leaningLoadRoof = 511.2
leaningLoadFloor = 568

nModePeriod = 3
isBaseFixed = 0