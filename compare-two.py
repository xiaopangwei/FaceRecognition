import face_recognition
import sys
toleranceMid=0.6
toleranceLow=0.4
toleranceHigh=0.8
"""

这是一个比较两张图片任务是否相同的程序，含有两个命令行参数

1、输入图片文件1的路径
2、输入图片文件2的路径

"""
if __name__ == '__main__':
    if len(sys.argv)<3:
        print ("Require Two Cli Arguments")
        sys.exit(1)
    else:
        standard=face_recognition.load_image_file(sys.argv[1])
        trainImage = face_recognition.load_image_file(sys.argv[2])
        standardEncoding=face_recognition.face_encodings(standard)[0]
        trainImageEncoding=face_recognition.face_encodings(trainImage)[0]
        faceLocations = face_recognition.face_locations(trainImage)
        results=face_recognition.compare_faces([standardEncoding, ], trainImageEncoding, tolerance=toleranceHigh)
        print (str(results))

