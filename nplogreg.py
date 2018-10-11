import numpy as np 
from math import e



def sigmoid(z):
  return (1.0 / (1.0 + e ** -z))

class LogRegNp:

  def save_weights(self, fileName):
        with open(fileName, 'w') as theFile:
            output = ''
            for w in self.w:
                output += str(w) + ','
            
            theFile.write(output[:-1])

  def load_weights(self, fileName):
      with open(fileName, 'r') as theFile:
          self.w = [float(w) for w in theFile.read().split(',')]

  def cost_function(self, X, y):

    predictions = self.predict(X)

    #Take the error when label=1
    class1_cost = -y*np.log(predictions)

    #Take the error when label=0
    class2_cost = (1-y)*np.log(1.-predictions)

    #Take the sum of both costs
    cost = class1_cost - class2_cost

    #Take the average cost
    cost = cost.sum() / self.m

    return cost

  def predict(self, X):
    z = np.dot(X, self.w)
    return sigmoid(z)


  
  def fit(self, X, y, alpha=500, epsilon=0.1, lam_bda=1, cycles=1000000):

    self.w = np.zeros(len(X[0]))
    self.m = len(X)
    self.n = len(X[0])
    
    cost_history = []
    old_cost = self.cost_function(X, y)
    for _ in range(cycles):
    
      predictions = self.predict(X)

      gradient = np.dot(X.T, predictions - y) + (lam_bda / self.m) * sum(self.w)

      gradient = gradient * (alpha / self.m)

      self.w -= gradient
     
      current_cost = self.cost_function(X, y)
      if abs(old_cost - current_cost) < 0.001:
        break

      # cost = self.cost_function(X, y)
      # print(cost)

