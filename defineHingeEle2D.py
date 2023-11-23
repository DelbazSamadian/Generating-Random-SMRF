from openseespy.opensees import *

def defineHingeEle2D (firstEleTag, iNode, jNode, ASec, Emat, I33, transfTag, firstZeroEleTag, firstNodeTag, rigidMatTag, hingeMatTag, nFac, crackFac, LOffsetRBS=0):
    Xi = nodeCoord(iNode, 1)
    Yi = nodeCoord(iNode, 2)
    Xj = nodeCoord(jNode, 1)
    Yj = nodeCoord(jNode, 2)
    
    LxEle = Xj-Xi
    LyEle = Yj-Yi
    
    if LxEle > 1e-6:
        dirEle = 1
    else:
        dirEle = 2
    
    if LOffsetRBS == 0:
        iiNode = firstNodeTag
        jjNode = firstNodeTag+1
        node(iiNode, Xi, Yi)
        node(jjNode, Xj, Yj)
        
        eleTag1 = firstZeroEleTag
        eleTag2 = firstZeroEleTag + 1
        element('zeroLength', eleTag1, iNode, iiNode, '-mat', rigidMatTag, rigidMatTag, hingeMatTag, '-dir', 1, 2, 3)
        element('zeroLength', eleTag2, jjNode, jNode, '-mat', rigidMatTag, rigidMatTag, hingeMatTag, '-dir', 1, 2, 3)
        
        eleTag = firstEleTag
        IMod = (nFac+1)/nFac*I33*crackFac
        element('elasticBeamColumn', eleTag, iiNode, jjNode, ASec, Emat, IMod, transfTag)
        
    else:
        iiNode = firstNodeTag
        iiiNode = firstNodeTag+1
        jjNode = firstNodeTag+2
        jjjNode = firstNodeTag+3
        node(iiNode, Xi+LOffsetRBS, Yi)
        node(iiiNode, Xi+LOffsetRBS, Yi)
        node(jjNode, Xj-LOffsetRBS, Yj)
        node(jjjNode, Xj-LOffsetRBS, Yj)
        
        eleTag1 = firstZeroEleTag
        eleTag2 = firstZeroEleTag + 1
        element('zeroLength', eleTag1, iiNode, iiiNode, '-mat', rigidMatTag, rigidMatTag, hingeMatTag, '-dir', 1, 2, 3)
        element('zeroLength', eleTag2, jjjNode, jjNode, '-mat', rigidMatTag, rigidMatTag, hingeMatTag, '-dir', 1, 2, 3)
        
        eleTagMid = firstEleTag
        eleTagLeft = firstEleTag+1
        eleTagRight = firstEleTag+2
        IMod = (nFac+1)/nFac*I33*crackFac
        element('elasticBeamColumn', eleTagMid, iiiNode, jjjNode, ASec, Emat, IMod, transfTag)
        element('elasticBeamColumn', eleTagLeft, iNode, iiNode, ASec, Emat, I33, transfTag)
        element('elasticBeamColumn', eleTagRight, jjNode, jNode, ASec, Emat, I33, transfTag)
    
    
    
    