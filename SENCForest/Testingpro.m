function [result_new, updateModel]=Testingpro(streamdata,streamdatalabel,model,Para, newClassLabel)     %trainsize,window)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Parametres%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
newclasslabel=newClassLabel;
buffer=[];
result_new=[];
idbuffer=[];
batchdatalabel=[];

batchdatalabel_true=[];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%testing%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for j=1:size(streamdata,1)
%     fprintf('%d True label is %d\n',j,streamdatalabel(j));
    [Mass, mtimetest] = SENCEstimation(streamdata(j,:),model,Para.alpha, model.anomaly);
    %%mass(,1)--pathline;
    %%mass(,2)--distance
    %%mass(,3)--label
    %mass(,4)--id to go
    %mass(,5)--new class or not
    answermass=Mass(:,3);
    answermass(find(Mass(:,5)==1),:)=newclasslabel;
    Score =  tabulate( answermass);
    Score_1=Score(Score(:,2)==max(Score(:,2)),:);
    
    if  Score_1(1)==newclasslabel                     %%resultv(j)>0.5
        buffer=[buffer;streamdata(j,:)];
        idbuffer=[idbuffer Mass(:,4)];
        % batchdata=[batchdata;onetestinstance];
        batchdatalabel=[batchdatalabel; newclasslabel];
        batchdatalabel_true=[batchdatalabel_true; streamdatalabel(j)];
%         fprintf('New class emerging %d\n', size(buffer,1));
        result_new=[result_new;[newclasslabel streamdatalabel(j)]];
    else
        result_new=[result_new;[Score_1(1) streamdatalabel(j)]];
    end
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%retrain%%%%%%%%%%%%%%%%%%%%%%%%%%%%%55
    if size(buffer,1)>= Para.buffersize 
        %tic% && k==1%%   %%fix(trainsize*(0.5))
        model=updatemodel(buffer,model,batchdatalabel,idbuffer);
        %toc
        fprintf('---------UPDATE--------- \n %f',model.c );
        buffer=[];
    end
      fprintf('%d\n', j);

end

updateModel = model;
end


