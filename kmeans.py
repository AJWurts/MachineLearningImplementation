import random
from visualization import plot_points

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

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  
  def __ne__(self, other):
    return self.x != other.x or self.y != other.y


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
  
  def clear(self):
    self.points.clear()

  def addPoint(self, point):
    self.points.append(point)
  
  def remPoint(self, point):
    for i, p in enumerate(self.points):
      if p == point:
        del self.points[i]
        return True
    return False

  def __repr__(self):
    return str(self.center)




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


def kmeans(points, num_clusters, plot=False):
  minX = min([p.x for p in points])
  maxX = max([p.x for p in points])
  minY = min([p.y for p in points])
  maxY = max([p.y for p in points])
  print(minX, maxY, minY, maxY)
  clusters = []

  for i in range(num_clusters):
    x = random.uniform(minX, maxX)
    y = random.uniform(minY, maxY)
    clusters.append(Cluster(Point(x, y), i))

  while True:
    for p in points:
      min_dist = None
      min_clust_index = None
      for i, c in enumerate(clusters):
        dist = p.dist_to(c.center)

        if min_dist is None or dist < min_dist:
          min_dist = dist
          min_clust_index = i
      clusters[min_clust_index].addPoint(p)


    
    if plot:
      img = plot_points([Point(-100, -100)])
      colors = ['red', 'blue', 'yellow']
    anyChange = False
    for i, c in enumerate(clusters):
      oldCenter = c.center
      c.reCalcCenter()
      if oldCenter != c.center:
        anyChange = True

      if plot:
        img = plot_points(c.points, fill=colors[i], image=img)
        img = plot_points([c.center], fill='green', image=img)

  
    if plot:
      img.show()
      input() # Pauses after each step


    
    if not anyChange:
      break
    else:
      [c.clear() for c in clusters]



    

  return clusters

  


points = getPointsFromFile('cluster_data.txt')
minX = min([p.x for p in points])
maxX = max([p.x for p in points])
minY = min([p.y for p in points])
maxY = max([p.y for p in points])
pRange = [minX, maxX, minY, maxY]
clusters = kmeans(points, 6)

img, _ = plot_points([Point(-100, -100)], fill='black')
img.show()
colors = ['red', 'blue', 'white', 'purple', 'orange', 'navy']
for i, c in enumerate(clusters):
  img, _ = plot_points(c.points, fill=colors[i], image=img, pRange=pRange, axis=True)
  img, _ = plot_points([c.center], fill='green', image=img, pRange=pRange, label='Cluster ' + str(i), axis=True)


img.show()

print(clusters)

