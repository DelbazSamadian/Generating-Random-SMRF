import numpy as np
import os
import math

# params
nCondition = 5 + 8 + 4
nCase = 10200
nTypeCol = 4
nTypeBeam = 2
nStory = 2
nBay = 3
colList = ['W21X44',	'W21X48',	'W21X50',	'W21X55',	'W21X57',	'W21X62',	'W21X68',	'W21X73',	'W21X83',	'W21X93',	'W21X101',	'W21X111', 'W24X94',	'W21X122', 'W24X103', 'W24X104',	'W21X132', 'W24X117',	'W21X147','W24X131','W21X166', 'W24X146', 'W21X182','W24X162', 'W21X201', 'W24X176', 'W24X192',	'W24X207',	'W24X229',	'W24X250',	'W24X279',	'W24X306',	'W24X335',	'W24X370', 'W27X336',	'W27X368',	'W27X539',]
beamList = ['W16X26',	'W16X31',	'W16X36',	'W16X40',	'W16X45',	'W16X50',	'W16X57',	'W16X67',	'W16X77',	'W16X89',	'W16X100',	'W21X44',	'W21X48',	'W21X50',	'W21X55',	'W21X57',	'W21X62',	'W21X68',	'W21X73',	'W21X83',	'W21X93',	'W21X101',	'W21X111',	'W21X122',	'W21X132',	'W21X147',	'W21X166',	'W21X182',	'W21X201',	'W24X55',	'W24X62',	'W24X68',	'W24X76',	'W24X84',	'W24X94',	'W27X84',	'W27X94',	'W27X102',	'W27X114',	'W27X129',	'W30X90',	'W30X99',	'W30X108',	'W30X116',	'W30X124',	'W30X132',	'W30X148',	'W30X173',	'W30X191',	'W30X211',	'W30X235',	'W30X261',	'W30X292',	'W30X326',	'W30X357',]


    
# generate random variables by given distribution
EsMean = 2.9e4*1.18
EsCov = 0.13
EsStd = EsMean*EsCov
EsMeanLog = 2*math.log(EsMean)-0.5*math.log(EsMean**2 + EsStd**2)
EsStdLog = math.sqrt(-2*math.log(EsMean) + math.log(EsMean**2 + EsStd**2))

FyMean = 50*1.18
FyCov = 0.13
FyStd = FyCov*FyMean
FyMeanLog = 2*math.log(FyMean)-0.5*math.log(FyMean**2 + FyStd**2)
FyStdLog = math.sqrt(-2*math.log(FyMean) + math.log(FyMean**2 + FyStd**2))

HStoryMin = 0.75*156
HStoryMax = 1.25*156


LBayRatioMin = 1.25
LBayRatioMax = 2

massMean = 2.07263*1.05
massCov = 0.1

EsList = np.random.lognormal(EsMeanLog, EsStdLog, nCase) 
FyList = np.random.lognormal(FyMeanLog, FyStdLog, nCase)
HStoryList = np.random.uniform(HStoryMin, HStoryMax, nCase)
LBayRatioList = np.random.uniform(LBayRatioMin, LBayRatioMax, nCase)
massList = np.random.normal(massMean, massCov*massMean, nCase) 
LBayList = LBayRatioList*HStoryList*1.154

# code
nColList = len(colList)
nBeamList = len(beamList)
colSecList = np.zeros([nCase,nTypeCol])
beamSecList = np.zeros([nCase,nTypeBeam])
I33Beam = np.zeros([nStory])
Z33Beam= np.zeros([nStory])
I33Col = np.zeros([nStory,nBay+1])
Z33Col = np.zeros([nStory,nBay+1])
beamNames = np.zeros([nStory], dtype=object)
colNames = np.zeros([nStory,nBay+1], dtype=object)

if not os.path.exists('randomVariables'):
    os.makedirs('randomVariables')

