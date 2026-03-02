from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen 


class Manager(ScreenManager):
    pass 

class StartScreen(Screen):
    pass
        

class PassMana(MDApp):
    def build(self):
        return StartScreen()
    
if __name__ == '__main__':
    PassMana().run()