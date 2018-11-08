"""
CSI4106 Introduction to AI Project
Justin Huynh
Cooper Lawrence
"""
# Requirements:
# Python3, pip install keyboard

import keyboard

class Controller:
    """
    Class for controlling the player's car via keyboard input.
    """
    def __init__(self):
        pass

    def turn_left(self):
        keyboard.press('left') #TODO: Update to press_and_release

    def turn_left_accelerate(self):
        keyboard.press('left, z')

    def turn_right(self):
        keyboard.press('right')

    def turn_right_accelerate(self):
        keyboard.press('right, z')

    def accelerate(self):
        keyboard.press('z')

    def brake(self):
        keyboard.press('x')