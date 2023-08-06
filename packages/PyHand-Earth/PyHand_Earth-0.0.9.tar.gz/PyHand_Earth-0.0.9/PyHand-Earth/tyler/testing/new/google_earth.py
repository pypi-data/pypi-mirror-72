import os
import time
import subprocess
import psutil
from keyboard_commands import KeyboardCommands

class GoogleEarth():

    def __init__(self):
        self.current_command = ''
        self.keyboard_commands = KeyboardCommands()
        self.screen_position = []
        self.resolution = ''

    def check_process_running(self, process_name):
        #Check if there is any running process that contains the given name processName.
        #Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def initialize_google_earth(self):

        #Checking if Google Earth is already running
        if self.check_process_running('google-earth'):
            self.start_google_earth()

        else:
            #Start Google Earth if it is not already running and resize window
            os.system("nohup google-earth-pro </dev/null >/dev/null 2>&1 &")
            time.sleep(2)
            self.start_google_earth()

        sidebar_coords = self.keyboard_commands.locate_image('clicked_sidebar.png')

        if sidebar_coords:
            self.keyboard_commands.click_with_location(sidebar_coords)
            time.sleep(2)

            # These don't need to be executed immediately after the toolbar is disabled
            # now because the user has to click start before commands start being sent.
            # Possibly move this to after user has clicked start video???

            # self.keyboard_commands.drag_mouse(80, 200, 1)
            # self.keyboard_commands.click_without_location()

        else:
            os.system("wmctrl -a Google Earth Pro")
            sidebar_coords = self.keyboard_commands.locate_image('unclicked_sidebar.png')
            if sidebar_coords:
                self.keyboard_commands.move_mouse_to_coords(sidebar_coords)

    def start_google_earth(self):
        self.set_screen_resolution()
        comm = "wmctrl -r 'Google Earth' -e 0," + str(int(self.resolution[0])) + "," + \
                str(int(self.resolution[1])) + "," + str(self.screen_position[0]) + "," + \
                str(self.screen_position[1])
        os.system(comm)
        time.sleep(2)

    def set_screen_resolution(self):
        output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4', shell=True, stdout=subprocess.PIPE).communicate()[0]
        self.resolution = output.split()[0].split(b'x')

        self.screen_position.append(int((int(self.resolution[0])*(2/5))))
        self.screen_position.append(int((int(self.resolution[1])*(1/2))))
        self.resolution[0] = (int(self.resolution[0])/2)-(self.screen_position[0]/2)
        self.resolution[1] = (int(self.resolution[1])/2)-(self.screen_position[1]/2)

    def get_screen_resolution(self):
        return self.resolution

    def get_screen_position(self):
        return self.screen_position

    def close_earth(self):
        os.system("wmctrl -c Google Earth Pro")
