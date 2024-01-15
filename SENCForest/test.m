%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Test Instaces%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Extract the next 2000 instances for testing
%fprintf('%d\n', next_instances_index);

next_instances_index = 4001; 
current_old_clusters = [0 9 1]; % ADD OLD LABEL IN EACH NEW PERIOD
positive_class_label = 4; % CHANGE TO THE LABEL OF NEW CLASS

end_instances_index = next_instances_index + num_train_instances - 1;
%fprintf('%d\n', end_instances_index);
streamdata = cluster_data(next_instances_index:end_instances_index, 1:2);      % Attributes (rows 2001-4000, first 2 columns)
streamdatalabel = cluster_data(next_instances_index:end_instances_index, 3);   % Labels (rows 2001-4000, third column)

% Identify and label new classes
for i = 1:length(streamdatalabel)
    if ~ismember(streamdatalabel(i), current_old_clusters)
        % If the label is not in the current_old_clusters, label it as 999 (new class)
        streamdatalabel(i) = positive_class_label;    
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%testing process%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Para.beta=1;%%pathline
Para.alpha=1;%%%distance
Para.buffersize=100;
[Result, updateModel]=Testingpro(streamdata,streamdatalabel,Model,Para, positive_class_label);% eachclassnum,window);
Model = updateModel;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Evaluation%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i=1:size(Result,1)
    newevaluation(i)=sum(Result(1:i,1)==Result(1:i,2))/i;
end
fprintf('---------END---------');

en_accuracy = EN_accuracy(Result);
  
f_measure = F_measure(Result, positive_class_label);