import random

class Point:
  def __init__(self, x, y, id=None, cluster=None):
    self.x = x
    self.y = y
    if id is not None:
      self.id = id
    self.id = -1
    self.cluster = None

  def dist_to(self, other):
    return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

  def setCluster(self, cluster):
    self.cluster = cluster.id

  def __repr__(self):
    return "[{0}, {1}]".format(self.x, self.y)

  @staticmethod
  def _parseNum(num):
    split = num.split('E')
    return float(split[0]) * 10 ** int(split[1])

  @staticmethod
  def parseCoord(coord):
    x = Point._parseNum(coord[0])
    y = Point._parseNum(coord[1])

    return x, y
  
  def min(self):
    if self.x < self.y:
      return self.x
    else:
      return self.y

  def max(self):
    if self.x > self.y:
      return self.x
    else:
      return self.y


class Cluster:
  def __init__(self, center, id, points=None):
    self.center = center
    if points is not None:
      self.points = points
    else:
      self.points = []

    self.id = id
  def reCalcCenter(self):
    if len(self.points) == 0:
      return
    x_sum = 0
    y_sum = 0
    for p in self.points:
      x_sum += p.x
      y_sum += p.y
    
    self.center = Point(x_sum / len(self.points), y_sum / len(self.points))

  def addPoint(self, point):
    self.points.append(point)
  
  def remPoint(self, point):
    for i, p in enumerate(self.points):
      if p.id == point.id:
        del self.points[i]



def getPointsFromFile(file):

  with open(file, 'r') as theFile:
    points = []
    split = theFile.read().split('\n') 
    for line in split:
      if line != '':
        point_split = line.split('\t')
        point = Point(*Point.parseCoord(point_split[1:]), int(point_split[0]))
        points.append(point)
    return points


def kmeans(points, num_clusters):
  minVal = min([p.min() for p in points])
  maxVal = max([p.max() for p in points])
  clusters = []
  for i in range(num_clusters):
    x = (random.random() * (maxVal - minVal)) + minVal
    y = (random.random() * (maxVal - minVal)) + minVal
    clusters.append(Cluster(Point(x, y), i))

  for p in points:
      min_dist = None
      min_clust_index = None
      for i, c in enumerate(clusters):
        dist = p.dist_to(c.center)
        if min_dist is None or dist < min_dist:
          min_dist = dist
          min_clust_index = i
      min_cluster = clusters[min_clust_index]
      min_cluster.addPoint(p)

      
  while True:
    anyChange = False
    for c in clusters:
      for p in points:
        min_dist = None
        min_cluster = None
        for i, clust in enumerate(clusters):
          dist = p.dist_to(c.center)
          if min_dist is None or dist < min_dist:
            min_dist = dist
            min_cluster = clust

        
        if min_cluster != c:
          c.remPoint(p)
          min_cluster.addPoint(p)
          anyChange = True


    for c in clusters:
      c.reCalcCenter()
    
    if not anyChange:
      break

  return clusters

  


points = getPointsFromFile('cluster_data.txt')

clusters = kmeans(points, 10)
print(clusters)


