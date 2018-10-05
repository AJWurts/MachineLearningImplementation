
from math import log
from math import e as E


"""
h_w(x) = w_0 + w_1*x_1 + ... + w_n*x_n

w_0 = w_0 - a * 1/m * sum([h_w(x) - y) * x_j])

"""
def euclidean(w_old, w_new):
    dist = sum([(w_new[i] - w_old[i]) ** 2 for i in range(len(w_old))]) ** 0.5
    return dist

class LogisticRegression:
  
    def h_w(self, X):
        def logit(val):
            print(val)
            return 1 / (1 + E ** -val)
        res = 0
        for i in range(len(X)):
            # print(X[i], self.w[i])
            res += X[i]*self.w[i]
        

        return logit(res)

    def fit(self, X, y, lam=10, alpha=0.001):
        

        def cost(X, y):
            try:
                if y == 1:
                    return -log(self.h_w(X))
                else:
                    return -log(1.00001-self.h_w(X))
            except Exception as e:
                print(self.h_w(X), y)
                exit()

        m = len(X[0])
        n = len(X)
        self.w = [0 for _ in range(m)]
        w_old = [1000] + self.w[1:]
        epsilon = 200
        # slide 65
        # slide 48
        while euclidean(w_old, self.w) >= epsilon:
            
            w_old = self.w[:]
            for j, w_j in enumerate(self.w):
                a_value = sum([cost(X[i], y[i]) * X[i][j] for i in range(n)])
                print(a_value)
                self.w[j] += alpha * (1/m) * a_value #+ \
               # (lam / (2 * m)) * sum([w__i ** 2 for w__i in self.w])
        

        #### https://ml-cheatsheet.readthedocs.io/en/latest/logistic_regression.html 

    def predict(self, X):
        val = self.h_w(X)
        return 1 / (1 + E ** -val)

   
        
    

