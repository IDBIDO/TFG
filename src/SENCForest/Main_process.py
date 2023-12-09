import sys
from time import time
import numpy as np
from scipy.io import loadmat

from src.SENCForest.SENCForest import SENCForest

# from SENCForest import SENCForest  # Assuming SENCForest is implemented in SENCForest.py
# from Testingpro import Testingpro  # Assuming Testingpro is implemented in Testingpro.py

# Parameters
train_num = 2  # Known Classes
newclass_num = 1
num_per_class = 2000
alltraindata = np.empty((0, 2))  # Replace num_features with the actual number of features -> 0: class instance, 1: class label
alltraindatalabel = np.empty((0,), dtype=int)
streamdata = np.empty((0, 2))
streamdatalabel = np.empty((0,), dtype=int)
ALLindex = [0, 1, 2]  # randperm(size(Input_dataset(:,1),1)); %class index

# Load data
mat_data = loadmat('data.mat')
Input_dataset = mat_data['art4']
#np.savetxt('Input_dataset.txt', Input_dataset[0][0], fmt='%f', delimiter='\t')
# Random Instances
for i in range(len(Input_dataset)):
    dataindex = np.random.permutation(len(Input_dataset[i, 0]))  # random select class id
    datatemp = Input_dataset[i, 0][dataindex, :]  # random select instances
    Input_dataset[i, 0] = datatemp
#print(Input_dataset)
np.savetxt('Input_dataset.txt', Input_dataset[0][0], fmt='%f', delimiter='\t')
print(datatemp.shape)

# Train Instances
traindata = np.empty((train_num, 2), dtype=object)
for i in range(train_num):
    datatemp = Input_dataset[ALLindex[i], 0]
    traindata[i, 0] = datatemp[:num_per_class, :]
    traindata[i, 1] = Input_dataset[ALLindex[i], 1]
    alltraindata = np.vstack((alltraindata, traindata[i, 0]))

    label_array = np.ones((traindata[i, 0].shape[0],)) * traindata[i, 1]
    label_array = label_array.flatten()  # Flatten the array to 1D
    alltraindatalabel = np.hstack((alltraindatalabel, label_array))
print(datatemp.shape)
#print(alltraindata.shape)
#print(alltraindatalabel.shape)
np.savetxt('alltraindatalabel.txt', alltraindatalabel, fmt='%d')
np.savetxt('alltraindata.txt', alltraindata, fmt='%f', delimiter='\t')


# Test Instances
testdata = []
for i in range(train_num + newclass_num):       # 3 classes: 2 known, 1 new
    datatemp = Input_dataset[ALLindex[i], 0]
    # select 500 instances not in training set, starting from num_per_class + 1
    testdata.append([datatemp[num_per_class + 1:num_per_class + 501, :], Input_dataset[ALLindex[i], 1]])
    if i <= train_num:
        testdata[i][1] = Input_dataset[ALLindex[i], 1]
    else:
        testdata[i][1] = 999  # new class
    streamdata = np.vstack((streamdata, testdata[i][0]))
    stream_label = np.ones((testdata[i][0].shape[0],)) * testdata[i][1]
    stream_label = stream_label.flatten()  # Flatten the array to 1D
    streamdatalabel = np.hstack((streamdatalabel, stream_label))

randindex = np.random.permutation(streamdata.shape[0])
streamdata = streamdata[randindex, :]
streamdatalabel = streamdatalabel[randindex]
np.savetxt('streamdatalabel.txt', streamdatalabel, fmt='%d')
np.savetxt('streamdata.txt', streamdata, fmt='%f', delimiter='\t')


# Now we have 2 datasets: alltraindata and streamdata,
# with label information in alltraindatalabel and streamdatalabel

#
# Training process
NumTree = 100  # number of Tree
NumSub = 100  # subsample size for each class
CurtNumDim = alltraindata.shape[1]
rseed = int(sum(100 * np.random.randint(0, 1000, size=10)))  # Generate a random seed based on the current time
#sys.setrecursionlimit(5000)

start_time = time()  # Start the timer
Model = SENCForest(alltraindata, NumTree, NumSub, CurtNumDim, rseed, alltraindatalabel)  # Train the SENCForest model
elapsed_time = time() - start_time  # Calculate elapsed time
print(f"Elapsed Time: {elapsed_time} seconds")

#
# # Testing process
# Para = {'beta': 1, 'alpha': 1, 'buffersize': 300}
# Result = Testingpro(streamdata, streamdatalabel, Model, Para)
#
# # Evaluation
# newevaluation = [np.sum(Result[:i + 1, 0] == Result[:i + 1, 1]) / (i + 1) for i in range(Result.shape[0])]
