import numpy as np
import time

from src.SENCForest.SENCTree import SENCTree


def SENCForest(Data, NumTree, NumSub, NumDim, rseed, label):
    global id, pathline3, pathline
    id = 1
    pathline3 = []
    pathline = []

    # Parametres
    Forest = {}
    Forest['NumTree'] = NumTree
    Forest['NumSub'] = NumSub
    Forest['NumDim'] = NumDim
    Forest['c'] = 2 * (np.log(NumSub - 1) + 0.5772156649) - 2 * (NumSub - 1) / NumSub
    Forest['rseed'] = rseed
    np.random.seed(rseed)
    NumInst, DimInst = Data.shape
    Forest['Trees'] = [None] * NumTree
    Forest['fruit'] = np.unique(label)
    Forest['HeightLimit'] = 200
    Paras = {}
    Paras['HeightLimit'] = Forest['HeightLimit']
    Paras['IndexDim'] = np.arange(1, DimInst + 1)
    Paras['NumDim'] = NumDim
    classindex = {}

    et = time.process_time()

    for j in range(Forest['fruit'].shape[0]):
        classindex[j] = np.where(label == Forest['fruit'][j])[0]

    IndexSub = []

    for i in range(NumTree):
        for j in range(Forest['fruit'].shape[0]):
            tempin = classindex[j]
            tempso = np.random.permutation(tempin.shape[0])
            if tempin.shape[0] < NumSub:
                print('Number of instances is too small.')
                break
            else:
                IndexSub = np.concatenate([IndexSub, tempin[tempso[:NumSub]]])

        pathline = []
        pathline3 = []
        Forest['Trees'][i] = SENCTree(Data, IndexSub, 0, Paras, label)
        Forest['Trees'][i]['totalid'] = id - 1
        Forest['Trees'][i]['pathline'] = pathline3
        Forest['Trees'][i]['pathline1'] = pathline
        tempan = np.sort(Forest['Trees'][i]['pathline1'][:, 0])

        varsf = np.zeros(tempan.shape[0])
        varsb = np.zeros(tempan.shape[0])
        vars_rate2 = np.zeros(tempan.shape[0])

        for j in range(tempan.shape[0]):
            varsf[j] = np.std(tempan[:j + 1])
            varsb[j] = np.std(tempan[j:])
            vars_rate2[j] = np.abs(varsf[j] - varsb[j])

        bb = np.argmin(vars_rate2)
        Forest['anomaly'][i] = tempan[bb]
        IndexSub = []
        id = 1

    Forest['ElapseTime'] = time.process_time() - et

    return Forest
