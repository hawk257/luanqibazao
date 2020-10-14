# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pydicom
import numpy as np  #
import matplotlib.pyplot as plt
import sys
import glob
import os

#pydicom 用于dicom文件读取
#numpy   进行科学计算
#matplotlib 数据可视化，用于dicom文件的可视化
#sys  python解释器
#glob  输入文件路径，返回文件列表

#读取单个切片文件
def readslice(patientfile):
    dcm = pydicom.dcmread(patientfile)
    return dcm

#正则表达式提取关键信息，
def load_information(info):
    print('ok')
    return

#具体处理切片，参数为361张切片具体内容
def analysisslices(slices):
    basicinfo = load_information(slices[0])
    slices.sort(key=lambda x: float(x.ImagePositionPatient[2])) #以z轴进行排序
    slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2]) #提取切片厚度
    print(slice_thickness)
    return

#提取所有切片信息
def readallslice(path,pname):#pname为患者标号
    npath = path + '\\' + pname
    print(npath)
    #加载所有切片
    slicesdir = os.listdir(npath)
    print(slicesdir)
    slices = [readslice(npath+'\\'+s) for s in slicesdir]
    analysisslices(slices) #分析患者切片

#读取所有患者影像文件,并加载所有切片，获取切片相关信息，按切片z轴方向进行排序,调用readallslice
def readalldata(path):
    allpatients=os.listdir(path)   #allpatients 存储了所有患者数量及标号
    allpatients.sort()
    print(allpatients)
    # 制作一个循环，重复操作所有患者
    for p in allpatients:
          readallslice(path,p)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = '.\\data\\'
    readalldata(path)



