
from math import log
from math import e
from random import uniform
import numpy as np


"""
predict(x) = w_0 + w_1*x_1 + ... + w_n*x_n

w_0 = w_0 - a * 1/m * sum([predict(x) - y) * x_j])

"""
def euclidean(w_old, w_new):
    dist = sum([(w_new[i] - w_old[i]) ** 2 for i in range(len(w_old))]) ** 0.5
    return dist

class LogisticRegression:
  
    def save_weights(self, fileName):
        with open(fileName, 'w') as theFile:
            output = ''
            for w in self.w:
                output += str(w) + ','
            
            theFile.write(output[:-1])

    def load_weights(self, fileName):
        with open(fileName, 'r') as theFile:
            self.w = [float(w) for w in theFile.read().split(',')]


    def J(self):
        def cost(X_i, y):
            h = self.predict(X_i)
            # print(h)
            if abs(y) < 0.00000001:
                return -log(1.0000000001 - h)
            else:
                return -log(h)
            # return -y*log(h) - (1-y)*log(1- h)
            
        class_one_total = 0
        class_two_total = 0
        for i in range(self.m):
            h = self.predict(self.X[i])
            if self.y[i] == 1:
                class_one_total += -log(h)
            else:
                class_two_total += -log(1.0000000001 - h)

        cost = class_one_total - class_two_total
        # print(total_cost)
        return cost / self.m

    def predict(self, X, debug=False):
        def logit(val):
            # print("Logit Input: ", val)
            try:
                return 1 / (1 + (e ** -val))
            except:
                return 0.00000000001
        res = 0

        for i in range(len(X)):
            res += X[i]*self.w[i]
        
        if debug:
            print(res)
        logit_val = logit(res)

        if logit_val > 0.5:
            return 1
        else:
            return 0.00000000001

    def fit(self, X, y, lam=10, alpha=1, epsilon=0.01):
        
        self.X = X
        self.y = y
        self.n = len(X[0])
        self.m = len(X)
        self.w = [0 for i in range(self.n)]
        w_old = [1000] + self.w[1:] # Large initial value so epsilon isn't met
        prev_J = self.J()
        print("Initial:", prev_J)
        # slide 65
        # slide 48
        diff = euclidean(w_old, self.w)
        while diff > epsilon:
            # print(self.w)
            w_old = self.w[:]
            w_copy = self.w[:]

            for j in range(self.n):
                
                gradient = 0
                for i in range(self.m):
                    prediction = self.predict(X[i])
                    diff = (prediction - y[i]) * X[i][j]
                    gradient += diff
                # gradient = sum([(self.predict(X[i]) - y[i]) * X[i][j]  for i in range(self.m)]) 
                
                delta = alpha * (1/self.m) * gradient

                w_copy[j] -= delta #+ \
               # (lam / (2 * m)) * sum([w__i ** 2 for w__i in self.w])
            
            self.w = w_copy[:]

            diff = euclidean(w_old, self.w)
     
            prev_J = self.J()
            print("J: ", prev_J)
            print("weights: ", self.w)

        #### https://ml-cheatsheet.readthedocs.io/en/latest/logistic_regression.html 



   
        
    

