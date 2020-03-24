import pickle
import collections
import random
import cv2
import json


def video_length(name):

    cap = cv2.VideoCapture(name)    
    if cap.isOpened():  # 当成功打开视频时cap.isOpened()返回True,否则返回False
        rate = cap.get(5)   # 帧速率
        FrameNumber = cap.get(7)  # 视频文件的帧数
        duration = FrameNumber/rate  # 帧速率/视频总帧数 是时间，除以60之后单位是分钟
    return duration



if __name__ == "__main__":
    file = open("squat2.txt",'rb')
    v1,v2 = pickle.load(file)
    # print(v1)
    # v2 = pickle.load(file)
    textMap = {0:"No squat",1:"squat"}
    valueMap = collections.defaultdict(int)
    nct = 1
    outputjson = {}
    outputjson['heads up'] = "squat"
    outputjson['data'] = []
    for ind,file in enumerate(v1['filename']):
        index = int(file.split("_")[2])
        try:
            valueMap[index] = v1["category"][index]
        except:
            print(nct)
            nct += 1
            print("Not exist people")



    videoCapture=cv2.VideoCapture('Falsetest2_trim.avi')
    duration =  video_length('Falsetest2_trim.avi')
    # duration = 22
    sucess,frame=videoCapture.read()
    ct = 0
    while ct<1823:
        sucess,frame=videoCapture.read()
        current_time = ct/1823*duration
        # if ct<500:
        current_bin = v2[ct][1]
        cv2.putText(frame,textMap[valueMap[ct]],(400,50),cv2.FONT_HERSHEY_PLAIN,2.0,(0,0,255),2)
        # else:
        #     current_bin = random.uniform(0.58,0.98)
        #     cv2.putText(frame,"squat",(400,50),cv2.FONT_HERSHEY_PLAIN,2.0,(0,0,255),2)
        outputjson['data'].append([current_time,current_bin])
        cv2.namedWindow('test Video')    
        try:
            cv2.imshow("test Video",frame)
        except:
            break
        ct += 1
        keycode=cv2.waitKey(1)
        if keycode==27:
            cv2.destroyWindow('test Video')
            videoCapture.release()
            break

    with open("timeLable2.json", 'w') as outfile:
        json.dump(str(outputjson),outfile)
