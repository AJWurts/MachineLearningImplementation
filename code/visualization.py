######################################################################################
#              IF YOU DONT HAVE PIL INSTALLED COMMENT OUT THIS CODE                  #
######################################################################################


from PIL import Image, ImageDraw, ImageFont
from IPython.display import display

def plot_edges(edge_list, image=None):
    SIZE = 800
    if image is None:
        image = Image.new('RGB', (SIZE, SIZE))
    expansion_factor = SIZE / 15
    draw = ImageDraw.Draw(image)
    for edge in edge_list:
        draw.line((edge.p1.get_xy(expansion_factor),
                   edge.p2.get_xy(expansion_factor)), fill='white')

    return image


def plot_points(points, fill='blue', image=None, pRange=None, label=None, axis=False):
    if pRange is None:
      minX = min([p.x for p in points])
      maxX = max([p.x for p in points])
      minY = min([p.y for p in points])
      maxY = max([p.y for p in points])

    else:
      minX = pRange[0]
      maxX = pRange[1]
      minY = pRange[2]
      maxY = pRange[3]

    size = 800
    xRange = max(maxX - minX, 0.01)
    yRange = max(maxY - minY, 0.01)

    padding = [20, 20, 20, 20] # top, right, bottom, left
    if axis:
      padding = [70, 10, 10, 70]

    axisSize = [45, 65] # [x axis height, y axis width]
    
    xExp = (size - (padding[1] + padding[3])) / xRange
    yExp = (size - (padding[0] + padding[2])) / yRange

    offsetX = padding[3]
    offsetY = padding[0]

    for p in points:
      p.x -= minX
      p.y -= minY
    
    radius = 5
    if image is None:
        image = Image.new("RGB", (size, size))
   
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('arial.ttf', 20)
    if label is not None:
      draw.text((offsetX + xExp * points[0].x - 30, offsetY + yExp * points[0].y + 15), label, fill=fill, font=font)


    if axis:
      ## Axis lines
      # X Axis
      draw.line(((axisSize[1], axisSize[0]), (axisSize[1], size)), fill='white', width=5)
      draw.line(((axisSize[1], axisSize[0]), (size, axisSize[0])), fill='white', width=5)
      for i in range(axisSize[0], 801, 100):
        ## X Axis Labels and Ticks
        if i == axisSize[0]:
          continue
        draw.line(((i, axisSize[0]), (i, axisSize[0] + 5)), fill='white')
        draw.text((i - 22, axisSize[0] - 22), "{:.3f}".format((i - axisSize[0]) / xExp), font=font)

      
      for i in range(axisSize[1], 801, 100):
        ## Y Axis Label and Ticks
        draw.line(((axisSize[1], i), (axisSize[1], i)), fill='white')
        draw.text((1, i - 10), "{:.3f}".format((i - axisSize[1]) / yExp), font=font)

      # Axis Labels
      draw.text((0, size - 20), 'Length', font=font)
      draw.text((size - 70, axisSize[0] - 40), "Width", font=font)
  
    for p in points:
        draw.ellipse((offsetX + xExp * p.x - radius,
                      offsetY + yExp * p.y - radius,
                      offsetX + xExp * p.x + radius,
                      offsetY + yExp * p.y + radius), fill=fill)

    return image, [minX, maxX, minY, maxY]


def plot_path(points, image=None):
    size = 800
    radius = 2
    if image is None:
        image = Image.new("RGB", (size, size))
    exp = size / 15
    draw = ImageDraw.Draw(image)
    for i in range(1, len(points)):
        p1 = points[i-1]
        p2 = points[i]
        for p in [p1, p2]:
            draw.ellipse((exp * p.x - radius,
                          exp * p.y - radius,
                          exp * p.x + radius,
                          exp * p.y + radius), fill='blue')

        draw.line((exp * p1.x, exp * p1.y, exp *
                   p2.x, exp * p2.y), fill='white')

    return image
