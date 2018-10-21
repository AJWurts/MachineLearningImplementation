

def load_data():
  data = []
  with open("chronic_kidney_disease_full.1.csv", 'r') as theFile:
      lines = theFile.read().split('\n')
      for i, l in enumerate(lines):
          current = []
          for attr in l.split(',')[:25]:
              current.append(float(attr))
          data.append(current)

  return data