function newtree=updatetree(temptree,idtree,alltraindata,alltraindatalabel,newlabel)
global pathline3 pathlinenew pathline5 rt

if temptree.NodeStatus == 0
    tempid=find(idtree==temptree.id);
    if ~isempty(tempid)
        pathline3=[];
        updata=alltraindata(tempid,:);
        updatalabel=alltraindatalabel(tempid,:);
        if temptree.Size~=0
            updata=[updata; repmat(temptree.center,temptree.Size,1)];
            updatalabel=[ updatalabel;temptree.la ];
        end
        IndexDim = 1:size(updata,2);
        Paras.NumDim = size(updata,2);
        Paras.HeightLimit = 50;
        Paras.IndexDim = IndexDim;
        
        IndexSub = 1:size(updata,1);
        rt=temptree.Height+3;
        newtree= SENCTree2(updata, IndexSub, temptree.Height, Paras,updatalabel,newlabel);% build an isolation tree
    else  
        newtree=temptree;
        if ~isempty(temptree.la)
            pathline5=[pathline5 temptree.high];
        end
    end 
    return
    
    
else
    
    LeftChild =temptree.LeftChild;
    RightChild = temptree.RightChild;
    
    temptree.LeftChild= updatetree(LeftChild,idtree,alltraindata,alltraindatalabel,newlabel);
    
    temptree.RightChild=  updatetree(RightChild,idtree,alltraindata,alltraindatalabel,newlabel);
    
    
end

newtree=temptree;


end