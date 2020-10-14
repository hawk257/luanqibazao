import numpy as np  #
import matplotlib.pyplot as plt
import sys
import glob
import os
import SimpleITK as sitk
import fastmarching as fstm

inputfilename ='C:\\Users\\Hawk\\PycharmProjects\\pythonProject\\data\\Dicomfold\\image-000001.dcm'
outputfilename ='c:\\abc.dcm'
seedx = 100
seedy = 100
sigma = 0.5
SigmoidAlpha = -0.3
SigmoidBeta = 2.0
TimeThreshold = 200
StopingTime = 210
fstm(inputfilename, outputfilename, seedx, seedy, sigma, SigmoidAlpha, SigmoidBeta, TimeThreshold, StopingTime)
