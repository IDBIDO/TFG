

% Example usage:
% tree = Model.Trees{63, 1};  % One of the trees in your model
% totalLeaves = countLeaves(tree);
% disp(['Total number of leaves in the tree: ', num2str(totalLeaves)]);

totalLeaves = 0;
numTrees = length(Model.Trees);
for i = 1:numTrees
    currentTree = Model.Trees{i, 1};
    totalLeaves = totalLeaves + countLeaves(currentTree);
end
averageLeaves = totalLeaves / numTrees;
disp(['Average number of leaves per tree: ', num2str(averageLeaves)]);


function numLeaves = countLeaves(node)
    if isempty(node.LeftChild) && isempty(node.RightChild)
        % This is a leaf node
        numLeaves = 1;
    else
        % Count leaves in left and right subtrees
        numLeavesLeft = countLeaves(node.LeftChild);
        numLeavesRight = countLeaves(node.RightChild);
        numLeaves = numLeavesLeft + numLeavesRight;
    end
end