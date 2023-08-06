#!/usr/bin/python3
import numpy
from fepydas.datatypes.Data import Data1D, Transformation
from fepydas.workers.Fit import SpectralLine, CalibrationFit

def extractCalibration(axis: Data1D, data: Data1D, references, width=10):
  indexes = identifyPeaks(data)
  SpectralFit = SpectralLine()
  peaks = []
  peakErrs = []
  for i, idx in enumerate(indexes[0]):
    if idx+width>len(axis.values) or idx-width<0:
      continue
    x,y = axis.values[idx-width:idx+width], data.values[idx-width:idx+width]
    SpectralFit.initializeAuto(x,y)
    SpectralFit.fit(x,y)
    peaks.append(SpectralFit.result.params["x0"].value)
    peakErrs.append(SpectralFit.result.params["x0"].stderr)
  references = numpy.array(references,dtype=numpy.float64)
  peaks = numpy.array(peaks,dtype=numpy.float64)
  peakErrs = numpy.array(peakErrs,dtype=numpy.float64)
  print("Calibration with ",references,peaks)
  idx = numpy.where(~numpy.isnan(references))[0]
  references = references[idx]
  peaks = peaks[idx]
  peakErrs = peakErrs[idx]
  calib = CalibrationFit()
  calib.initializeAuto()
  calib.fit(peaks,references)#,peakErrs)
  return calib.toTransformation()
  
  
def identifyPeaks(data: Data1D):  
  derivative = numpy.diff(data.values)
  derivative.resize(data.values.shape)
  nonflat = derivative != 0
  zerocrossings = numpy.diff(numpy.sign(derivative)) != 0
  zerocrossings.resize(data.values.shape)
  noiseLevel = data.values > numpy.average(data.values)*10
  
  peaks = zerocrossings*noiseLevel*nonflat
  print("{0} peaks detected".format(numpy.sum(peaks)))
  return numpy.where(peaks)
