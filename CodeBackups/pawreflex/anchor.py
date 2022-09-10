from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import (StringProperty, NumericProperty, ReferenceListProperty, ObjectProperty, OptionProperty, VariableListProperty)
from kivy.uix.popup import Popup


from fakecode import main

class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text

class CombWidget(AnchorLayout):
    padding = VariableListProperty([0, 0, 0, 0])
    anchor_x = OptionProperty('left')
    anchor_y = OptionProperty('top')
    b1 = Button(
        text="Start",
        font_size = 12,
        pos_hint={'center_x':.5, 'center_y':.5},
        size_hint=(0.2,0.1)
    )
    b1.bind(on_touch_down=self.fn)
    self.add_widget(b1)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            popup = TextInputPopup(self)
            popup.open()
            self.popup_input = popup.obj_text

    def fn(self, value):
        main(run=self.popup_input)

        # exec(open("fakecode.py").read)
        # insert self.popup_input into run

class PawApp(App):
    def build(self):
        return CombWidget(size_hint = (1,1), width = 800, cols =1)

if __name__ == "__main__":
    PawApp().run()