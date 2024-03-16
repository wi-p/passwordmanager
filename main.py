from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from sqlite3 import connect
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.core.window import Window

# -- Customized widgets --
class BoxPassword(BoxLayout):
    def __init__(self, name, pw, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)

        self.ids.name.text = name
        self.ids.pw.text = pw


class Pop(Popup):
    def __init__(self, title, **kwargs):
        super(Popup, self).__init__(**kwargs)

        self.title = title
        self.size_hint = (None, None)
        self.width = dp(200)
        self.height = dp(150)
        self.content = Button(text = 'Fechar')

        self.content.bind(on_press = self.dismiss)
        self.open()

class Manager(ScreenManager):
    def changeScreen(self, pwid):
        values = DataBase().getRegister(pwid)

        self.get_screen('update').ids.pwn_update.text = values[0][1]
        self.get_screen('update').ids.pwp_update.text = values[0][2]
        self.get_screen('update').ids.pwname.text = str(values[0][0])

        self.current = 'update'


class SnIndex(Screen):
    def on_pre_enter(self, *args):
        if 'boxpw' in self.ids.keys():
            for pw in DataBase().readData()[:]:
               self.ids.boxpw.add_widget(BoxPassword(pw[1],pw[2]))

    def on_pre_leave(self, *args):
        if 'boxpw' in self.ids.keys():
            for value in DataBase().readData():
                self.removeWidget()

    def removeWidget(self):
        try:
            self.ids.boxpw.remove_widget(self.ids.boxpw.children[0])
        except IndexError:
            pass


class AddScreen(Screen):
    def on_pre_enter(self):
        Window.bind(on_keyboard = self.returnIndex)

    def on_pre_leave(self):
        Window.unbind(on_keyboard = self.returnIndex)

    def returnIndex(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'index'

            return True

    def savePassword(self):
        DataBase().saveData(self.ids.ti_name.text, self.ids.ti_password.text)

        self.ids.ti_name.text, self.ids.ti_password.text = '',''


class SnUpdate(Screen):
    def on_pre_enter(self):
        Window.bind(on_keyboard = self.returnIndex)

    def on_pre_leave(self):
        Window.unbind(on_keyboard = self.returnIndex)

    def returnIndex(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'index'

            return True

    def updatePassword(self):
        DataBase().updateRegister((
            self.ids.pwn_update.text,
            self.ids.pwp_update.text,
            self.ids.pwname.text
        ))

        Pop('Dados atualizados com sucesso!')

    def deleteRegister(self):
        DataBase().deleteRegister(self.ids.pwname.text)

        self.ids.pwn_update.text = ''
        self.ids.pwp_update.text = ''

        Pop('Regisro apagado com sucesso!')


class PassWordManagerApp(App):
    def build(self):
        self.icon = 'appimages/appicon.png'
        return Manager()


class DataBase(object):
    con = connect('appdb.db')
    cursor = con.cursor()

    def createDataBase(self):
        self.cursor.execute("""
            CREATE TABLE PassWord(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(30) NOT NULL,
                password VARCHAR(20)
            );
        """)
        self.con.close()

    def saveData(self, name, password):
        self.cursor.execute("""
            INSERT INTO Password (name, password) VALUES (?,?);
        """, [name.capitalize(), password])
        self.con.commit()

    def readData(self):
        self.cursor.execute("""
            SELECT * FROM Password;
        """)

        return self.cursor.fetchall()

    def getRegister(self, name):
        self.cursor.execute("""
            SELECT * FROM Password
            WHERE name = (?);
        """, [name])

        return self.cursor.fetchall()

    def updateRegister(self, new_vs):
        self.cursor.execute("""
            UPDATE Password SET name = ?, password = ?
            WHERE id = ?;
        """, new_vs)

        self.con.commit()

    def deleteRegister(self, id):
        self.cursor.execute("""
            DELETE FROM Password
            WHERE id = ?;
        """, (id,))

        self.con.commit()


if __name__ == '__main__':
    PassWordManagerApp().run()



