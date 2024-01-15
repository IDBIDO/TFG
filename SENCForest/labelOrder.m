
% Suponiendo que cluster_data es tu conjunto de datos y la última columna contiene las etiquetas
data_labels = cluster_data(:, end); % Extrae las etiquetas

% Inicializa un arreglo vacío para almacenar el orden de aparición
unique_labels_in_order = [];

% Recorre todas las etiquetas
for i = 1:length(data_labels)
    label = data_labels(i);
    % Si la etiqueta actual no está ya en unique_labels_in_order, añádela
    if ~ismember(label, unique_labels_in_order)
        unique_labels_in_order = [unique_labels_in_order; label];
    end
end

fprintf('---------END---------\n');