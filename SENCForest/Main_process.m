
% SENCForest.
% This is main program. art4 is simulated toydata by two dimension.
% 
% This package was developed by Mr. Mu. For any problem concerning the code, please feel free to contact Mr. Mu.

newevaluation=[];
Input_dataset=art4;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Parametres%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
train_num=2;  %Known Classes
newclass_num=1;   % clases emergentes en un periodo
num_per_class=2000;
alltraindata=[];
alltraindatalabel=[];
streamdata=[];
streamdatalabel=[];
ALLindex=[1 2 3];%randperm(size(Input_dataset(:,1),1)); %class index
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Random instances

for i =1:size(Input_dataset(:,1),1)
    dataindex=randperm(size(Input_dataset{i,1},1));    
    %testdataindex1=randperm(size(Input_dataset{i,1},2));
    datatemp=Input_dataset{i,1};
    datatemp=datatemp(dataindex',:);
    datatemp=full(datatemp(dataindex,:));
    Input_dataset{i,1}=datatemp;
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Train Instaces%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i=1:train_num
    datatemp=Input_dataset{ALLindex(i),1};            % coger todos los puntos de la clase i
    traindata{i,1}=datatemp(1:num_per_class,:);  % extraer un numero especifico de datos
    traindata{i,2}=Input_dataset{ALLindex(i),2} ; %extraer la etiqueta
    alltraindata=[alltraindata;traindata{i,1}] ;  % agregar los datos extraidos en un data stream
    alltraindatalabel=[alltraindatalabel;ones(size(traindata{i,1},1),1)*traindata{i,2}];
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Test Instaces%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
testdata1={};
for i=1:train_num+newclass_num
    datatemp=Input_dataset{ALLindex(i),1};
    testdata{i,1}=datatemp(num_per_class+1:num_per_class+500,:);  %extraer 500 empezando de ultima instancias training + 1
    % asignar etiqueta(que clase pertenece)
    if i<=train_num
        testdata{i,2}=Input_dataset{ALLindex(i),2};
    else
        testdata{i,2}=999; %new class
    end
    % concatenar todos los datos
    streamdata=[streamdata;testdata{i,1}]; 
    streamdatalabel=[streamdatalabel;ones(size(testdata{i,1},1),1)*testdata{i,2}];
end
% balajar los datos      
randindex=randperm(size(streamdata,1));
streamdata=streamdata(randindex,:);
streamdatalabel=streamdatalabel(randindex,:);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%trainning process%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
NumTree = 100; % number of Tree
NumSub = 100; % subsample size for each class
CurtNumDim=size(alltraindata, 2);
rseed = sum(100 * clock);
set(0,'RecursionLimit',5000)
tic
Model = SENCForest(alltraindata, NumTree, NumSub, CurtNumDim, rseed,alltraindatalabel);
toc

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%testing process%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Para.beta=1;%%pathline
Para.alpha=1;%%%distance
Para.buffersize=50;
[Result]=Testingpro(streamdata,streamdatalabel,Model,Para);% eachclassnum,window);
%Model = updateModel
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Evaluation%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i=1:size(Result,1)
    newevaluation(i)=sum(Result(1:i,1)==Result(1:i,2))/i;
end
fprintf('---------END---------');

en_accuracy = EN_accuracy(Result);
positive_class_label = 999;  
f_measure = F_measure(Result, positive_class_label);