from sklearn.datasets import load_digits
from sklearn.metrics import fowlkes_mallows_score
from sklearn.cluster import AgglomerativeClustering, AffinityPropagation
from kmeans import kmeans, Point, predict



data, target = load_digits(return_X_y=True)

# K-Means
kmeans_data = [Point(val) for val in data]
k_means = kmeans(kmeans_data, 10)

labels = []


for point in data:
    labels.append(predict(k_means, Point(point)))
target = [int(num) for num in target]




results = [[0 for _ in range(10)] for __ in range(10)]

for i, val in enumerate(labels):
    results[target[i]][val] += 1

conversion = {}
for t_i, targ in enumerate(results):
    max_cluster = None
    for c_i, cluster in enumerate(targ):
        if max_cluster is None or cluster > targ[max_cluster]:
            max_cluster = c_i
    
        conversion[t_i] = max_cluster

labels = [conversion[l] for l in labels]


print("K-Means Fowlkes-Mallows Score: ", fowlkes_mallows_score(target[:200], labels[:200]))
print("Grid for K-Means")
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

# Agglomerative Clustering

agglo = AgglomerativeClustering(n_clusters=10, linkage="ward")

clustering = agglo.fit(data)

results = [[0 for _ in range(10)] for __ in range(10)]

for i, val in enumerate(clustering.labels_):
    results[target[i]][val] += 1

conversion = {}
for t_i, targ in enumerate(results):
    max_cluster = None
    for c_i, cluster in enumerate(targ):
        if max_cluster is None or cluster > targ[max_cluster]:
            max_cluster = c_i
    
        conversion[t_i] = max_cluster

labels = [conversion[l] for l in clustering.labels_]

print("Agglomerative Fowlkes-Mallows Score: ", fowlkes_mallows_score(target[:500], labels[:500]))
print("Grid for Agglomerative")
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




# Affinity Propagation

aff = AffinityPropagation(preference=-50000)
clustering = aff.fit(data)

count = {}

for label in clustering.labels_:
    if label not in count:
        count[label] = 1
    else:
        count[label] += 1

results = [[0 for _ in range(10)] for __ in range(10)]

for i, val in enumerate(clustering.labels_):
    results[target[i]][val] += 1

conversion = {}
for t_i, targ in enumerate(results):
    max_cluster = None
    for c_i, cluster in enumerate(targ):
        if max_cluster is None or cluster > targ[max_cluster]:
            max_cluster = c_i
    
        conversion[t_i] = max_cluster

labels = [conversion[l] for l in clustering.labels_]

print("Affinity Fowlkes-Mallows Score: ", fowlkes_mallows_score(target[:500], labels[:500]))
print("Grid for Affinity")
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

