from logisticregression import LogisticRegression
from preprocessing import load_to_array
from random import shuffle

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



data = load_data('best.csv')
# print(data)
shuffle(data)

# The problem when I stopped was that the number of attributes for every item was inconsistent and the results without ckd were shorters
# Also there are random strings thrown in there to mess everything up
# But should be able to test it with LogisticRegression from sklearn soon, and then my code


train_X = [d[:24] for d in data[:int(len(data) * .8)]]
train_y = [d[24] for d in data[:int(len(data) * .8)]]

test_X = [d[:24] for d in data[:int(len(data) * 0.2)]]
test_y = [d[24] for d in data[:int(len(data) * 0.2)]]

log = LogisticRegression()

log.fit(train_X, train_y)


total = 0
correct = 0
for x, y in zip(test_X, test_y):
    x = log.predict([x])
    if x[0] == y:
        correct += 1
    
    total += 1
        

print("Accuracy: ", correct / total * 100)