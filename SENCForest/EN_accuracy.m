function en_accuracy = EN_accuracy(Result)
    % Initialize counters
    A_n = 0;  % Correct predictions for new classes
    A_o = 0;  % Correct predictions for known classes
    N = size(Result, 1);  % Total number of instances

    % Define the label for new classes (e.g., 999 or 'NewClass')
    new_class_label = 999;  % Adjust as needed

    % Iterate through each instance in the Result
    for i = 1:N
        predicted_class = Result(i, 1);
        true_class = Result(i, 2);
        
        % Check if the prediction is correct
        if predicted_class == true_class
            % Check if it's a new class or a known class
            if true_class == new_class_label
                A_n = A_n + 1;  % Correct new class prediction
            else
                A_o = A_o + 1;  % Correct known class prediction
            end
        end
    end

    % Calculate EN Accuracy
    en_accuracy = (A_n + A_o) / N;

    % Return or display the EN Accuracy
    disp(['EN Accuracy: ', num2str(en_accuracy)]);
end


