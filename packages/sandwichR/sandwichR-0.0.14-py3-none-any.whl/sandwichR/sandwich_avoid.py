#!/usr/bin/env python3
from sandwichR.sandwich_baseboard import *

class Condition(enum.Enum):
  IR_LEFT = 1
  IR_RIGHT = 2
  IR_BOTH = 3
  SONAR_10CM = 4
  SONAR_5CM = 5
  SONAR_3CM = 6
  SONAR_1CM = 7

class Avoid():
  def __init__(self):
    pass

  def avoidInit(self, baseObj = None, wheelType = Wheels.OMNI):
    if baseObj == None:
      self.baseboard = Sandwich_Baseboard(wheelType)
      self.baseboard.portOpen("/dev/ttyAMA0")
      self.baseboard.boardInit()
    else:
      self.baseboard = baseObj

    self.baseboard.setEventHandler(Events.FRONT_IR_EVENT, self,__frontIrCallback)
    self.baseboard.setEventHandler(Events.SONAR_EVENT, self,__sonarCallback)
    self.state = -1
    self.dist = 0
    self.avoidFlag = False
    self.stopFlag = False
    print("Avoid mode start")

  def __frontIrCallback(self, data):
    self.state = data.front_ir_1 << 1 | data.front_ir_2

  def __sonarCallback(self, data):
    self.dist = data.distance

  def avoid(self, speed = 5):
    if self.avoidFlag == True:
      print("Already avoiding obstacles")
      return

    self.avoidFlag = True

    avoidTH = threading.Thread(target=self.__avoidTh, args=(speed,))
    avoidTH.daemon = True
    avoidTH.start()

    print("Obstacle avoidance start")

  def __avoidTh(self, speed):
    while self.avoidFlag:
      # left ir check
      if self.state == 0x2:
        self.baseboard.control(0,0,5)
      # right ir check
      elif self.state == 0x1:
        self.baseboard.control(0,0,-5)
      else:
        self.baseboard.control(5,0,0)
      
      time.sleep(0.1)

  def stop(self):
    self.baseboard.control(0,0,0)
    self.avoidFlag = False

  def stopCondition(self, condition):
    if self.avoidFlag == False:
      print("Not in avoiding obstacles")
      return

    if self.stopFlag == True:
      print("Already stop condition check")
      return

    self.stopFlag = True

    avoidTH = threading.Thread(target=self.__stopConditionTh, args=(condition,))
    avoidTH.daemon = True
    avoidTH.start()

  def __stopConditionTh(self, condition):
    while self.stopFlag:
      if Condition(condition) == Condition.IR_LEFT:
        if self.state == 2:
          self.avoidFlag = False
          self.stopFlag = False
      elif Condition(condition) == Condition.IR_RIGHT:
        if self.state == 1:
          self.avoidFlag = False
          self.stopFlag = False
      elif Condition(condition) == Condition.IR_BOTH:
        if self.state == 3:
          self.avoidFlag = False
          self.stopFlag = False
      elif Condition(condition) == Condition.SONAR_10CM:
        if self.dist < 10:
          self.avoidFlag = False
          self.stopFlag = False
      elif Condition(condition) == Condition.SONAR_5CM:
        if self.dist < 5:
          self.avoidFlag = False
          self.stopFlag = False
      elif Condition(condition) == Condition.SONAR_3CM:
        if self.dist < 3:
          self.avoidFlag = False
          self.stopFlag = False
      elif Condition(condition) == Condition.SONAR_1CM:
        if self.dist < 1:
          self.avoidFlag = False
          self.stopFlag = False
      else:
        self.stopFlag = False
        print("Invalid condition. stop check done")