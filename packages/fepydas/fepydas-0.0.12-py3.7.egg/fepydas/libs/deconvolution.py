#!/usr/bin/python3
import numpy.fft as fft
import numpy
import scipy.signal as ss

from multiprocessing.pool import Pool
from lmfit import minimize, Parameters

def epsilonResidual(pars,  signal,  ref):
  epsilon = pars['epsilon'].value
  result = performDeconvolution(signal,  ref,  epsilon)
  contrast = numpy.sum(numpy.abs(result))-numpy.sum(signal)
  result.fill(contrast)
  return result

def findEpsilon(signal,  ref):
  parameters=Parameters()
  parameters.add("epsilon",  value=1)
  result = minimize(epsilonResidual,  parameters,  args=(signal, ref))
  return result.params['epsilon'].value

def performDeconvolution(signal,  ref,  epsilon):
  H = (fft.fft(ref/numpy.sum(ref)))
  ft = fft.fft(signal)
  ft = ft*numpy.conj(H)/(H*numpy.conj(H) + epsilon)
  result =numpy.real(fft.ifft(ft))
  return result

def deconvolve2D(signals, ref):
  reference = numpy.zeros(signals.shape[1])
  for i,x in enumerate(ref):
    reference[i]=x
  epsilon = findEpsilon(signals[0,:], reference) #This assumes similar epsilons can/should be used for all spectra..
  print("Epsilon: {0}".format(epsilon))
  pool = Pool(4)
  jobs = {}
  data = numpy.zeros(signals.shape)
  for i in range(signals.shape[0]):
    jobs[i] = pool.apply_async(performDeconvolution, [signals[i,:], reference, epsilon])
    results = {}
  for i in range(signals.shape[0]):
      data[i,:]=jobs[i].get(1000) 
  return data


def deconvolve(signal, ref, eps=None):
  reference = numpy.zeros(signal.shape)
  for i,x in enumerate(ref):
    reference[i]=x
  if eps:
    epsilon = eps
  else:
    epsilon = findEpsilon(signal,  reference)
  print("Epsilon: {0}".format(epsilon))
  result = performDeconvolution(signal,  reference,  epsilon)
  max = numpy.argmax(signal)
  shift = max - numpy.argmax(result)
  indexes = numpy.roll(numpy.arange(signal.shape[0]), shift)
  return result[indexes]

def convolve(signal, ref):
  return ss.convolve(signal, ref, mode="full")[:len(signal)]

def trimRef(ref):
  maxIdx = numpy.argmax(ref)
  zeroes = numpy.where(ref==0)[0]
  start = 0
  end = zeroes[numpy.where(zeroes > maxIdx)[0][-1]]
  ref = ref[start:end]
  ref = numpy.array(ref,dtype=numpy.float64)
  ref /= ref.sum()
  return ref
