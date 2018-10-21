from logisticregression import LogisticRegression
from nplogreg import LogRegNp
from preprocessing import load_to_array
from random import shuffle
import numpy as np
import matplotlib.pyplot as plt

def f_measure(predictor, X, y):

  true_positive = 0
  false_positive = 0
  true_negative = 0
  false_negative = 0

  for i in range(len(X)):
    prediction = predictor.predict(X[i])
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
        lines = theFile.read().split('\n')[1:]
        print(len(lines))
        for i, l in enumerate(lines):
            current = []
            for attr in l.split(',')[:25]:
              try:
                current.append(float(attr))
              except:
                print(i, l, attr)
            data.append(current)

    return data



data = load_data('chronic_kidney_disease_full.csv')

shuffle(data)


train_X = np.array([d[:len(d)-2] for d in data[:int(len(data) * .8)]])
# train_X = train_X / np.linalg.norm(train_X)
train_y = np.array([d[len(d)-1] for d in data[:int(len(data) * .8)]])

test_X = np.array([d[:len(d)-2] for d in data[int(len(data) * 0.2):]])
# test_X = test_X / np.linalg.norm(test_X)
test_y = np.array([d[len(d)-1] for d in data[int(len(data) * 0.2):]])

  
log = LogRegNp()

training_set = []
test_set = []
for lam_bda in np.arange(-2.0, 4.0, 0.2):
    log.fit(train_X, train_y, lam_bda=lam_bda)
    training_set.append([lam_bda, f_measure(log, train_X, train_y)])
    test_set.append([lam_bda, f_measure(log, test_X, test_y)])




plt.plot([v[0] for v in training_set], [v[1] for v in training_set])
plt.xlabel("Lambda")
plt.ylabel("F-Measure")
plt.title("Training Data")
plt.show()
plt.plot([v[0] for v in test_set], [v[1] for v in test_set])
plt.title("Test Data")
plt.show()


with open('results.txt', 'w') as theFile:
    theFile.write(str(training_set) + '\n')
    theFile.write(str(test_set))
