import numpy as np


def SENCTree(Data, CurtIndex, CurtHeight, Paras, alltraindatalabel):
    global flag1, id, pathline, pathline3
    flag1 = 0

    Tree = {}
    Tree['Height'] = CurtHeight
    NumInst = len(CurtIndex)

    if CurtHeight >= Paras['HeightLimit'] or NumInst <= 10:
        if NumInst > 1:
            Tree['NodeStatus'] = 0
            Tree['SplitAttribute'] = []
            Tree['SplitPoint'] = []
            Tree['LeftChild'] = []
            Tree['RightChild'] = []
            Tree['Size'] = NumInst
            Tree['CurtIndex'] = CurtIndex
            Tree['la'] = alltraindatalabel[CurtIndex, :]
            Tree['id'] = id
            id += 1
            Tree['center'] = np.mean(Data[CurtIndex, :], axis=0)
            Tree['dist'] = np.max(np.linalg.norm(Data[CurtIndex, :] - Tree['center'], axis=1))
            if NumInst != 1:
                c = 2 * (np.log(Tree['Size'] - 1) + 0.5772156649) - 2 * (Tree['Size'] - 1) / Tree['Size']
            else:
                c = 0

            Tree['high'] = CurtHeight + c
            pathline.append([Tree['high'], NumInst])
            pathline3[CurtIndex] = np.tile(Tree['high'], (1, NumInst))
        else:
            Tree['NodeStatus'] = 0
            Tree['SplitAttribute'] = []
            Tree['SplitPoint'] = []
            Tree['LeftChild'] = []
            Tree['RightChild'] = []
            Tree['Size'] = NumInst
            Tree['CurtIndex'] = CurtIndex
            Tree['la'] = alltraindatalabel[CurtIndex, :]
            if NumInst == 1:
                Tree['center'] = Data[CurtIndex, :]
            Tree['id'] = id
            id += 1
            flag1 = 1
            Tree['high'] = CurtHeight

        return Tree
    else:
        Tree['NodeStatus'] = 1
        # randomly select a split attribute
        rindex = np.random.randint(0, Paras['NumDim'])
        Tree['SplitAttribute'] = Paras['IndexDim'][rindex]
        print(Tree['SplitAttribute'])
        CurtData = Data[CurtIndex, Tree['SplitAttribute']]
        CurtDatalabel = alltraindatalabel[CurtIndex, :]
        Tree['SplitPoint'] = np.min(CurtData) + (np.max(CurtData) - np.min(CurtData)) * np.random.rand()
        # instance index for left child and right children
        LeftCurtIndex = CurtIndex[CurtData < Tree['SplitPoint']]
        RightCurtIndex = np.setdiff1d(CurtIndex, LeftCurtIndex)
        Tree['LeftCurtIndex'] = LeftCurtIndex
        Tree['LeftCurtIndexla'] = alltraindatalabel[LeftCurtIndex, :]
        Tree['RightCurtIndex'] = RightCurtIndex
        Tree['RightCurtIndexla'] = alltraindatalabel[RightCurtIndex, :]
        Tree['Size'] = NumInst
        # build right and left child trees
        Tree['LeftChild'] = SENCTree(Data, LeftCurtIndex, CurtHeight + 1, Paras, alltraindatalabel)
        if flag1 == 1:
            Tree['center'] = np.mean(Data[RightCurtIndex, :], axis=0)
            Tree['dist'] = np.max(np.linalg.norm(Data[RightCurtIndex, :] - Tree['center'], axis=1))
            Tree['la'] = alltraindatalabel[RightCurtIndex, :]
            flag1 = 0

        Tree['RightChild'] = SENCTree(Data, RightCurtIndex, CurtHeight + 1, Paras, alltraindatalabel)
        if flag1 == 1:
            Tree['center'] = np.mean(Data[LeftCurtIndex, :], axis=0)
            Tree['dist'] = np.max(np.linalg.norm(Data[LeftCurtIndex, :] - Tree['center'], axis=1))
            Tree['la'] = alltraindatalabel[LeftCurtIndex, :]
            flag1 = 0

        iTree = {'size': []}

    return Tree
