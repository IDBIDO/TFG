function Tree = SENCTree(Data, CurtIndex, CurtHeight, Paras,alltraindatalabel)
global flag1 id pathline pathline3
flag1=0;

Tree.Height = CurtHeight;
NumInst = length(CurtIndex);

if CurtHeight >= Paras.HeightLimit || NumInst <= 10
    if  NumInst > 1
        Tree.NodeStatus = 0;
        Tree.SplitAttribute = [];
        Tree.SplitPoint = [];
        Tree.LeftChild = [];
        Tree.RightChild = [];
        Tree.Size = NumInst;
        Tree.CurtIndex=CurtIndex;
        Tree.la=alltraindatalabel(CurtIndex,:);
        
        Tree.id=id;
        id=id+1;
        Tree.center = mean(Data(CurtIndex,:),1);
        Tree.dist=max(pdist2(Data(CurtIndex,:),Tree.center));
        if NumInst~=1
            c = 2 * (log(Tree.Size - 1) + 0.5772156649) - 2 * (Tree.Size - 1) / Tree.Size;
        else
            c=0;
        end
        
        Tree.high = CurtHeight + c;
        pathline=[pathline;Tree.high NumInst];
        pathline3(CurtIndex)=repmat(Tree.high,1,NumInst);
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
        Tree.id=id;
        id=id+1;
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
    % bulit right and left child trees
    
    Tree.LeftChild = SENCTree(Data, LeftCurtIndex, CurtHeight + 1, Paras,alltraindatalabel);
    if flag1==1
        Tree.center= mean(Data(RightCurtIndex,:),1);
        Tree.dist=max(pdist2(Data(RightCurtIndex,:),Tree.center));
        Tree.la=alltraindatalabel(RightCurtIndex,:);
        flag1=0;
        
    end
    Tree.RightChild = SENCTree(Data, RightCurtIndex, CurtHeight + 1, Paras,alltraindatalabel);
    if flag1==1
        
        Tree.center = mean(Data(LeftCurtIndex,:));
        Tree.dist=max(pdist2(Data(LeftCurtIndex,:),Tree.center));
        Tree.la=alltraindatalabel(LeftCurtIndex,:);
        flag1=0;
        
    end
    
    iTree.size = [];
    
end
end