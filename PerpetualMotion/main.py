import os

from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiStepper import DPiStepper

from MainScreen import MainScreen
from PerpetualMachine import PerpetualMachine

os.environ['DISPLAY'] = ":0.0"
import sys
sys.path.insert(0, '.venv/src/pidev')
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy.AdminScreen import AdminScreen
from pidev.kivy.DPEAButton import DPEAButton

class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        self.machine = PerpetualMachine()
        Builder.load_file('main.kv')
        sm = ScreenManager()
        print("hi")
        sm.add_widget(MainScreen(self.machine, name='main'))
        sm.add_widget(PassCodeScreen(name='passCode'))
        sm.add_widget(PauseScreen(name='pauseScene'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm


Window.clearcolor = (1, 1, 1, 1)  # White



if __name__ == "__main__":
    # Makes the window auto full screen
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()
    ProjectNameGUI().run()