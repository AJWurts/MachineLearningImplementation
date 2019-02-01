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

    pred = self.predict(X)


    cost = -y*np.log(pred) - (1-y)*np.log(1. - pred)

    cost = cost.sum() / self.m

    return cost

  def predict(self, X):
    z = np.dot(X, self.w)
    return sigmoid(z)


  
  def fit(self, X, y, alpha=500, epsilon=0.0001, lam_bda=1, cycles=200000):

    self.w = np.zeros(len(X[0]))
    self.m = len(X)
    self.n = len(X[0])
    

    old_cost = self.cost_function(X, y)
    for _ in range(cycles):
    
      pred = self.predict(X)

      grad = np.dot(X.T, pred - y) + (lam_bda / self.m) * sum(self.w)

      grad = grad * (alpha / self.m)

      self.w -= grad
     
      current_cost = self.cost_function(X, y)


      if abs(old_cost - current_cost) < epsilon:
        break
      
      old_cost = current_cost