import os
import cPickle
import datetime

from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.utils import shuffle
from numpy import array
import my_model_multi_out_multianswer as mModel

folder = './testSpendTimeReport/'
if not os.path.exists(folder):
    os.makedirs(folder)

print 'load dataset.....'

# dataset = mModel.load_datasets(n=100000, pointsInFrame=20)
datasetSize = 1000
dataSetStep = 0.19
dataset = mModel.load_dataset_uniform(n=datasetSize, step=dataSetStep, maxPics=1)

# Split the data into training/testing sets
dataset_X_train = dataset[0][:-10]
dataset_X_test = dataset[0][-10:]

# Split the targets into training/testing sets
dataset_y_train = dataset[1][:-10]
dataset_y_test = dataset[1][-10:]

# load it again
# with open(folder + 'mrg.pkl', 'rb') as fid:
#     mrg = cPickle.load(fid)

mrg = MultiOutputRegressor(GradientBoostingRegressor(max_depth=10,
                                                     learning_rate=.1, min_samples_leaf=2,
                                                     min_samples_split=2))

startTime = datetime.datetime.now()

learning_cicles = 10
for i in xrange(learning_cicles):
    dataset_X_train, dataset_y_train = shuffle(dataset_X_train, dataset_y_train)
    print 'training ' + str(i) + ' left: ' + str(learning_cicles - i) + ' ..... '
    mrg.fit(dataset_X_train, dataset_y_train)

endTime = datetime.datetime.now()
elapsedTime = endTime - startTime
print 'spend time :' + str(elapsedTime)

print 'save neural network to disk.....'

# save the classifier
with open(folder + 'mrg.pkl', 'wb') as fid:
    cPickle.dump(mrg, fid)

print 'testing.....'
predictYs = mrg.predict(dataset_X_test)
predictYs = list(predictYs)
print str(predictYs)

print 'print to log file.....'
f1 = open(folder + 'log.txt', 'w+')
f1.write(str(mrg) + '\n' + '\n')
f1.write('datasetSize= ' + str(datasetSize) + '\n')
f1.write('dataSetStep= ' + str(dataSetStep) + '\n')
f1.write('learning_cicles= ' + str(learning_cicles) + '\n\n')
f1.write('spended time: ' + str(elapsedTime) + '\n\n')

for i in xrange(len(predictYs)):
    y = dataset_y_test[i]
    x = dataset_X_test[i]
    predictY = predictYs[i]
    f1.write('test ' + str(i) + '\n')
    f1.write('centrPoint= ' + str(y) + '\n')
    f1.write('predictCentrPoint ' + str(predictY) + '\n')
    f1.write('err= ' + str(array(y) - array(predictY)) + '\n' + '\n')

f1.close()
print 'drawing.....'

for i in xrange(len(dataset_X_test)):
    y = dataset_y_test[i]
    x = dataset_X_test[i]
    mModel.draw_model(y, predictPoint=predictYs[i], fileNameToSave=folder + 'test_' + str(i), show=0)
    mModel.draw_training_model(x, y, fileNameToSave=folder + 'training_model_' + str(i), show=0)

print 'finish.....'
