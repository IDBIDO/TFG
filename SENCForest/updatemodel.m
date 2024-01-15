function [newReForest]=updatemodel(alltraindata,ReForest,alltraindatalabel,idbuffer)
global id2 pathlinenew pathline4 pathline5
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Parameter%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
newi=1;
slectnumber=20;%ReForest.NumSub;
for i=1:ReForest.NumTree 
pathline4=[];
idtree=idbuffer(i,:);
temptree=ReForest.Trees{i};
id2=temptree.totalid+1;
pathlinenew=[];
newlabel=unique(alltraindatalabel);
pathline5=[];
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%select instance%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

inde=randperm(size(alltraindata,1));
idtree1=idtree(inde(1:slectnumber));
alltraindata1=alltraindata(inde(1:slectnumber),:);
alltraindatalabel1=alltraindatalabel(inde(1:slectnumber),:);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
newtree=updatetree(temptree,idtree1,alltraindata1,alltraindatalabel1,newlabel);

newtree.totalid=id2-1;
newtree.pathline1=pathline5;
 tempan= sort(pathline5);
    %%%%%%%%%%%%%%%%%%%%%%
    for j=1:size(tempan,2)
        
        varsf(j)=std(tempan(1:j));
        varsb(j)=std(tempan(j:end));
        
        
        vars_rate2(j)=abs(varsf(j)-varsb(j));
    end
    bb=find(vars_rate2==min(vars_rate2));
   fprintf('old para is %d; new para is %d.',ReForest.anomaly(i),tempan(bb(1)));
    ReForest.anomaly(i)=tempan(bb(1));
    varsf=[];
    varsb=[];
    vars_rate2=[];   
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ReForest.Trees{newi}=newtree;

end
%fprintf("\n jjjjjjjjjjjjjjjjjjjjjjj")
newReForest=ReForest;


end