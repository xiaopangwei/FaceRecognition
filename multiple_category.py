#coding:utf-8
import face_recognition
import os
import shutil
import time
import sys

"""
这是一个多分类的程序，含有两个命令行参数

1、输入文件夹的路径
2、输出文件夹的路径
"""
#inputPath= "/Users/weihuang/Desktop/fbb"
#outputPath= "/Users/weihuang/Desktop/category_result"

inputPath= sys.argv[1]
outputPath= sys.argv[2]
#-1 表示出现一张照片上有多个人
#0 表示无法识别的照片
category_dict={-1:0,-2:0,0:0}
#最多类别编号
maxCategoryCount=0
#已经识别的图片
knownImageEncoding=[]

#具体的调参参数 0-1 之间
# 越小分类的类别越多，越大，分类的数量越小
lowTolerance=0.65
#获取文件列表
def loadImageList():
    photosName=[]
    list = os.listdir(inputPath)
    for line in list:
        filepath = os.path.join(inputPath, line)
        if os.path.isdir(filepath):
            pass
        else:
            photosName.append(filepath)
    print ("Total Photo Num is "+str(len(photosName)))
    return photosName

#拷贝文件
def copyFile(src,index):
    fileName=os.path.basename(src)
    toPath= outputPath + os.path.sep + "type--" + str(index) + os.path.sep
    if os.path.exists(toPath)==False:
        os.makedirs(toPath)
        shutil.copyfile(src,toPath+os.path.sep+fileName)
    else:
        shutil.copyfile(src,toPath+os.path.sep+fileName)

#比较相似度
def checkEncoding(imagePath):
    unknown = face_recognition.load_image_file(imagePath)
    if len(face_recognition.face_locations(unknown))>1:
        category_dict[-1]+=1
        copyFile(imagePath,"MoreThanOne")
    else:
        if len(face_recognition.face_encodings(unknown))<=0:
            category_dict[-2]+=1
            copyFile(imagePath,"CannotRecognition")
        else:
            flag=True
            #如果之前出现过这类图片，Flag=True
            for index,item in enumerate(knownImageEncoding):
                unknownEncoding = face_recognition.face_encodings(unknown)[0]
                results = face_recognition.compare_faces([item,], unknownEncoding,tolerance=lowTolerance)
                #之前已经出现过
                if results[0]:
                    copyFile(imagePath,index)
                    category_dict[index]+=1
                    flag=False
                    break
            if flag:
                # 之前没有出现过
                global maxCategoryCount
                knownImageEncoding.insert(maxCategoryCount, unknownEncoding)
                copyFile(imagePath, maxCategoryCount)
                category_dict[maxCategoryCount] = 1
                maxCategoryCount += 1
#主方法
if __name__ == '__main__':
    if len(sys.argv)<3:
        print ("Require Two Cli Arguments")
        sys.exit(1)
    starttime = time.time()
    total=loadImageList()
    if len(total)<=0:
        pass
    else:
        firstImage=face_recognition.load_image_file(total[0])
        firstImageEncoding=face_recognition.face_encodings(firstImage)[0]
        knownImageEncoding.insert(maxCategoryCount, firstImageEncoding)
        maxCategoryCount+=1

        for index,item in enumerate(total):
            #print (item)
            if index%50==0:
                print ("Now Dealing "+str(index))
            checkEncoding(item)
    endtime =time.time()
    print ("---------------------------------------")
    for k,v in category_dict.items():
        print ("type--"+str(k),str(v))
    print ("Finished classification ,cost "+str(endtime-starttime))