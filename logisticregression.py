
from math import log

"""
h_w(x) = w_0 + w_1*x_1 + ... + w_n*x_n

w_0 = w_0 - a * 1/m * sum([h_w(x) - y) * x_j])

"""
def euclidean(w_old, w_new):
    dist = sum([(w_new[i] - w_old[i]) ** 2 for i in range(len(w_old))]) ** 0.5
    return dist

def LogisticRegression(X, y, lam, alpha=0.1):
    def h_w(X):
        res = 0
        for i in range(len(X)):
            res += X[i]*w[i]
        
        return res

    def cost(X, y):
        if y == 1:
            return -log(h_w(X))
        else:
            return -log(1-h_w(X))

    m = len(X[0])
    w = [0 for _ in range(m)]
    w_old = 1000
    epsilon = 1
    # slide 65
    # slide 48
    while euclidean(w_old, w) >= epsilon :
        w_old = w[:]
        for j, w_i in enumerate(w):
            w_i = w_i - alpha * (1/m) * \
            sum([cost(X[i], y[i]) * X[i][j] for i in range(m)]) + \
            (lam / (2 * m)) * sum([w__i ** 2 for w__i in w])
    
    return w
        
    

