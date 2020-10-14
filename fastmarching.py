from __future__ import print_function

import SimpleITK as sitk
import sys

if len(sys.argv) < 3:
    print("Usage:", sys.argv[0],
          " <inputImage> <outputImage> <seedX> <seedY> <Sigma>",
          "<SigmoidAlpha> <SigmoidBeta> <TimeThreshold>")
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

smoothing = sitk.CurvatureAnisotropicDiffusionImageFilter()
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

sitk.WriteImage(result, outputFilename)