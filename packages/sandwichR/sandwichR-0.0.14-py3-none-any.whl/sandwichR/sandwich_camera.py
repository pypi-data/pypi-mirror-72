from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2
import time
import imutils
import sys
import os
import re
import pickle
import threading
import json
import colorsys
import enum
import pigpio

import numpy as np
from io import BytesIO

import os.path
import pkg_resources

import IPython.display
import PIL.Image
import tflite_runtime.interpreter as tflite

from sandwichR.sandwich_config import *

SERVO1 = 6
SERVO2 = 5
SERVO_MIN = 600
SERVO_MID = 1400
SERVO_MAX = 2200

class CameraEvents(enum.Enum):
  OBJECT_EVENT = 1
  FACE_EVENT = 2
  COLOR_EVENT = 3

class Sandwich_Camera():
    def __init__(self):
        self.streamFlag = False
        self.eventHandlerDic = []

        print("camera module ready")
        
        self.armInit()

    def setEventHandler(self, event, func):
        if event in self.eventHandlerDic:
            print("Event ", event, " already exist lisntener")
        else:
            self.eventHandlerDic[event] = func

    def removeEventHandler(self, event):
        if event in self.eventHandlerDic:
            del self.eventHandlerDic[event]
            print("Event ", event, " is removed")
        else:
            print("Event ", event, " not exist lisntener")
        
    def cameraInit(self, width = 640, height = 480):
        self.cam = cv2.VideoCapture(-1)
        
        if( self.cam.isOpened() == False ):
            print("Unable to read camera feed")
            return
        
        self.cam.set(3,width)
        self.cam.set(4,height)

        self.mosaicFlag = False
        self.mosaicRate = 0

        self.rotateFlag = False
        self.rotateAngle = 0

        self.flipFlag = True
        
        print("camera stream ready")
        
    def __array_to_image(self, a, fmt='jpeg'):
        f = BytesIO()
        PIL.Image.fromarray(a).save(f, fmt)
    
        return IPython.display.Image(data=f.getvalue())
    
    def __get_frame(self):
        ret, frame = self.cam.read()
        
        if( self.flipFlag == True ):
            frame = cv2.flip(frame, 1)
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        return frame
    
    def set_flipflag(self, flag):
        self.flipFlag = flag
        
    def cameraStream(self):
        if( self.streamFlag == True ):
            print("The camera is already working.")
            return
        self.streamFlag = True

        th = threading.Thread(target=self.__cameraStreamTh)
        th.deamon = True
        th.start()

    def __cameraStreamTh(self):
        d = IPython.display.display("", display_id=1)
        d2 = IPython.display.display("", display_id=2)
        while self.streamFlag:
            t1 = time.time()
            frame = self.__get_frame()

            if self.mosaicFlag == True:
                frame = cv2.resize(frame, (self.cam.get(3)//self.mosaicRate, self.cam.get(4)//self.mosaicRate))
                frame = cv2.resize(frame, (self.cam.get(3), self.cam.get(4)))

            if self.rotateFlag == True:
                m1 = cv2.getRotationMatrix2D((self.cam.get(3)/2, self.cam.get(4)/2), self.rotateAngle, 1)
                frame = cv2.warpAffine(frame, m1, (self.cam.get(3),self.cam.get(4)))

            im = self.__array_to_image(frame)

            d.update(im)
            t2 = time.time()
            s = f"""{int(1/(t2-t1))} FPS"""
            d2.update( IPython.display.HTML(s) )

        IPython.display.clear_output()
        print ("Stream stopped")
            
    def cameraOff(self):
        if( self.streamFlag == False ):
            print("The camera is already stopped.")
            return
        self.streamFlag = False

        self.cam.release()
        time.sleep(1)

        print("Camera off")

    def mosaicMode(self, rate = 0):
        self.mosaicRate = rate

        if self.mosaicRate == 0:
            self.mosaicFlag = False
        else:
            self.mosaicFlag = True

    def rotateMode(self, angle = 90):
        self.rotateAngle += int(angle)

        if self.rotateAngle // 360 == 0:
            self.rotateFlag = False
        else:
            self.rotateFlag = True
        
    def tensorflowInit(self):
        if not os.path.isdir("/home/pi/Sandwich_res"):
            res_dir = pkg_resources.resource_filename(__package__,"res")
        else:
            res_dir = "/home/pi/Sandwich_res"
        
        model_file = res_dir + "/tensorflow/detect.tflite"
        label_file = res_dir + "/tensorflow/labelmap.txt"
        self.min_threshold = 0.5

        self.labels = self.__load_labels(label_file)
        self.interpreter = tflite.Interpreter(model_path=model_file)
        self.interpreter.allocate_tensors()
        _, self.input_height, self.input_width, _ = self.interpreter.get_input_details()[0]['shape']
        
        print("Tensorflow ready")
    
    def __load_labels(self, path):
        labels = {}
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
      
            for row_number, content in enumerate(lines):
                pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
                if( len(pair) == 2 and pair[0].strip().isdigit()):
                    labels[int(pair[0])] = pair[1].strip()
                else:
                    labels[row_number] = pair[0].strip()
        return labels
        
    def __set_input_tensor(self, interpreter, input_image):
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:,:] = np.uint8(input_image)

    def __get_output_tensor(self, interpreter, index):
        output_details = interpreter.get_output_details()[index]
        tensor = np.squeeze(interpreter.get_tensor(output_details['index']))

        return tensor

    def __detect_object(self, interpreter, detect_image, threshold):
        self.__set_input_tensor(interpreter, detect_image)
        interpreter.invoke()

        boxes = self.__get_output_tensor(interpreter, 0)
        classes = self.__get_output_tensor(interpreter, 1)
        scores = self.__get_output_tensor(interpreter, 2)
        count = int(self.__get_output_tensor(interpreter, 3))

        results = []
        for i in range(count):
            if scores[i] >= threshold:
                result = {
                  'bounding_box':boxes[i],
                  'class_id':classes[i],
                  'score':scores[i]
                }
                results.append(result)
    
        return results
        
    def tensorflowStream(self):
        if( self.streamFlag == True ):
            print("The camera is already working.")
            return
        self.streamFlag = True

        th = threading.Thread(target=self.__tensorflowStreamTh)
        th.deamon = True
        th.start()

    def __tensorflowStreamTh(self):
        d = IPython.display.display("", display_id=1)
        d2 = IPython.display.display("", display_id=2)
        while self.streamFlag:
            t1 = time.time()
            frame = self.__get_frame()
            image_resized = cv2.resize(frame, (self.input_width,self.input_height))
            
            input_data = np.expand_dims(image_resized, axis=0)
            
            results = self.__detect_object(self.interpreter, input_data, 0.5)
            
            for i in range(len(results)):
                if( (results[i]['score'] > self.min_threshold) and ( results[i]['score'] <= 1.0) ):
                    # draw rect
                    ymin, xmin, ymax, xmax = results[i]['bounding_box']
                    xmin = int(xmin * 640)
                    xmax = int(xmax * 640)
                    ymin = int(ymin * 480)
                    ymax = int(ymax * 480)

                    cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10,255, 0), 2)

                    # draw label
                    label = '%s: %d%%' % (self.labels[results[i]['class_id'] ], int(results[i]['score']*100))
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    label_ymin = max(ymin, labelSize[1] + 10)
        
                    cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2, cv2.LINE_AA)

                    if self.eventHandlerDic.get(CameraEvents.OBJECT_EVENT):
                        self.eventHandlerDic[CameraEvents.OBJECT_EVENT](self.labels[results[i]['class_id'] ])
            
            im = self.__array_to_image(frame)
            d.update(im)
            t2 = time.time()
            s = f"""{int(1/(t2-t1))} FPS"""
            d2.update( IPython.display.HTML(s) )

        IPython.display.clear_output()
        print ("Object detection stopped")
            
    def tensorflowOff(self):
        if( self.streamFlag == False ):
            print("The camera is already stopped.")
            return    
        self.streamFlag = False

        self.cam.release()
        time.sleep(1)

        print("Tensorflow off")
        
    def facedetectorInit(self):
        if not os.path.isdir("/home/pi/Sandwich_res"):
            res_dir = pkg_resources.resource_filename(__package__,"res")
        else:
            res_dir = "/home/pi/Sandwich_res"
            
        self.face_detector = res_dir + "/lbph/haarcascade_frontalface_alt.xml"
        self.face_datapath = res_dir + "/lbph/"
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        self.detect_flag = False
        self.savedata_flag = False
        self.saveface_name = "None"
        self.during_recognite = False
        
        self.initDataset()
        with open(self.face_datapath + 'data.pickle', 'rb') as dataFile:
            self.recoDatas = pickle.load(dataFile)
        
        if os.path.isfile(config_path + 'trainer/trainer.yml'):
            self.__loadModel()
        else:
            self.__trainModel()
        print("Facedetector ready")
    
    def __loadModel(self):            
        try:
            print("LBPH model found")
            self.recognizer.read(config_path + 'trainer/trainer.yml')
        except:
            print("LBPH model read failed")
            
        print("LBPH model loaded")
        
    def __getFaceData(self, path):
        datas = 0

        with open(self.face_datapath + 'data.pickle', 'rb') as dataFile:
            datas = pickle.load(dataFile)
    
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

        faces = []
        ids = []

        for imagePath in imagePaths:
            PIL_img = pil.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')

            name = os.path.split(imagePath)[-1].split('_')[0]
            id = -1
            for data in datas:
                if datas[data] == name:
                    id = data

            faces.append(img_numpy)
            ids.append(id)

        return faces, ids
    
    def __trainModel(self):
        faces, ids = self.__getFaceData(self.face_datapath + 'faces')
        self.recognizer.train(faces, np.array(ids))

        if not os.path.isdir(self.face_datapath + 'trainer'):
            os.makedirs(self.face_datapath + 'trainer')
        self.recognizer.save(self.face_datapath + 'trainer/trainer.yml')
        
        print("Face trained")
        
    def facedetectorStream(self):
        if( self.streamFlag == True ):
            print("The camera is already working.")
            return
        self.streamFlag = True

        th = threading.Thread(target=self.facedetectorStreamTh)
        th.deamon = True
        th.start()

    def facedetectorStreamTh(self):
        d = IPython.display.display("", display_id=1)
        d2 = IPython.display.display("", display_id=2)
        while self.streamFlag:
            if self.during_recognite == True:
                continue
        
            t1 = time.time()
            frame = self.__get_frame()
            frame = self.__facerecognition(frame)
            im = self.__array_to_image(frame)
            
            d.update(im)
            t2 = time.time()
            s = f"""{int(1/(t2-t1))} FPS"""
            d2.update( IPython.display.HTML(s) )
          
        IPython.display.clear_output()
        print ("Facedetect stopped")

    def __facerecognition(self, image):
        self.during_recognite = True
        name = "Unknown"
        x = 0
        y = 0
        w = 0
        h = 0

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray, 1.2, 5, minSize=(40,40))

        for( x, y, w, h ) in faces:
            Id, conf = self.recognizer.predict(gray[y:y+h, x:x+w])
            cv2.rectangle(image, (x,y), (w,h), (10,255, 0), 2)
                           
            # draw label
            label = '%s: %d' % (self.recoDatas[Id], int(conf))
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            label_ymin = max(y, labelSize[1] + 10)
        
            cv2.putText(image, label, (x, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2, cv2.LINE_AA)

            if self.eventHandlerDic.get(CameraEvents.FACE_EVENT):
                self.eventHandlerDic[CameraEvents.FACE_EVENT](self.recoDatas[Id])
            
        self.during_recognite = False
        return image
    
    def facedetectorOff(self):
        if( self.streamFlag == False ):
            print("The camera is already stopped.")
            return
        self.streamFlag = False

        self.cam.release()
        time.sleep(1)

        print("Facedetect off")
        
    def faceRegistrationStream(self):
        if( self.streamFlag == True ):
            print("The camera is already working.")
            return
        self.streamFlag = True

        th = threading.Thread(target=self.__faceRegistrationStreamTh)
        th.deamon = True
        th.start()
        
    def __faceRegistrationStreamTh(self):
        if not os.path.isdir("/home/pi/Sandwich_res"):
            res_dir = pkg_resources.resource_filename(__package__,"res")
        else:
            res_dir = "/home/pi/Sandwich_res"
            
        guide = cv2.imread( res_dir + "/faceguide.png" )
        
        self.saveface_name = None
        self.registerFlag = False
        self.registerCnt = 0
        
        if not os.path.isdir(self.face_datapath + 'faces'):
            os.makedirs(self.face_datapath + 'faces')
            
        self.initDataset()
        
        d = IPython.display.display("", display_id=1)
        d2 = IPython.display.display("", display_id=2)
        
        while self.streamFlag:
            if self.during_recognite == True:
                continue
        
            t1 = time.time()
            frame = self.__get_frame()
            
            if self.registerFlag == True:
                self.makeFaceData(frame)
            
            frame = cv2.add(frame, guide)
            im = self.__array_to_image(frame)
            
            d.update(im)
            t2 = time.time()
            s = f"""{int(1/(t2-t1))} FPS"""
            d2.update( IPython.display.HTML(s) )
          
        IPython.display.clear_output()
        print ("Facedetect stopped")
        
    def makeFaceData(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray, 1.2, 5, minSize=(40,40))

        for( x, y, w, h ) in faces:
            face_image = gray[y:y+h, x:x+w]
            self.saveFaceData(face_image)
        
        self.registerCnt += 1
        
        if self.registerCnt >= 50:
            self.registerFlag = False
            
    def saveFaceData(self, image):
        if not os.path.isdir(self.face_datapath + 'faces'):
            os.makedirs(self.face_datapath + 'faces')
        filename = self.face_datapath + 'faces/'

        if self.saveface_name is not None:
            number = 0
            lists = os.listdir(self.face_datapath + 'faces')
            for list in lists:
                if self.saveface_name in list:
                    number += 1
      
            filename = filename + self.saveface_name + '_' + str(number) + '.jpg'
            cv2.imwrite(filename, image)
    
    def faceRegistrationStart(self, name):
        self.saveface_name = name
        self.registerFlag = True
        self.registerCnt = 0
    
    def faceRegistrationOff(self):
        if( self.streamFlag == False ):
            print("The camera is already stopped.")
            return
        self.streamFlag = False

        self.cam.release()
        time.sleep(1)

        print("Faceregistration off")
        
    def initDataset(self):
        datas = 0
        write = False

        if not os.path.exists(self.face_datapath + "data.pickle"):
            with open(self.face_datapath + 'data.pickle', 'wb') as dataFile:
                pickle.dump({}, dataFile, protocol=pickle.HIGHEST_PROTOCOL)

        with open(self.face_datapath + 'data.pickle', 'rb') as dataFile:
            datas = pickle.load(dataFile)
            names = list(datas.values())

            if not self.saveface_name in names and self.saveface_name is not None:
                number = len(datas)
                datas[number] = self.saveface_name
                write = True
        
        if write:
            with open(self.face_datapath + 'data.pickle', 'wb') as dataFile:
                pickle.dump(datas, dataFile, protocol=pickle.HIGHEST_PROTOCOL)
    
    def colorRecognitionInit(self):
        self.colorDataSet = {}

        if not os.path.isdir("/home/pi/Sandwich_res"):
            res_dir = pkg_resources.resource_filename(__package__,"res")
        else:
            res_dir = "/home/pi/Sandwich_res"
        
        color_file = res_dir + "/color/colorvalue.config"
        label_file = res_dir + "/color/colorguide.png"
        
        if not os.path.isfile(color_file):
            print("Color data init error : Not exist file")
            return

        f = open(color_file, 'r')
        configDatas = json.loads(f.read())
        colors = configDatas.get('colors')

        if colors is None:
            print("Color data init error : color name syntax error")
            return

        for name in colors:
            data = configDatas.get(name)
            
            if data is None:
                print("Color data init error : ", name, " color data syntax error")
                return

            cd = ColorData()

            cd.name = name
            cd.high = data.get('high')
            cd.low = data.get('low')

            self.colorDataSet[name] = cd

    def colorRecognitionStream(self):
        if( self.streamFlag == True ):
            print("The camera is already working.")
            return
        self.streamFlag = True

        th = threading.Thread(target=self.__colorRecognitionStreamTh)
        th.deamon = True
        th.start()
        
    def __colorRecognitionStreamTh(self):
        if not os.path.isdir("/home/pi/Sandwich_res"):
            res_dir = pkg_resources.resource_filename(__package__,"res")
        else:
            res_dir = "/home/pi/Sandwich_res"

        guide = cv2.imread( res_dir + "/color/colorguide.png" )

        roi = None
        color = "?"
        d = IPython.display.display("", display_id=1)
        d2 = IPython.display.display("", display_id=2)
        d3 = IPython.display.display("", display_id=3)

        while self.streamFlag:        
            t1 = time.time()
            frame = self.__get_frame()

            roi = frame[156:323, 235:404]
            roi = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)

            for name, data in self.colorDataSet.items():
                mask = cv2.inRange(roi, np.array( [data.low[0],data.low[1],data.low[2]] ), np.array( [data.high[0],data.high[1],data.high[2]] ) )
                if cv2.countNonZero(mask) > 4000:
                    color = name
                    break
                else:
                    color = "?"

            frame = cv2.add(frame, guide)
            im = self.__array_to_image(frame)

            d.update(im)
            t2 = time.time()
            s = f"""{int(1/(t2-t1))} FPS"""
            d2.update( IPython.display.HTML(s) )
            d3.update( color )

            if self.eventHandlerDic.get(CameraEvents.COLOR_EVENT):
                self.eventHandlerDic[CameraEvents.COLOR_EVENT](color)
          
        IPython.display.clear_output()
        print ("Color recognition stopped")

    def colorRecognitionOff(self):
        if( self.streamFlag == False ):
            print("The camera is already stopped.")
            return
        self.streamFlag = False

        self.cam.release()
        time.sleep(1)

        print("Color recognition off")
    
    def colorRegistrationInit(self):
        self.colorDataSet = {}
        self.registFlag = False
        self.registName = None

        if not os.path.isdir("/home/pi/Sandwich_res"):
            res_dir = pkg_resources.resource_filename(__package__,"res")
        else:
            res_dir = "/home/pi/Sandwich_res"
            
        color_file = res_dir + "/color/colorvalue.config"
        
        if not os.path.isfile(color_file):
            print("Color data init error : Not exist file")
            return

        f = open(color_file, 'r')
        configDatas = json.loads(f.read())
        colors = configDatas.get('colors')

        if colors is None:
            print("Color data init error : color name syntax error")
            return

        for name in colors:
            data = configDatas.get(name)
            
            if data is None:
                print("Color data init error : ", name, " color data syntax error")
                return

            cd = ColorData()

            cd.name = name
            cd.high = data.get('high')
            cd.low = data.get('low')

            self.colorDataSet[name] = cd
            
    def colorRegistrationStream(self):
        if( self.streamFlag == True ):
            print("The camera is already working.")
            return
        self.streamFlag = True

        th = threading.Thread(target=self.__colorRegistrationStreamTh)
        th.deamon = True
        th.start()

    def __colorRegistrationStreamTh(self):
        if not os.path.isdir("/home/pi/Sandwich_res"):
            res_dir = pkg_resources.resource_filename(__package__,"res")
        else:
            res_dir = "/home/pi/Sandwich_res"
            
        guide = cv2.imread( res_dir + "/color/colorguide.png" )
        
        regimg = np.zeros((100,100,3), np.uint8)
        roi = None
        d = IPython.display.display("", display_id=1)
        d2 = IPython.display.display("", display_id=2)
        d3 = IPython.display.display("", display_id=3)
        d4 = IPython.display.display("", display_id=4)
        
        while self.streamFlag:
            t1 = time.time()
            frame = self.__get_frame()

            roi = frame[156:323, 235:404]
            avr = roi.mean(axis=0).mean(axis=0)
            
            frame = cv2.add(frame, guide)
            im = self.__array_to_image(frame)
            
            regimg[:] = avr
            im2 = self.__array_to_image(regimg)
            
            if self.registFlag == True:
                hsv = colorsys.rgb_to_hsv(avr[0], avr[1], avr[2])
                
                cd = ColorData()
                cd.name = self.registName
                cd.high = [ round(360 * hsv[0])/2 + 5, 255, 255 ]
                cd.low = [ round(360 * hsv[0])/2 - 5, 100, 125 ]
                
                self.colorDataSet[cd.name] = cd
                self.registFlag = False

                self.__colorDataSetWrite()
            
            d.update(im)
            t2 = time.time()
            s = f"""{int(1/(t2-t1))} FPS"""
            d2.update( IPython.display.HTML(s) )
            
            d3.update(im2)
            d4.update(colorsys.rgb_to_hsv(avr[0], avr[1], avr[2]))
          
        IPython.display.clear_output()
        print ("Color regist stopped")

    def colorRegistrationStart(self,name):
        self.registFlag = True
        self.registName = name
        
    def colorRegistrationOff(self):
        if( self.streamFlag == False ):
            print("The camera is already stopped.")
            return
        self.streamFlag = False

        self.cam.release()
        time.sleep(1)

        print("Color regist off")
        
    def __colorDataSetWrite(self):
        res_dir = "/home/pi/Sandwich_res"
        color_file = res_dir + "/color/colorvalue.config"

        data = {}
        colors = []
        cdata = {}

        for key in self.colorDataSet:
            colors.append(key)

            cdata = {}
            cdata['high'] = self.colorDataSet[key].high
            cdata['low'] = self.colorDataSet[key].low

            data[key] = cdata

        data['colors'] = colors
        jdata = json.dumps(data, indent=4)
        f = open(color_file, "w")
        f.write(jdata)
        f.close()

        print("Color regist done. please call 'colorRegistrationInit' function.")

    def armInit(self):
        self.pigpio = None
        self.horizonDuty = 1400
        self.verticalDuty = 1400
        self.horizonAngle = 90
        self.verticalAngle = 90
        
        self.curHorizonDuty = 0
        self.curVerticalDuty = 0

        if not os.system('sudo pigpiod -p 5050') == 0:
            print("camera arm module init error. 5050 port should not be in use.")
        else:
            self.pigpio = pigpio.pi('localhost',5050)

        if self.pigpio == None:
            print("camera arm module init error.")
        else:
            th = threading.Thread(target=self.__armControlTh)
            th.deamon = True
            th.start()

    def setArmAngle(self, vertical = None, horizontal = None):
        if vertical == None:
            vertical = self.verticalAngle
        if horizontal == None:
            horizontal = self.horizonAngle

        self.horizonAngle = horizontal
        self.verticalAngle = vertical

        self.horizonDuty = self.__angle2duty( self.horizonAngle )
        self.verticalDuty = self.__angle2duty( self.verticalAngle )

    def changeArmAngle(self, vertical = 0, horizontal = 0):
        self.horizonAngle = self.horizonAngle + horizontal
        self.verticalAngle = self.verticalAngle + vertical

        self.horizonDuty = self.__angle2duty( self.horizonAngle )
        self.verticalDuty = self.__angle2duty( self.verticalAngle )

    def __armControlTh(self):
        print('camera arm module ready')

        while True:
            time.sleep(0.01)

            if self.curHorizonDuty != self.horizonDuty:
                self.pigpio.set_servo_pulsewidth(SERVO1, self.horizonDuty)
                self.curHorizonDuty = self.horizonDuty

            if self.curVerticalDuty != self.verticalDuty:
                self.pigpio.set_servo_pulsewidth(SERVO2, self.verticalDuty)
                self.curVerticalDuty = self.verticalDuty

        print('camera arm module stopped')

    def __angle2duty(self, angle):
        angle = self.__contains(angle, 0, 180)
        duty = angle * (SERVO_MAX - SERVO_MIN) / 180 + SERVO_MIN

        return duty

    def __contains(self, input, min, max):
        var = input

        if input > max:
            var = max
        
        if input < min:
            var = min

        return var