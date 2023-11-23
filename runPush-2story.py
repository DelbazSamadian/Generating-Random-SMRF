from openseespy.opensees import *
import os
import numpy as np
import matplotlib.pyplot as plt
# import vfo.vfo as vfo
import glob
import pandas as pd
import glob
firstModel = 1
lastModel = 10200
for iModel in range(firstModel,lastModel+1):
    
    #print('model= %d is running ...' % (iModel))
    
    exec(open('model.py').read())
    
#     # # # old version
#     # # modelName = '2DFrame'
#     # # loadCaseName = 'pushover'
#     # # opp.createODB(modelName, loadCaseName)
#     # # # ----------------
    
    dataDir = 'outputs/pushover-all'
    
    if not os.path.exists(dataDir):
        os.makedirs(dataDir)
    
    
    recorder('Node', '-file', dataDir + '/V-Disp%s.txt' %(iModel), '-time', '-node', roofNode, '-dof', 1, 'disp')
    
    seriesTag = 3
    timeSeries('Linear', seriesTag) 
    pattern('Plain', 3, seriesTag)
    zigmaF = nStory*(nStory+1)/2*(nBay+1)
    for j in range(1,nStory+1):
        for i in range(nBay+1):
            nodeTag = int(i*1e4 + j*1e2 + 3)
            load(nodeTag, j/zigmaF, 0, 0)
#             # print(j/zigmaF)
    
    targetDrift = 0.05
    HStructure = y[nStory]
    incr = 0.005
    
    
#     # # deltaTarget = targetDrift*HStructure
#     # # nStep = int(deltaTarget/incr)
#     # # wipeAnalysis()
#     # # constraints('Transformation')
#     # # numberer('RCM')
#     # # system('BandSPD')
#     # # test('NormDispIncr', 1e-6, 100)
#     # # algorithm('KrylovNewton')
#     # # integrator('DisplacementControl', roofNode, 1, incr)
#     # # analysis('Static')
#     # # analyze(nStep)
#     # # wipe()
    
    exec(open('Pushover_convergence_loop.py').read())
    wipe()
    
    
#     # # dataPath = dataDir + '/V-Disp.txt'
#     # # data = np.loadtxt(dataPath)
#     # # indexNeg = np.where(data[:,0] <= 0)[0]
#     # # Negative = indexNeg[:1]
#     # # #K= int(Negative)
#     # # if not Negative:
#     # #     lk=data[0:,1]
#     # #     mk=data[:,0]
#     # # else:
#     # #     lk=data[0:int(Negative),1]
#     #     mk=data[0:int(Negative),0]
   
#os.chdir('outputs/pushover-all')
# gghhh=np.zeros([5000,2])
# filenames =glob.glob("*.txt")
filenames = []
for iModel in range(firstModel,lastModel+1):
    name = 'outputs/pushover-all/V-Disp%s.txt' % (iModel)
    filenames.append(name)


df = [pd.read_csv(file, sep = " ", header=None,) 
      for file in filenames]

# filenames = [i for i in glob.glob(f"*.txt")]
# df = [pd.read_csv(file, sep = " ", header=None,) 
#       for file in filenames]

# indexNeg = np.where(df[1].loc[:,0] < 0)[0]
# Negative = indexNeg[:1]
# for ii in range(8000):
#     indexNeg = np.where(df[ii].loc[:,0] < 0)[0]
#     # firstNegIndex = indexNeg[:1]
#     # indexNeg2= np.where(df[ii].loc[:,1] < 0)[0]
#     # Negative2=indexNeg[:1]
#     #K= int(Negative)
#     if np.size(indexNeg) == 0:
#         plt.plot(df[ii].loc[:,1]/HStructure, df[ii].loc[:,0],label='Building %d' %(ii+1))
#         #plt.legend()
#     else:
#         plt.plot(df[ii].loc[0:int(Negative),1]/HStructure, df[ii].loc[0:int(Negative),0],label='Building %d' %(ii+1))
        
     
#     # plt.legend()
#     plt.xlabel('Drift values')
#     plt.ylabel('Base shear values')
#     plt.title('V-Disp')
#     plt.xlim(0, 0.10)
#     plt.ylim(0, 1000)


#lk=data[0:,1]
#     mk=data[:,0]
# else:
#     lk=data[0:int(Negative),1]
#     mk=data[0:int(Negative),0]

# #deli=df[2].loc[:,0]
# #delbaz1=delbaz.loc[:,0]
# #plt.plot(df[0][1], df[1][0]) 
# #plt.plot(df[2].loc[:,1], df[2].loc[:,0])
# for i in range(lastModel):
#     plt.plot(df[i].loc[:,1], df[i].loc[:,0],label='Building %d' %(i+1))
#     plt.plot(df[i+1].loc[:,1], df[i+1].loc[:,0],label='Building %d' %(i+2))
#     plt.legend()
#     # plt.plot(df[0][2])
#     plt.show()
    
# plt.plot(df[1].loc[:,1], df[1].loc[:,0],label='First Line')
# plt.plot(df[0].loc[:,1], df[0].loc[:,0],label='second Line') 

    
    
    # plt.figure()    
    # plt.plot(finalpush[1][:], finalpush[0][:])
    
        # K= int(Negative)
     # if not Negative:
     #     plt.figure()    
     #     plt.plot(data[0:,1], data[:,0])
     # else:
     #     plt.figure()      
     #     plt.plot(data[0:int(Negative),1], data[0:int(Negative),0])        
    # plt.xlabel('Displacement values')
    # plt.ylabel('Base shear values')
    # plt.title('V-Disp')
    # plt.legend(['V-Disp'])
    # if not os.path.exists('outputs/pushoverfigures'):
    #     os.makedirs('outputs/pushoverfigures')
    # plt.savefig('outputs/pushoverfigures/Building%d.png' %(iModel))


    
    
    
    # # old version of postprocessing:
    # opp.animate_deformedshape(Model=modelName, LoadCase= loadCaseName, dt=0.01)
    
    


