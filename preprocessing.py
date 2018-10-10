
from random import shuffle
from sklearn.linear_model import LogisticRegression

class Attribute:
    def __init__(self, name, the_type):
        self.name = name
        self.type = the_type.strip()
        result = self.type.strip('}{')
        self.valid = result.split(',')

    def checkValidEntry(self, entry):
        if 'numeric' in self.type:
            try:
                float(entry)
                return True
            except:
                return False
        elif '{' in self.type:
            return entry in self.valid
    
    def __repr__(self):
        return "{0} + {1}".format(self.name, self.type)


def load_to_array(fileName):
    data = []
    attributes = []
    with open(fileName, 'r') as theFile:
        lines = theFile.read().split('\n')
        dataLines = False
        for l in lines:
            if '@data' in l:
                dataLines = True
                continue
            elif '@attribute' in l:
                split = l.split(' ')
                name = split[1]
                the_type = split[2]
                attributes.append(Attribute(name, the_type))

            if dataLines:
                split = l.split(',')
                current = []
                for i, attr in enumerate(split):
                    current.append(attr.strip(' '))
                
                data.append(current)

    return data, attributes


def replaceQuestionMarkWithMean(data, attributes):
    ckdmeans = [0 for i in attributes]
    ckd_count = 0
    notckdmeans = [0 for i in attributes]
    notckd_count = 0


    for d in data:
        for i, attr in enumerate(d[:-1]):
            if "numeric" in attributes[i].type and attr != '?':
                if d[-1] == 'ckd':
                    ckdmeans[i] += float(attr)
                else:
                    notckdmeans[i] += float(attr)
            
        if d[-1] == 'ckd':
            ckd_count += 1
        else:
            notckd_count += 1
    
    ckdmeans = [the_sum / ckd_count for the_sum in ckdmeans]
    notckdmeans = [the_sum / notckd_count for the_sum in notckdmeans]

    for d in data:
        for i, attr in enumerate(d[:-1]):
            if 'numeric' in attributes[i].type:
                if attr == '?' and d[-1] == 'ckd' :
                    d[i] = ckdmeans[i]
                elif attr == '?':
                    d[i] = notckdmeans[i]

    
    return data

def changeYesNoTo01(data, attrs):
    for d in data:
        for i in range(len(attrs)):
            if '{yes,no}' in attrs[i].type\
                 or 'good' in attrs[i].type \
                 or 'present' in attrs[i].type \
                 or 'abnormal' in attrs[i].type:
                if d[i] == 'yes' \
                    or d[i] == 'good' \
                    or d[i] == 'normal'\
                    or d[i] == 'absent':
                    d[i] = 1
                else:
                    d[i] = 0
            elif  type(d[i]) is str and 'ckd' in d[i]:
                if d[i] == 'ckd':
                    d[i] = 1
                else:
                    d[i] = 0


    return data

def finalStep(data):
    for d in data:
        for i, a in enumerate(d):
            if a == '?':
                d[i] = 0
            else:
    
                try:
                    d[i] = float(d[i])
                except:
                    print(type(a), a)
    return data

def outputToCsv(fileName, data):
    with open(fileName, 'w') as theFile:
        for d in data:
            for attr in d[:-1]:
                theFile.write(str(attr)  + ",")
            
            theFile.write(str(d[-1]) + '\n')
    


if __name__ == "__main__":

    data, attrs = load_to_array('chronic_kidney_disease_full.arff')


    print(len(data))
    print(len(attrs), attrs)
    filled = replaceQuestionMarkWithMean(data, attrs)
    better = changeYesNoTo01(filled, attrs)
    best = finalStep(better)
    outputToCsv("best2.csv", best)

    shuffle(best)

    # The problem when I stopped was that the number of attributes for every item was inconsistent and the results without ckd were shorters
    # Also there are random strings thrown in there to mess everything up
    # But should be able to test it with LogisticRegression from sklearn soon, and then my code


    # train_X = [d[:24] for d in best[:int(len(best) * .8)]]
    # train_y = [d[24] for d in best[:int(len(best) * .8)]]

    # test_X = [d[:24] for d in best[:int(len(best) * 0.2)]]
    # test_y = [d[24] for d in best[:int(len(best) * 0.2)]]

    # clf = LogisticRegression().fit(train_X, train_y)

    # print(clf.predict([test_X[0]]), test_y[0])

    # total = 0
    # correct = 0
    # for x, y in zip(test_X, test_y):
    #     x = clf.predict([x])
    #     if x[0] == y:
    #         correct += 1
        
    #     total += 1
            

    # print("Accuracy: ", correct / total * 100)





    



