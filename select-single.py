import face_recognition
import os
import shutil
import sys
"""

这是一个选择相似图片的程序，含有三个命令行参数

1、需要选择的标准图片的路径
2、输入文件夹的路径
3、输出文件夹的路径
"""

def loadImageList():
    photosName=[]
    list = os.listdir(sys.argv[2])
    for line in list:
        filepath = os.path.join(sys.argv[2], line)
        if os.path.isdir(filepath):
            pass
        else:
            photosName.append(filepath)
    print ("Total Photo Num is "+str(len(photosName)))
    return photosName


def copyFile(src):
    fileName=os.path.basename(src)
    shutil.copyfile(src,sys.argv[3]+os.path.sep+fileName)


def checkEncoding(stardardEncoding,imagePath):
    unknown = face_recognition.load_image_file(imagePath)
    if len(face_recognition.face_locations(unknown))>1:
        pass
    else:
        if len(face_recognition.face_encodings(unknown))<=0:
            print ("Cannot Recognition "+imagePath)
        else:
            unknown_encoding = face_recognition.face_encodings(unknown)[0]
            results = face_recognition.compare_faces([stardardEncoding,], unknown_encoding)
            if results[0]==True:
                copyFile(imagePath)
if __name__ == '__main__':
    if len(sys.argv)<3:
        print ("Require Two Cli Arguments")
        sys.exit(1)
    else:
        standard=face_recognition.load_image_file(sys.argv[1])
        standard_encoding=face_recognition.face_encodings(standard)[0]
        total=loadImageList()
        for item in total:
            checkEncoding(standard_encoding,item)