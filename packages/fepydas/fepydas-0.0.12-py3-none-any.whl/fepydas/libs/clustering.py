#!/usr/bin/python3
import numpy
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
from sklearn.decomposition import PCA

def performGMM(spectra, kaiser=0.01, clusteringConvergence=0.1, maxClusters=None, withPCA = True, bayesian = False):
  numSpectra = spectra.shape[0]
  numDim = spectra.shape[1]
  if withPCA:
    pca = PCA()
    print("Attempting PCA")
    pca.fit(spectra)
    number = len(pca.explained_variance_ratio_)
    print("PCA found {0}/{1} components".format(number, numDim))
    pcaSpectra = pca.transform(spectra)
  else:
    pcaSpectra = spectra
    number = numDim
  #Bah
  print("Attempting GMM")
  print(pcaSpectra.shape)
  number = 2
  prevProb=-10000
  prevGMM=None
  while True:
    if bayesian:
      gmm = BayesianGaussianMixture(n_components=number)
    else:
      gmm = GaussianMixture(n_components=number)
    gmm.fit(pcaSpectra)
    prob = numpy.average(gmm.score(pcaSpectra))
    print("Components: {0} Average Probability: {1}".format(number, prob))
    if prob-clusteringConvergence<prevProb:
      break
    prevProb = prob
    prevGMM = gmm
    number+=1
    if maxClusters and maxClusters < number:
      break
  number-=1
  gmm = prevGMM
  print("GMM converged with {0} Components".format(len(gmm.means_)))
  resp = gmm.predict_proba(pcaSpectra)
  GMM_Avgspectra = numpy.ndarray(shape=(number+1, numDim))
  GMM_Avgspectra[number,:] = numpy.average(spectra,axis=0)*number
  GMM_Cluster=numpy.argmax(resp,  axis=1)
  GMM_MaxResponsibility=numpy.amax(resp,  axis=1)
  GMM_Projection = numpy.ndarray(shape=(number+1, numSpectra))
  spectraCopy = numpy.ndarray(shape=spectra.shape)
  spectraCopy[:,:] = spectra[:,:]

  for i in range(number):
    GMM_Avgspectra[i,:]=(numpy.average(spectra,  weights=resp[:, i],  axis=0))

  GMM_Avgs = numpy.sum(GMM_Avgspectra,  axis=1)
  for i in range(number):
    square = numpy.dot(GMM_Avgspectra[i],GMM_Avgspectra[i])
    for j in range(numSpectra):
      GMM_Projection[i,j]=numpy.dot(spectra[j],GMM_Avgspectra[i])/square
      temp = GMM_Projection[i,j]*GMM_Avgspectra[i]
      for k in range(i):
        temp -= numpy.dot(temp,GMM_Projection[k,j]*GMM_Avgspectra[k])/numpy.dot(GMM_Projection[k,j]*GMM_Avgspectra[k],GMM_Projection[k,j]*GMM_Avgspectra[k])*GMM_Projection[k,j]*GMM_Avgspectra[k]
      spectraCopy[j,:]-=temp
    print("Component {0}: Weight {1} Integrated Average {2}".format(i,  gmm.weights_[i], GMM_Avgs[i]))
  for j in range(numSpectra):
    GMM_Projection[number,j] = numpy.dot(spectraCopy[j,:],spectraCopy[j,:]) / numpy.dot(spectra[j,:],spectra[j,:])
  GMM_Avgspectra[number,:] = numpy.average(spectraCopy, axis=0)
  #  print("Spectrum {0}: Cluster: {1} Responsibility: {2}".format(i,GMM_Cluster[i], GMM_MaxResponsibility[i]))
  return GMM_Avgspectra, GMM_Cluster, GMM_Projection
