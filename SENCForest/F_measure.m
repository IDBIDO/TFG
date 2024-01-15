function f_measure = F_measure(Result, positive_class_label)
    % Extract true and predicted labels
    true_labels = Result(:, 2);
    predicted_labels = Result(:, 1);
    
    % Calculate TP, FP, and FN
    TP = sum((predicted_labels == positive_class_label) & (true_labels == positive_class_label));
    FP = sum((predicted_labels == positive_class_label) & (true_labels ~= positive_class_label));
    FN = sum((predicted_labels ~= positive_class_label) & (true_labels == positive_class_label));
    
    % Calculate Precision and Recall
    Precision = TP / (TP + FP);
    Recall = TP / (TP + FN);
    
    % Handle the case where Precision and Recall are both zero
    if (Precision + Recall) == 0
        f_measure = 0;
    else
        % Calculate F-measure
        f_measure = 2 * (Precision * Recall) / (Precision + Recall);
    end

    % Display the F-measure
    disp(['F-measure: ', num2str(f_measure)]);
end
