import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class MyGrid(Widget):
    SMID = ObjectProperty(None)
    passw = ObjectProperty(None)
    FDL = ObjectProperty(None)
    TDL = ObjectProperty(None)
    TM = ObjectProperty(None)
    NM = ObjectProperty(None)

    def btn(self):
        lst = [self.SMID.text, self.passw.text, self.FDL.text, self.TDL.text, self.TM.text, self.NM.text]
        return lst

class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == '__main__':
    MyApp().run()