iCase = 0
iIter = 0
while (1):
    
    i = 0
    conditions = np.zeros([nCondition])
    colSecIndex = np.random.randint(nColList, size=(nTypeCol))
    beamSecIndex = np.random.randint(nBeamList, size=(nTypeBeam))
    
    # -------------------------
    # check columns
    # -------------------------
    for j in range(nStory):
        if colSecIndex[int(j*2+1)] >= colSecIndex[int(j*2)]:
            conditions[i] = 1
        i += 1  
        
        if j < nStory-1:
            if colSecIndex[int(j*2)] >= colSecIndex[int(j*2+2)]:
                conditions[i] = 1
            i += 1  
                
            if colSecIndex[int(j*2+1)] >= colSecIndex[int(j*2+3)]:
                conditions[i] = 1
            i += 1  
    
    # -------------------------
    # check beams
    # -------------------------
    for j in range(nStory-1):
        if beamSecIndex[j] >= beamSecIndex[j+1]:
            conditions[i] = 1
    
    # check if conditions satisfied till here
    satisfied = 1
    for ii in range(i+1):
        if conditions[ii] == 0:
            satisfied = 0
            break
    
    if satisfied == 0:
        continue
    
    i += 1  
    
    # -------------------------
    # check weak-beam and strong-column
    # -------------------------
    
    for j in range(nStory):
        # beams
        beamIndex = beamSecIndex[j]
        secName = beamList[beamIndex]
        fileName = 'sections/%s.py' % (secName)
        exec(open(fileName).read())
        I33Beam[j] = I33
        Z33Beam[j]= Z33
        beamNames[j] = secName
        
        # columns
        colIndex = colSecIndex[int(j*2)]
        secNameOuter = colList[colIndex]
        fileName = 'sections/%s.py' % (secNameOuter)
        exec(open(fileName).read())
        I33Outer = I33
        Z33Outer = Z33
        
        colIndex = colSecIndex[int(j*2+1)]
        secNameInner = colList[colIndex]
        fileName = 'sections/%s.py' % (secNameInner)
        exec(open(fileName).read())
        I33Inner = I33
        Z33Inner = Z33
        
        for ii in range(nBay+1):
            
            if ii == 0 or ii == nBay:
                I33Col[j,ii] = I33Outer
                Z33Col[j,ii] = Z33Outer
                colNames[j,ii] = secNameOuter
            else:
                I33Col[j,ii] = I33Inner
                Z33Col[j,ii] = Z33Inner
                colNames[j,ii] = secNameInner
                
    
    # iterate on each joint
    for j in range(nStory):
        for ii in range(nBay+1):
            if j == nStory-1:
                if ii == 0 or ii == nBay:
                    sumI33Col = I33Col[j,ii]
                    sumI33Beam = I33Beam[j]
                else:
                    sumI33Col = I33Col[j,ii]
                    sumI33Beam = 2*I33Beam[j]
            else:
                if ii == 0 or ii == nBay:
                    sumI33Col = I33Col[j,ii] + I33Col[j+1,ii]
                    sumI33Beam = I33Beam[j]
                else:
                    sumI33Col = I33Col[j,ii] + I33Col[j+1,ii]
                    sumI33Beam = 2*I33Beam[j]
            
            if sumI33Col >= sumI33Beam:
                conditions[i] = 1
            i += 1
    # -------------------------
    # check practically criteria
    # -------------------------
            
    for j in range(nStory):
        if 0.6<=I33Col[j,0]/I33Col[j,1]<=0.8:
            conditions[i] = 1
        i += 1
    for j in range(nStory):
        if 0.45<=Z33Beam[j]/Z33Col[j,1]<=0.8:
            conditions[i] = 1
        i += 1 
        
            
    
    
    if conditions.all() == 1:
        colSecList[iCase,:] = colSecIndex
        beamSecList[iCase,:] = beamSecIndex
        
        fileId = open('randomVariables/randomVariables(%d).py' % (iCase+1),'w')
        fileId.write('import numpy as np\n\n')
        
        # beams
        fileId.write('beamSec = np.array([ \n')
        for j in range(nStory):
            secName = str(beamNames[j])
            fileId.write("\t['%s', '%s', '%s'],\n" % (secName, secName, secName))
        fileId.write('])\n\n')
        
        # columns
        fileId.write('colSec = np.array([ \n')
        for j in range(nStory):
            fileId.write('\t[')
            for ii in range(nBay+1):
                secName = str(colNames[j,ii])
                fileId.write("'%s', " % (secName))
            fileId.write('],\n')
        fileId.write('])\n\n')
        
        # other variables
        fileId.write('HStory = %.2f\n' % (HStoryList[iCase]))
        fileId.write('LBay = %.2f\n' % (LBayList[iCase]))
        fileId.write('Es = %.2f\n' % (EsList[iCase]))
        fileId.write('Fy = %.2f\n' % (FyList[iCase]))
        fileId.write('massValue = %.5f\n' % (massList[iCase]))
        
        
        fileId.close()
        
        iCase += 1
    
    if iCase == nCase:
        break
    
    iIter += 1
    





