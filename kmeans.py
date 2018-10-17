import random
from visualization import plot_points

class Point:
  def __init__(self, attrs, id=None, cluster=None):
    self.attrs = attrs
    if id is not None:
      self.id = id
    self.id = -1
    self.cluster = None

  def __getitem__(self, i):
    return self.attrs[i]

  def __getattr__(self, attr):
    if attr == 'x':
      return self.attrs[0]
    elif attr == 'y':
      return self.attrs[1]
    elif attr == 'attrs':
      return self.attrs
    elif attr == 'id':
      return self.id
    elif attr == 'cluster':
      return self.cluster

  def dist_to(self, other):
    the_sum = 0
    for i in range(len(self.attrs)):
      if (type(self.attrs[i]) is int or type(self.attrs[i]) is float)\
          and (type(other.attrs[i] is int or type(other.attrs[i] is float))):
        the_sum += (self.attrs[i] - other.attrs[i]) ** 2
    return the_sum ** 0.5

  def setCluster(self, cluster):
    self.cluster = cluster.id

  def __repr__(self):
    return str(self.attrs)

  @staticmethod
  def _parseNum(num):
    split = num.split('E')
    return float(split[0]) * 10 ** int(split[1])

  @staticmethod
  def parseCoord(coord):
    x = Point._parseNum(coord[0])
    y = Point._parseNum(coord[1])

    return [x, y]
  
  def __eq__(self, other):
    if len(self.attrs) != len(other.attrs):
      return False
    
    for i in range(len(self.attrs)):
      if (type(self.attrs[i]) is int or type(self.attrs[i]) is float)\
          and (type(other.attrs[i] is int or type(other.attrs[i] is float))):
          if self.attrs[i] != other.attrs[i]:
            return False

    return True

  
  def __ne__(self, other):
    return not self == other


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
    var_sum = [0 for _ in self.center.attrs]

    for p in self.points:
      for i in range(len(p.attrs)):
        var_sum[i] += p[i]
    
    new_attrs = [var_sum[i] / len(self.points) for i in range(len(self.center.attrs))]

    self.center = Point(new_attrs)
  
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


def getMinMax(points):
  minMax = [[None, None] for _ in range(len(points[0].attrs))]

  for p in points:
    for i, a in enumerate(p.attrs):
      if minMax[i][0] is not None and a < minMax[i][0]:
        minMax[i][0] = a
      elif minMax[i][0] is None:
        minMax[i][0] = a

      if minMax[i][1] is not None and minMax[i][1] < a:
        minMax[i][1] = a
      elif minMax[i][1] is None:
        minMax[i][1] = a
      
  return minMax



def getPointsFromFile(file):

  with open(file, 'r') as theFile:
    points = []
    split = theFile.read().split('\n') 
    for line in split:
      if line != '':
        point_split = line.split('\t')
        point = Point(Point.parseCoord(point_split[1:]), int(point_split[0]))
        points.append(point)
    return points


def kmeans(points, num_clusters, plot=False):
  minMax = getMinMax(points)
  clusters = []

  for i in range(num_clusters):
    attrs = []
    for key in range(len(points[0].attrs)):
      attrs.append(random.uniform(minMax[key][0], minMax[key][1]))

    clusters.append(Cluster(Point(attrs), i))

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

  
if __name__ == "__main__":

  points = getPointsFromFile('cluster_data.txt')
  minX = min([p.x for p in points])
  maxX = max([p.x for p in points])
  minY = min([p.y for p in points])
  maxY = max([p.y for p in points])
  pRange = [minX, maxX, minY, maxY]
  clusters = kmeans(points, 6)

  img, _ = plot_points([Point([-100 for _ in points[0].attrs])], fill='black')
  img.show()
  colors = ['red', 'blue', 'white', 'purple', 'orange', 'gray']
  for i, c in enumerate(clusters):
    img, _ = plot_points(c.points, fill=colors[i], image=img, pRange=pRange, axis=True)
    img, _ = plot_points([c.center], fill='green', image=img, pRange=pRange, label='Cluster ' + str(i), axis=True)


  img.show()

  print(clusters)

