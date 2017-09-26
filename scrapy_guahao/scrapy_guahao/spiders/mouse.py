#coding=utf-8
from pymouse import PyMouse

def click():
      m = PyMouse()
      m.click(81,52)#移动并且在xy位置点击
