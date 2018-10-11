from logisticregression import LogisticRegression
from nplogreg import LogRegNp
from preprocessing import load_to_array
from random import shuffle
import numpy as np

def f_measure(predictor, X, y):

  true_positive = 0
  false_positive = 0
  true_negative = 0
  false_negative = 0

  for i in range(len(X)):
    prediction = predictor.predict(X[i])
    print(prediction)
    if prediction > 0.5:
      prediction = 1
    else:
      prediction = 0
    if y[i] == 1:
      if prediction == 1:
        true_positive += 1
      else:
        false_positive += 1
    elif y[i] == 0:
      if prediction == 0:
        true_negative += 1
      else:
        false_negative += 1
  
  try:
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
  except:
    return np.nan

  if true_positive == 0:
    return 0
  return (2 * precision * recall) / (precision + recall)


def load_data(fileName):
    data = []
    with open(fileName, 'r') as theFile:
        lines = theFile.read().split('\n')
        print(len(lines))
        for i, l in enumerate(lines):
            current = []
            for attr in l.split(',')[:25]:
                current.append(float(attr))
            data.append(current)

    return data



data = load_data('best2.csv')

# data = data / np.linalg.norm(data)
# print(data)
shuffle(data)

# The problem when I stopped was that the number of attributes for every item was inconsistent and the results without ckd were shorters
# Also there are random strings thrown in there to mess everything up
# But should be able to test it with LogisticRegression from sklearn soon, and then my code


train_X = np.array([d[:24] for d in data[:int(len(data) * .8)]])
train_X = train_X / np.linalg.norm(train_X)
train_y = np.array([d[24] for d in data[:int(len(data) * .8)]])

test_X = np.array([d[:24] for d in data[int(len(data) * 0.2):]])
test_X = test_X / np.linalg.norm(test_X)
test_y = np.array([d[24] for d in data[int(len(data) * 0.2):]])

  
log = LogRegNp()

log.fit(train_X, train_y)#, alpha=0.0001, epsilon=0.000000000000000001)
# log.load_weights('weights_logreg.ml')
log.save_weights("weights_logreg.ml")

training_set = []
test_set = []
for lam_bda in np.arange(-2.0, 4.0, 0.2):
    log.fit(train_X, train_y, lam_bda=lam_bda)
    training_set.append([lam_bda, f_measure(log, train_X, train_y)])
    test_set.append([lam_bda, f_measure(log, test_X, test_y)])

with open('results.txt', 'w') as theFile:
    theFile.write(str(training_set) + '\n')
    theFile.write(str(test_set))
