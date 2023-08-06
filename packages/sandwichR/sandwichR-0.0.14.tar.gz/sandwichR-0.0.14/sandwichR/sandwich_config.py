#!/usr/bin/env python3
import os.path
import json

class PinData():
  pinNumber = 0
  mode = 0
  request = 0
  moduleCount = 0
  minPulse = 0
  maxPulse = 0

class SetData():
  leftRevice = 0
  rightRevice = 0

class FloorIrCallbackData():
  floor_ir_1 = 0
  floor_ir_2 = 0
  floor_ir_3 = 0
  floor_ir_4 = 0
  floor_ir_5 = 0

class FrontIrCallbackData():
  front_ir_1 = 0
  front_ir_2 = 0

class SonarCallbackData():
  distance = 0

class EventCallbackData(FloorIrCallbackData, FrontIrCallbackData, SonarCallbackData):
  def __init__(self):
    floor_ir_1 = 0
    floor_ir_2 = 0
    floor_ir_3 = 0
    floor_ir_4 = 0
    floor_ir_5 = 0
    front_ir_1 = 0
    front_ir_2 = 0
    distance = 0

class Notes():
  B0  = 31
  C1  = 33
  CS1 = 35
  D1  = 37
  DS1 = 39
  E1  = 41
  F1  = 44
  FS1 = 46
  G1  = 49
  GS1 = 52
  A1  = 55
  AS1 = 58
  B1  = 62
  C2  = 65
  CS2 = 69
  D2  = 73
  DS2 = 78
  E2  = 82
  F2  = 87
  FS2 = 93
  G2  = 98
  GS2 = 104
  A2  = 110
  AS2 = 117
  B2  = 123
  C3  = 131
  CS3 = 139
  D3  = 147
  DS3 = 156
  E3  = 165
  F3  = 175
  FS3 = 185
  G3  = 196
  GS3 = 208
  A3  = 220
  AS3 = 233
  B3  = 247
  C4  = 262
  CS4 = 277
  D4  = 294
  DS4 = 311
  E4  = 330
  F4  = 349
  FS4 = 370
  G4  = 392
  GS4 = 415
  A4  = 440
  AS4 = 466
  B4  = 494
  C5  = 523
  CS5 = 554
  D5  = 587
  DS5 = 622
  E5  = 659
  F5  = 698
  FS5 = 740
  G5  = 784
  GS5 = 831
  A5  = 880
  AS5 = 932
  B5  = 988
  C6  = 1047
  CS6 = 1109
  D6  = 1175
  DS6 = 1245
  E6  = 1319
  F6  = 1397
  FS6 = 1480
  G6  = 1568
  GS6 = 1661
  A6  = 1760
  AS6 = 1865
  B6  = 1976
  C7  = 2093
  CS7 = 2217
  D7  = 2349
  DS7 = 2489
  E7  = 2637
  F7  = 2794
  FS7 = 2960
  G7  = 3136
  GS7 = 3322
  A7  = 3520
  AS7 = 3729
  B7  = 3951
  C8  = 4186
  CS8 = 4435
  D8  = 4699
  DS8 = 4978

class ColorData():
  name = None
  high = []
  low = []

class Sandwich_Config():

  def readConfigFile(self, config_path, pins, sets):
    if config_path.isspace():
      print("Configuration load error : Empty dir")
      return

    if not os.path.isdir(config_path):
      print("Configuration load error : Not dir")
      return

    if not os.path.isfile(config_path + "/pins.config"):
      print("Configuration load error : pin config file not exist")
      return

    if not os.path.isfile(config_path + "/sets.config"):
      print("Configuration load error : setting config file not exist")
      return
    
    self.pinModeParser(config_path, pins)
    self.settingParser(config_path, sets)

  def settingParser(self, config_path, sets):
    f = open(config_path + "/sets.config", 'r')
    configDatas = json.loads(f.read())
    setdatas = configDatas.get('sets')

    if setdatas is None:
      print("Set configuration error : file error")
      return

    sets.leftRevice = setdatas.get('leftRevice')
    sets.rightRevice = setdatas.get('rightRevice')

    f.close()

  def settingWriter(self, sets):
    if not os.path.isdir("/home/pi/Sandwich_res/sets"):
      os.makedirs("/home/pi/Sandwich_res/sets")
      
    f = open("/home/pi/Sandwich_res/sets/sets.config", 'w')

    setdatas = dict()
    setdatas["leftRevice"] = sets.leftRevice
    setdatas["rightRevice"] = sets.rightRevice
    
    json.dump(setdatas, f, indent=4)
    
    f.close()

  def pinModeParser(self, config_path, pins):
    f = open(config_path + "/pins.config", 'r')
    configDatas = json.loads(f.read())
    # configDatas = rapidjson.loads(f.read())
    pindatas = configDatas.get('pins')

    if pindatas is None:
      print("Pin configuration error : file error")
      return

    for data in pindatas:
      pin = PinData()
      
      pinnum = data.get('number')
      if pinnum is None:
        print("Pin configuration error : file syntax error")
        return
      pin.pinNumber = pinnum
      
      mode = data.get('mode')
      if mode is None:
        print("Pin configuration error : file syntax error")
        return
      pin.mode = mode

      pin.moduleCount = data.get('moduleCount')
      pin.minPulse = data.get('minPulse')
      pin.maxPulse = data.get('maxPulse')

      pins[pinnum] = pin
      
    f.close()

  def __init__(self):
    pass

# if __name__ == '__main__':
#   pins = dict()
#   sc = Sandwich_Config()
#   sc.readConfigFile('../pins', pins)

#   for num, data in pins.items():
#     print( num, data.mode )