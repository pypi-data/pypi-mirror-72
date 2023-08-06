#!/usr/bin/env python3
from sandwichR.sandwich_baseboard import *

class Linetrace():
  def __init__(self):
    pass

  def linetraceInit(self, baseObj = None, wheelType = Wheels.OMNI):
    if baseObj == None:
      self.baseboard = Sandwich_Baseboard(wheelType)
      self.baseboard.portOpen("/dev/ttyAMA0")
      self.baseboard.boardInit()
    else:
      self.baseboard = baseObj

    self.baseboard.setEventHandler(Events.FLOOR_IR_EVENT, self,__floorIrCallback)
    self.state = -1
    self.traceFlag = False
    print("Linetrace mode start")

  def __floorIrCallback(self, data):
    self.state = data.floor_ir_1 << 4 | data.floor_ir_2 << 3 | data.floor_ir_3 << 2 | data.floor_ir_4 << 1 | data.floor_ir_5

  def linetrace(self, speed = 5):
    if self.traceFlag == True:
      print("Already tracing")
      return

    self.traceFlag = True

    traceTH = threading.Thread(target=self.__traceTh, args=(speed,))
    traceTH.daemon = True
    traceTH.start()

    print("Linetrace start")

  def __traceTh(self, speed):
    while self.traceFlag:
      if self.state == 0x11:
        self.baseboard.control(0,0,0)
        self.traceFlag = False
      elif self.state == 0x8:
        self.baseboard.control(0,0,5)
      elif self.state == 0x2:
        self.baseboard.control(0,0,-5)
      else:
        self.baseboard.control(speed,0,0)
      
      time.sleep(0.1)

  def crossline(self, speed = 5, cnt = 1):
    if self.traceFlag == True:
      print("Already tracing")
      return

    self.traceFlag = True

    traceTH = threading.Thread(target=self.__crosslineTh, args=(speed,cnt,))
    traceTH.daemon = True
    traceTH.start()

    print("Crossline start")
  
  def __crosslineTh(self, speed, cnt):
    self.baseboard.control(speed,0,0)
    cross = 0
    
    while cross < cnt:
      if self.state == 0x11:
        cross += 1
      elif self.state == 0x8:
        self.baseboard.control(0,0,5)
      elif self.state == 0x2:
        self.baseboard.control(0,0,-5)
      else:
        self.baseboard.control(speed,0,0)
      
      time.sleep(0.1)
        
    self.baseboard.control(0,0,0)
    self.traceFlag = False

  def right(self, speed = 5):
    if self.traceFlag == True:
      print("Already tracing")
      return

    self.traceFlag = True

    traceTH = threading.Thread(target=self.__rightTh, args=(speed,))
    traceTH.daemon = True
    traceTH.start()

    print("Right corner search start")
    
  def __rightTh(self, speed):
    while self.traceFlag:
      if self.state == 0x18:
        self.baseboard.control(0,0,0)
        self.traceFlag = False
      elif self.state == 0x8:
        self.baseboard.control(0,0,5)
      elif self.state == 0x2:
        self.baseboard.control(0,0,-5)
      else:
        self.baseboard.control(speed,0,0)
      
      time.sleep(0.1)

  def left(self, speed = 5):
    if self.traceFlag == True:
      print("Already tracing")
      return

    self.traceFlag = True

    traceTH = threading.Thread(target=self.__leftTh, args=(speed,))
    traceTH.daemon = True
    traceTH.start()

    print("Left corner search start")
      
  def __leftTh(self, speed):
    while self.traceFlag:
      if self.state == 0x3:
        self.baseboard.control(0,0,0)
        self.traceFlag = False
      elif self.state == 0x8:
        self.baseboard.control(0,0,5)
      elif self.state == 0x2:
        self.baseboard.control(0,0,-5)
      else:
        self.baseboard.control(speed,0,0)
      
      time.sleep(0.1)

  def stop(self):
    self.baseboard.control(0,0,0)
    self.traceFlag = False