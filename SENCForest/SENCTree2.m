function Tree = SENCTree2(Data, CurtIndex, CurtHeight, Paras,alltraindatalabel,newlabel)
global flag1 id2 pathline pathline3 pathline4 pathline5 rt
flag1=0;

Tree.Height = CurtHeight;
NumInst = length(CurtIndex);

%    if CurtHeight >= Paras.HeightLimit || NumInst <= 10
if  NumInst <= 10 || CurtHeight >= rt %%Paras.HeightLimit
    if NumInst  > 1
        Tree.NodeStatus = 0;
        Tree.SplitAttribute = [];
        Tree.SplitPoint = [];
        Tree.LeftChild = [];
        Tree.RightChild = [];
        Tree.Size = NumInst;
        Tree.CurtIndex=CurtIndex;
        Tree.la=alltraindatalabel(CurtIndex,:);
        Tree.id=id2;
        id2=id2+1;
        C = mean(Data(CurtIndex,:),1);
        Tree.dist=max(pdist2(Data(CurtIndex,:),C));
        Tree.center=C;
        if NumInst~=1
            c = 2 * (log(Tree.Size - 1) + 0.5772156649) - 2 * (Tree.Size - 1) / Tree.Size;
        else
            c=0;
        end
        Tree.high = CurtHeight + c;
        pathline3(CurtIndex)=repmat(Tree.high,1,NumInst);
        
        pathline5=[pathline5 Tree.high];
    else
        Tree.NodeStatus = 0;
        Tree.SplitAttribute = [];
        Tree.SplitPoint = [];
        Tree.LeftChild = [];
        Tree.RightChild = [];
        Tree.Size = NumInst;
        Tree.CurtIndex=CurtIndex;
        Tree.la=alltraindatalabel(CurtIndex,:);
        if  NumInst == 1
            Tree.center=Data(CurtIndex,:);
        end
        Tree.id=id2;
        id2=id2+1;
        flag1=1;
        Tree.high = CurtHeight;
    end
    
    return;
else
    Tree.NodeStatus = 1;
    % randomly select a split attribute
    [temp, rindex] = max(rand(1, Paras.NumDim));
    Tree.SplitAttribute = Paras.IndexDim(rindex);
    CurtData = Data(CurtIndex, Tree.SplitAttribute);
    CurtDatalabel=alltraindatalabel(CurtIndex,:);
    Tree.SplitPoint = min(CurtData) + (max(CurtData) - min(CurtData)) * rand(1);
    % instance index for left child and right children
    
    
    LeftCurtIndex = CurtIndex(CurtData < Tree.SplitPoint);
    RightCurtIndex = setdiff(CurtIndex, LeftCurtIndex);
    Tree.LeftCurtIndex=LeftCurtIndex;
    Tree.LeftCurtIndexla=alltraindatalabel(LeftCurtIndex,:);
    Tree.RightCurtIndex=RightCurtIndex;
    Tree.RightCurtIndexla=alltraindatalabel(RightCurtIndex,:);
    Tree.Size = NumInst;
    
    Tree.LeftChild = SENCTree2(Data, LeftCurtIndex, CurtHeight + 1, Paras,alltraindatalabel,newlabel);
    if flag1==1
        
        C = mean(Data(RightCurtIndex,:),1);
        Tree.dist=max(pdist2(Data(RightCurtIndex,:),C));
        Tree.center=C;
        flag1=0;
        if NumInst~=1
            c = 2 * (log(Tree.Size - 1) + 0.5772156649) - 2 * (Tree.Size - 1) / Tree.Size;
        else
            c=0;
        end
        Tree.high = CurtHeight + c;
    end
    Tree.RightChild = SENCTree2(Data, RightCurtIndex, CurtHeight + 1, Paras,alltraindatalabel,newlabel);
    if flag1==1
        C = mean(Data(LeftCurtIndex,:),1);
        Tree.dist=max(pdist2(Data(LeftCurtIndex,:),C));
        Tree.center=C;
        flag1=0;
        if NumInst~=1
            c = 2 * (log(Tree.Size - 1) + 0.5772156649) - 2 * (Tree.Size - 1) / Tree.Size;
        else
            c=0;
        end
        Tree.high = CurtHeight + c;
    end
    
    iTree.size = [];
    
end
