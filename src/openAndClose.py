import time
import urx
import enum


def grasp(self, current=None):
    self.robot.set_digital_out(4, 1)
    self.robot.set_digital_out(3, 0)


def release(self, current=None):
    self.robot.set_digital_out(4, 0)
    self.robot.set_digital_out(3, 1)
