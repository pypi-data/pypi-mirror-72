#!/usr/bin/python3
import numpy
from sklearn.decomposition import LatentDirichletAllocation
from fepydas.datatypes.Dataset import SpectrumSeries
from fepydas.datatypes.Data import Data1D, Data2D

#This function performs a common LDA Decomposition on a set of input maps, which have the same axis (e.g. Raman Shift) 

def Common_LDA_Decomposition(inputMaps, numComponents=10, maxIterations=100):
  names = sorted(inputMaps.keys())
  totalIntegrals = {}
  backgroundIntegrals = {}
  correctedIntegrals = {}
  allData = []
  axis = None
  datatype = None

  for name in names:
    totalIntegrals[name] = numpy.sum(inputMaps[name].data.values, axis=0)
    background = numpy.amin(inputMaps[name].data.values,axis=0)
    backgroundIntegrals[name] = background
    #inputMaps[name].data.values-=numpy.amin(background)
    correctedIntegrals[name] = numpy.sum(inputMaps[name].data.values, axis=0)
    if len(allData) == 0:
      allData = inputMaps[name].data.values.copy()
      axis = inputMaps[name].axis
      datatype = inputMaps[name].data.datatype
    else:
      allData = numpy.append(allData, inputMaps[name].data.values, axis=0)
  #allData = numpy.append(allData, allData, axis=0)
  numpy.random.shuffle(allData)
  #allData = numpy.append(allData, numpy.shuffle(allData), axis=0)
  
  LDA = LatentDirichletAllocation(n_components=numComponents, learning_method="batch", max_iter=maxIterations, evaluate_every=5, max_doc_update_iter=10000, verbose=1, n_jobs=-1)
  LDA.fit(allData)
  print("Fit finished with remaining perplexity {0} after {1} iterations.".format(LDA.perplexity(allData), LDA.n_iter_))
  components = LDA.components_

  #Construct new Datasets
  # 1) Spectra
  keys = ["Total_Corrected"]
  data = numpy.atleast_2d(numpy.sum(allData, axis=0))

  for i in range(numComponents):
    keys.append("Component_{0}".format(i+1))
    data = numpy.vstack([data, components[i]])
  for name in names:
    keys.extend([name+"_Total",name+"_Background",name+"_Corrected"])
    data = numpy.vstack([data, totalIntegrals[name], backgroundIntegrals[name], correctedIntegrals[name]])
  spectra = SpectrumSeries(axis, Data1D(keys, None), Data2D(data,datatype))

  # 2) Transformations
  transformations = {}
  for name in names:
    keys=[name+"_Corrected"]
    integral = numpy.sum(inputMaps[name].data.values, axis=1)
    data = numpy.atleast_2d(integral)
    transformation = LDA.transform(inputMaps[name].data.values)
    transformation = transformation.T * integral
    print(numComponents)
    for i in range(numComponents):
      keys.append(name+"_Component_{0}".format(i+1))
      data = numpy.vstack([data, transformation[i,:]])
    transformations[name] = SpectrumSeries(inputMaps[name].keys, Data1D(keys, None), Data2D(data,datatype))

  return spectra, transformations
