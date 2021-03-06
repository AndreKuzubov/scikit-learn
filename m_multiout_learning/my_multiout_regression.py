from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.utils import shuffle
from numpy import array
import my_model_multi_out as mModel

print 'load dataset.....'

# dataset = mModel.load_datasets(n=100000, pointsInFrame=20)
datasetSize = 5000
dataSetStep = 0.5
dataset = mModel.load_dataset_uniform(n=datasetSize, step=dataSetStep)

# Split the data into training/testing sets
dataset_X_train = dataset[0][:-10]
dataset_X_test = dataset[0][-10:]

# Split the targets into training/testing sets
dataset_y_train = dataset[1][:-10]
dataset_y_test = dataset[1][-10:]

X = [[1, 23, 5], [1, 23, 8]]
Y = [[12, 6], [3, 9]]

mrg = MultiOutputRegressor(GradientBoostingRegressor(max_depth=10,
                                                     learning_rate=.05, min_samples_leaf=2,
                                                     min_samples_split=2))

learning_cicles = 1
for i in xrange(learning_cicles):
    dataset_X_train, dataset_y_train = shuffle(dataset_X_train, dataset_y_train)
    print 'training ' + str(i) + ' ..... '
    mrg.fit(dataset_X_train, dataset_y_train)

print mrg.predict(dataset_X_test)

print 'testing.....'
pedictY = mrg.predict(dataset_X_test)
predictY = list(pedictY)

print 'print to log file.....'
f1 = open('./log.txt', 'w+')
f1.write(str(mrg) + '\n' + '\n')
f1.write('datasetSize= ' + str(datasetSize) + '\n')
f1.write('dataSetStep= ' + str(dataSetStep) + '\n')
f1.write('learning_cicles= ' + str(learning_cicles) + '\n')

for i in xrange(len(pedictY)):
    y = dataset_y_test[i]
    x = dataset_X_test[i]
    predictY = pedictY[i]
    f1.write('test ' + str(i) + '\n')
    f1.write('centrPoint= ' + str(y) + '\n')
    f1.write('predictCentrPoint ' + str(predictY) + '\n')
    f1.write('err= ' + str(array(y) - array(predictY)) + '\n' + '\n')
f1.close()
print 'drawing.....'

for i in xrange(len(pedictY)):
    y = dataset_y_test[i]
    x = dataset_X_test[i]
    predictY = pedictY[i]
    mModel.draw_model(y, predictPoint=predictY, fileNameToSave='test_' + str(i), show=0)
    mModel.draw_learning_model(y, x, fileNameToSave='learning_model_' + str(i), show=0)

print 'finish.....'
