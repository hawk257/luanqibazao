from __future__ import print_function
import pydicom
import numpy as np  #
import matplotlib.pyplot as plt
import sys
import glob
import os
import SimpleITK as sitk
import fastmarching as fstm



dcm = pydicom.dcmread('C:\\Users\\Hawk\\PycharmProjects\\pythonProject\\data\\Dicomfold\\image-000001.dcm')
intercept=dcm.RescaleIntercept
slope=dcm.RescaleSlope
hudata=dcm.pixel_array*slope+intercept
print(hudata)
# plt.hist(hudata.flatten(), bins=80, color='c')
# plt.xlabel("Hounsfield Units (HU)")
# plt.ylabel("Frequency")
# plt.show()
image = dcm.pixel_array

image1=sitk.ReadImage('C:\\Users\\Hawk\\PycharmProjects\\pythonProject\\data\\Dicomfold\\image-000001.dcm')
image_float = sitk.Cast(image1, sitk.sitkFloat32)
# sobel
sobel_op = sitk.SobelEdgeDetectionImageFilter()
sobel_sitk = sobel_op.Execute(image_float)
sobel_sitk = sitk.Cast(sobel_sitk, sitk.sitkInt16)
#sitk.WriteImage(sobel_sitk, "sobel_sitk.mha")
# image[image < 1200] = 0

#plt.imshow(sobel_sitk)
#plt.show()

#nda = sitk.GetArrayFromImage(sobel_sitk).squeeze()
#plt.imshow(nda, cmap=plt.cm.bone)
#plt.show()



if len(sys.argv) < 10:
    print("Usage: {0} <inputImage> <outputImage> <seedX> <seedY> <Sigma> <SigmoidAlpha> <SigmoidBeta> <TimeThreshold>".format(sys.argv[0]))
    sys.exit(1)

inputFilename = sys.argv[1]
outputFilename = sys.argv[2]

seedPosition = (int(sys.argv[3]), int(sys.argv[4]))

sigma = float(sys.argv[5])
alpha = float(sys.argv[6])
beta = float(sys.argv[7])
timeThreshold = float(sys.argv[8])
stoppingTime = float(sys.argv[9])

inputImage = sitk.ReadImage(inputFilename, sitk.sitkFloat32)

print(inputImage)

smoothing = image1 #sitk.CurvatureAnisotropicDiffusionImageFilter()
smoothing.SetTimeStep(0.125)
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
print(result)
#sitk.WriteImage(result, outputFilename)
iii = sitk.GetArrayFromImage(result).squeeze()
plt.imshow(iii, cmap=plt.cm.bone)
plt.show()