from sklearn.datasets import load_digits
from sklearn.cluster import AgglomerativeClustering, AffinityPropagation


data, target = load_digits(return_X_y=True)

agglo = AgglomerativeClustering(n_clusters=10, linkage="ward")

clustering = agglo.fit(data)

results = [[0 for _ in range(10)] for __ in range(10)]

for i, val in enumerate(clustering.labels_):
    results[val-1][target[i]] += 1

print('Cluster on X axis, Number on Y Axis', end='\n    ')
[print("{:3d}".format(i), end=' ') for i in range(10)]
print('', end='\n    ')
[print("----", end='') for i in range(10)]

print('')
for x in range(10):
    print(x, end=' | ')
    for y in range(10):
        print("{:3d}".format(results[x][y]), end=' ')
    print('')

## Cluster to value conversion
## Cluster -> Number
## 3 -> 0
## 2 -> 1
## 7 -> 2
## 8 -> 3
## 4 -> 4
## 6 -> 5
## 0 -> 6
## 1 -> 7
## 1 -> 8
## 5 -> 9


# X axis is Cluster Number, Y Value is the actual Value

aff = AffinityPropagation()
clustering = aff.fit(data)

count = {}

for label in clustering.labels_:
    if label not in count:
        count[label] = 1
    else:
        count[label] += 1

zipped = []
for key in count.keys():
    zipped.append((key, count[key]))

    





