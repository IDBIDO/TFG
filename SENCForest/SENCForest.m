function Forest = SENCForest(Data, NumTree, NumSub, NumDim, rseed,label)
global id pathline3 pathline
id=1;
pathline3=[];
pathline=[];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Parametres%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Forest.NumTree = NumTree;
Forest.NumSub = NumSub;
Forest.NumDim = NumDim;
Forest.c = 2 * (log(NumSub - 1) + 0.5772156649) - 2 * (NumSub - 1) / NumSub;
Forest.rseed = rseed;
rand('state', rseed);
[NumInst, DimInst] = size(Data);
Forest.Trees = cell(NumTree, 1);
Forest.fruit=unique(label);
Forest.HeightLimit =200;  %; ceil(log2(NumSub*size(label,1)));
Paras.HeightLimit = Forest.HeightLimit;
Paras.IndexDim = 1:DimInst;
Paras.NumDim = NumDim;
classindex={};

et = cputime;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for j=1:size(Forest.fruit,1)
    classindex{j}=find(label==Forest.fruit(j,1));
end
IndexSub=[];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i = 1:NumTree
    for j=1:size(Forest.fruit,1)
        tempin =classindex{j};
        tempso=randperm(size(tempin,1));
        if size(tempin,1)<NumSub
            fprintf('number of instances is too small.');
            break;
        else
            IndexSub=[IndexSub tempin(tempso(1:NumSub),1)'];
        end
    end
    
    pathline=[];
    pathline3=[];
    Forest.Trees{i} = SENCTree(Data, IndexSub, 0, Paras,label);% build an isolation tree
    Forest.Trees{i}.totalid=id-1;
    Forest.Trees{i}.pathline=pathline3;
    Forest.Trees{i}.pathline1=pathline;
    tempan= sort(Forest.Trees{i}.pathline1(:,1)');
    
    for j=1:size(tempan,2)
        
        varsf(j)=std(tempan(1:j));
        varsb(j)=std(tempan(j:end));
        
        
        vars_rate2(j)=abs(varsf(j)-varsb(j));
    end
    bb=find(vars_rate2==min(vars_rate2));
    Forest.anomaly(i)=tempan(bb(1));
    IndexSub=[];
    id=1;
    varsf=[];
    varsb=[];
    vars_rate2=[];
    
end

Forest.ElapseTime = cputime - et;
end



