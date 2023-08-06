import os

class DirectoryLoader:
  def __init__(self, constructor):
    self.constructor = constructor
    self.loaded = {}

  def loadFromDirectory(self, directory, filter_function):
    files = os.listdir(directory)
    for filename in sorted(files):
      if filter_function(filename):   
        self.loaded[filename] = self.constructor(os.path.join(directory,filename))

  def callFunction(self, function, *args):
    for key in self.loaded.keys():
      getattr(self.loaded[key], function)(*args)

  def getList(self):
    return list(self.loaded.values())

  def getKeys(self):
    return list(self.loaded.keys())
