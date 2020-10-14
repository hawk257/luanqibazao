#!/usr/bin/env python

from __future__ import print_function

import SimpleITK as sitk
import sys
import os
import matplotlib.pyplot as plt



inputFilename = 'C:\\Users\\Hawk\\PycharmProjects\\pythonProject\\data\\Dicomfold\\image-000005.dcm'
#outputFilename = ''

seedPosition = (int(100), int(100))

sigma = float(0.5)
alpha = float(-0.3)
beta = float(1.0)
timeThreshold = float(200)
stoppingTime = float(210)

inputImage = sitk.ReadImage(inputFilename, sitk.sitkFloat32)
print(inputImage)


smoothing = sitk.CurvatureAnisotropicDiffusionImageFilter()
smoothing.SetTimeStep(0.03)
smoothing.SetNumberOfIterations(5)
smoothing.SetConductanceParameter(9.0)
smoothingOutput = smoothing.Execute(inputImage)


gradientMagnitude = sitk.GradientMagnitudeRecursiveGaussianImageFilter()
gradientMagnitude.SetSigma(sigma)
gradientMagnitudeOutput = gradientMagnitude.Execute(smoothingOutput)


sigmoid = sitk.SigmoidImageFilter()
sigmoid.SetOutputMinimum(0.0)
sigmoid.SetOutputMaximum(1.0)
sigmoid.SetAlpha(alpha)
sigmoid.SetBeta(beta)
sigmoid.DebugOn()
sigmoidOutput = sigmoid.Execute(gradientMagnitudeOutput)


fastMarching = sitk.FastMarchingImageFilter()

seedValue = 0
trialPoint = (seedPosition[0], seedPosition[1], seedValue)


fastMarching.AddTrialPoint(trialPoint)

fastMarching.SetStoppingValue(stoppingTime)

fastMarchingOutput = fastMarching.Execute(sigmoidOutput)


thresholder = sitk.BinaryThresholdImageFilter()
thresholder.SetLowerThreshold(0.0)
thresholder.SetUpperThreshold(timeThreshold)
thresholder.SetOutsideValue(0)
thresholder.SetInsideValue(255)

result = thresholder.Execute(fastMarchingOutput)

#sitk.WriteImage(result, outputFilename)
iii = sitk.GetArrayFromImage(result).squeeze()
plt.imshow(iii, cmap=plt.cm.bone)
plt.show()