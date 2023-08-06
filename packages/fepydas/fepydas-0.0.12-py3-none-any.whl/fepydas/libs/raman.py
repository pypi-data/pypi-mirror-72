#!/usr/bin/python3

from fepydas.constructors.datareaders.Custom import ASCII_RamanSeries
from fepydas.constructors.datareaders.Generic import Binary
from fepydas.constructors.Plots import SpectrumSeriesPlot
from fepydas.libs.decomposition import Common_LDA_Decomposition
from fepydas.workers.ASCIIWriter import MultiSpectrumWriter
import numpy
import os

def LoadAngleSeries(directory,name,stretching=1,offset=0):
  test = ASCII_RamanSeries(directory)
  test.cutAxis(90,600)
  test.keys.values = test.keys.values*(stretching)+offset
  test.saveBinary(name+".bin")

def GenerateBinaryMaps(inputs,stretching=1):
  for key in inputs.keys():
    LoadAngleSeries(inputs[key][0],key,stretching,offset=inputs[key][1])

def DecomposeMaps(keys,number,iterations,name):
  maps = {}
  for key in keys:
    maps[key]=Binary(key+".bin")
  spectra, transformations = Common_LDA_Decomposition(maps,number,iterations)
  spectra.saveBinary(name+"_Spectra.bin")
  for key in keys:
    transformations[key].saveBinary(key+"_Angles.bin")

def PlotDecomposition(keys,number,name):
  spectra = Binary(name+"_Spectra.bin")
  msw = MultiSpectrumWriter(name+"_Spectra.txt")
  msw.addSpectra(spectra)
  msw.write()
  spectra.data.values = spectra.data.values[:number+1,:]
  spectra.keys.values = spectra.keys.values[:number+1]
  ssp = SpectrumSeriesPlot(spectra)
  ssp.legend()
  ssp.setYLog()
  ssp.save(name+"_Spectra.png")
  for key in keys:
    series = Binary(key+"_Angles.bin")
    msw = MultiSpectrumWriter(key+"_Angles.txt")
    msw.addSpectra(series)
    msw.write()
    #series.data.values = series.data.values[1:number+1,:]
    #series.keys.values = series.keys.values[1:number+1]
    SpectrumSeriesPlot(series).save(key+"_Angles.png")
    SpectrumSeriesPlot(series, polar=True).save(key+"_Angles_Polar.png")

