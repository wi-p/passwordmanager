from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from simpledbmanager import DataBase
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivy.metrics import dp
from functools import partial
from kivymd.uix.dialog import MDDialog
from kivy.core.clipboard import Clipboard
from widgets import BoxPasswords


class DBApp(DataBase):
    pass


class HomeScreen(MDScreen):
    dialog = None 

    def on_enter(self, *args):
        Clock.schedule_once(self.load_passwords)
    
    def deletePassword(self, box, instance):
        DBApp('appdatabase').deleteItemTable('AppPassowrd', 'id', box.id)
        self.ids.lstpwd.remove_widget(box)

    def copyItem(self, value):
        content = value
        
        pass # Função para copiar item ao toca-lo.

    def load_passwords(self, *args):
        values = DBApp('appdatabase').readTable('AppPassowrd', '*')

        self.ids.lstpwd.clear_widgets()

        for value in values:
            box = BoxPasswords()
            box.bind(on_touch_down=lambda objeto=box: self.openDialog(objeto))

            box.id = str(value[0])
            box.size_hint_y = None
            box.height = dp(50)
            box.spacing = dp(10)
            btn = MDIconButton(icon='trash-can', md_bg_color = 'red', id = str(value[0]))

            btn.bind(on_release = partial(self.deletePassword, box))

            box.add_widget(MDLabel(text = str(value[0]), size_hint_x = None, width = dp(40)))
            box.add_widget(MDLabel(text = value[1]))
            box.add_widget(MDLabel(text = value[2]))
            box.add_widget(MDLabel(text = value[3]))
            box.add_widget(btn)

            self.ids.lstpwd.add_widget(
                box
            )       
    

    def openDialog(self, bx):
        print(bx)

        if not self.dialog :
            self.dialog = MDDialog(
                text = 'Copy infos',
                buttons = [
                    MDFlatButton(text = 'Copy password'), 
                    MDFlatButton(text = 'Copy username', on_release = partial(self.copyPassword, instance.children)),
                    MDFlatButton(text = 'Dismiss', on_release = self.closeDialog),
                ]
            )

            self.dialog.open()

    # I have to make it 
    def copyPassword(self, label, *args):
        #Clipboard.copy(label)
        print()
        print(label[1].text)
        print(label[2].text)
        
        
    def closeDialog(self, obj):
        self.dialog.dismiss()
        
        self.dialog = None 

class AddScreen(MDScreen):
    def adicionar(self):
        rg = [self.ids.appname, self.ids.apppassword, self.ids.appusername]

        DBApp('appdatabase').insertInTable('AppPassowrd', [rg[0].text,rg[1].text,rg[2].text],'appname, username,password')

        for item in rg:
            item.text = ''
            

class SettingScreen(MDScreen):
    pass


class PassMana(MDApp):


    def build_config(self, config):
        config.setdefaults('theme',{
            'theme_style':'Light',
            'primary_palette':'Blue'
        })

    def build(self):
        self.theme_cls.theme_style = self.config.get('Theme', 'theme_style')
        self.theme_cls.primary_palette = self.config.get('Theme', 'primary_palette')

        self.theme_cls.theme_style_switch_animation = True
    
    def changeTheme(self, *args):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"
        
        self.config.set('Theme', 'theme_style', self.theme_cls.theme_style)
        self.config.write()


if __name__ == '__main__':

    PassMana().run()

