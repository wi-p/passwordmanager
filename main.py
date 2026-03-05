from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from simpledbmanager import DataBase
from kivymd.uix.list import OneLineListItem
from kivy.clock import Clock

class DBApp(DataBase):
    pass

class HomeScreen(MDScreen):
    def on_enter(self, *args):
        Clock.schedule_once(self.load_passwords)

    def load_passwords(self, *args):
        values = DBApp('appdatabase').readTable('appname','(AppPassowrd)')

        self.ids.lstpwd.clear_widgets()

        for value in values:
            self.ids.lstpwd.add_widget(
                OneLineListItem(text=value[0])
            )

class AddScreen(MDScreen):
    def adicionar(self):
        rg = [self.ids.appname, self.ids.apppassword, self.ids.appusername]
        print(self.children)

        DBApp('appdatabase').insertInTable('AppPassowrd', [rg[0].text,rg[1].text,rg[2].text],'appname, username,password')

        for item in rg:
            item.text = ''

        


class SettingScreen(MDScreen):
    pass

class PassMana(MDApp):
    pass

if __name__ == '__main__':
    PassMana().run()