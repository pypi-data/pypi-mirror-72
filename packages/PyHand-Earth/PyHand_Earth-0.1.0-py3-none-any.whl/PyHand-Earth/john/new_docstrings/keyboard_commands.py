"""
Programmatically controls the mouse and keyboard by
utilizing imported PyAutoGUI automation module.
"""
#import time
import os
import pyautogui   # keyboard/mouse automation module

# Protects against error occuring upon mouse moving
#   beyond corners of screen
pyautogui.FAILSAFE = False

class KeyboardCommands():
    """
    Class that sends commands to control mouse behavior.
    """

    def __init__(self):
        """
        Sets default keyboard/mouse command to a null entry.
        """
        self.__current_command = ''

    def set_command(self, cmd):
        """
        Assigns current command passed to it.
        """
        self.__current_command = cmd

    def send_command(self):
        """
        Presses enter key in Google Earth Pro application.
        """
        os.system("wmctrl -a Google Earth Pro")
        pyautogui.press(self.__current_command)

    def locate_image(self, img):
        """
        Returns (left, top, width, height) of the first
place the passed image file is found and prints appropriate
error message if image not present.
        """
        try:
            location = pyautogui.locateOnScreen(img)
            return location
        except OSError:
            print(img + " Not Found")
            return False

    def click_with_location(self, location):
        """
        Clicks the mouse at the location passed.
        """
        pyautogui.click(location)

    def click_without_location(self):
        """
        Clicks the mouse.
        """
        pyautogui.click()

    def drag_mouse(self, x_offset, y_offset, duration):
        """
        Drags mouse relative to its current position the
parameters passed to it, including time duration.
        """
        pyautogui.dragRel(x_offset, y_offset, duration)

    def move_mouse_to_coords(self, coords):
        """
        Moves mouse cursor to passed coordinates.
        """
        pyautogui.moveTo(coords)
