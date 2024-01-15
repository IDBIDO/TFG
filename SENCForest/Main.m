
% SENCForest.
% This is the main program. 'art4' is simulated toy data by two dimensions.
% 
% This package was developed by Mr. Mu. For any problem concerning the code, please feel free to contact Mr. Mu.

newevaluation=[];
% Input_dataset=art4;  % Commented out as the dataset will be defined later
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
train_num=2;  % Known Classes
newclass_num=1;   % Emerging classes in a period
num_train_instances = 2000;
next_instances_index = 1;

 dimension = size(cluster_data, 2) - 1; % Number of attributes of the dataset 

alltraindata=[];
alltraindatalabel=[];
streamdata=[];
streamdatalabel=[];
current_old_clusters = [];

positive_class_label = 999;  

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Training instances %%%%%%%%%%%%%%%%%%

% Extract the first 'num_train_instances' for training
alltraindata = cluster_data(next_instances_index:num_train_instances, 1:dimension);      % Attributes (first 2000 rows, specified dimensions)
alltraindatalabel = cluster_data(next_instances_index:num_train_instances, end);   % Labels (first 2000 rows, last column)
next_instances_index = next_instances_index + num_train_instances;
current_old_clusters = unique(alltraindatalabel);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Test Instances %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Extract the next 'num_train_instances' for testing
end_instances_index = next_instances_index + num_train_instances - 1;
streamdata = cluster_data(next_instances_index:end_instances_index, 1:dimension);      % Attributes (next 2000 rows, specified dimensions)
streamdatalabel = cluster_data(next_instances_index:end_instances_index, end);   % Labels (next 2000 rows, last column)

% Identify and label new classes
for i = 1:length(streamdatalabel)
    if ~ismember(streamdatalabel(i), current_old_clusters)
        % If the label is not in 'current_old_clusters', label it as 999 (new class)
        streamdatalabel(i) = positive_class_label;
    end
end
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
Para.buffersize=100;
tic
[Result, updateModel]=Testingpro(streamdata,streamdatalabel,Model,Para, positive_class_label);% eachclassnum,window);
toc
Model = updateModel;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Evaluation%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i=1:size(Result,1)
    newevaluation(i)=sum(Result(1:i,1)==Result(1:i,2))/i;
end
fprintf('---------END---------\n');

en_accuracy = EN_accuracy(Result);
f_measure = F_measure(Result, positive_class_label);
