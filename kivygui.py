#!/usr/bin/env python3
import os
os.environ["KIVY_NO_ARGS"] = "1"
import sys

try:
    import kivy
except ImportError as e:
    print("Kivy is needed to run the GUI.")
    sys.exit(1)
kivy.require('2.0.0')


try:
    import japanize_kivy
except ImportError as e:
    print("japanize-kivy package is needed to run the GUI.")
    sys.exit(1)


from languages import *

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.resources import resource_add_path, resource_find


USER_FONT_SIZE = 24
UI_FONT_SIZE = 20
def find_key(x, d):
    # Helper function: find key in dictionary d with value of x
    for key, value in d.items():
         if x == value:
             return key
    return "key doesn't exist"


class TelsisApp(App):

    def build(self):
        #self.root = get_main_window()
        #self.root.clearcolor = (1, 1, 1, 1)
        self.icon = 'TelsisTranslatorIcon.ico'
        avail_languages_list = []
        for lang_code in avail_languages.keys():
            avail_languages_list.append(avail_languages[lang_code])

        source_label = Label(text='Source language:', 
                        font_size=UI_FONT_SIZE,
                        halign="right", valign="middle")
        target_label = Label(text='Target language:',
                        font_size=UI_FONT_SIZE,
                        halign="right", valign="middle")
        self.source_list = Spinner(text='',
                        font_size=UI_FONT_SIZE,
                        values=avail_languages_list)
        self.target_list = Spinner(text='',
                        font_size=UI_FONT_SIZE,
                        values=avail_languages_list)

        source_row = GridLayout(cols=2, size_hint=(1, 0.5))
        target_row = GridLayout(cols=2, size_hint=(1, 0.5))
        source_row.add_widget(source_label)
        source_row.add_widget(self.source_list)
        target_row.add_widget(target_label)
        target_row.add_widget(self.target_list)

        source_text_label = Label(text='Source text:', 
                        font_size=UI_FONT_SIZE,
                        font_name='fonts/NotoSansCJK-Regular.ttc',
                        size_hint=(1, 0.5),
                        halign="left", valign="middle")
        self.source_text = TextInput(text='', font_size=USER_FONT_SIZE)

        target_text_label = Label(text='Target text:',
                        font_size=UI_FONT_SIZE,
                        size_hint=(1, 0.5),
                        halign="left", valign="middle")
        self.translated_text_label = Label(text=' ', 
                        font_size=USER_FONT_SIZE,
                        font_name='fonts/NotoSansCJK-Regular.ttc',
                        size_hint=(1, None), halign="left", valign="top")
        target_text = ScrollView(size_hint=(1, None))
        target_text.add_widget(self.translated_text_label)

        translate_button = Button(text='Translate',
                        font_size=UI_FONT_SIZE*1.5,
                        size_hint=(.5, .5),
                        pos_hint={'center_x': .5, 'center_y': .5})
        translate_button.bind(on_press=self.on_press_translate_button)
        display_button = Button(text='Display',
                        font_size=UI_FONT_SIZE*1.5,
                        size_hint=(.5, .5),
                        pos_hint={'center_x': .5, 'center_y': .5})
        display_button.bind(on_press=self.on_press_display_button)

        button_row = GridLayout(cols=2, size_hint=(1, 0.5))
        button_row.add_widget(display_button)
        button_row.add_widget(translate_button)

        target_text_canvas = ScrollView(size_hint=(1, None))
        self.telsis_text_label = Label(text='', size_hint=(1, None),
                        font_size=USER_FONT_SIZE,
                        font_name='TelsisTyped1.otf',
                        halign="left", valign="top")
        target_text_canvas.add_widget(self.telsis_text_label)
        self.error_label = Label(text='')


        layout = BoxLayout(padding=10, orientation='vertical')
        layout.add_widget(source_row)  # Choose source language
        layout.add_widget(target_row)  # Choose target language
        layout.add_widget(source_text_label)  # Label for source text
        layout.add_widget(self.source_text)  # Input box for source text
        layout.add_widget(button_row)  # Press button to translate or display
        layout.add_widget(target_text_label)  # Label for target text
        layout.add_widget(target_text)  # Scroll window for translated text
        layout.add_widget(target_text_canvas)  # Translated text in Telsis font
        layout.add_widget(self.error_label)  # Error messages

        #layout.add_widget(Label(text='Hello from Kivy',
        #            size_hint=(.5, .5),
        #            pos_hint={'center_x': .5, 'center_y': .5}))
        return layout

    def set_translator(self, translator):
        self.translator = translator

    def on_press_translate_button(self, instance):
        if self.source_text.text == "":
            self.error_label.text = "Nothing to translate"
            self.telsis_text_label.text = ""
            self.translated_text_label.text = ""
            return
        srclang = self.source_list.text
        display_telsis_flag = False
        if srclang != '':
            srclang = find_key(self.source_list.text, avail_languages)
        tgtlang = self.target_list.text
        if tgtlang != '':
            tgtlang = find_key(self.target_list.text, avail_languages)
        srctext = self.source_text.text
        if srclang == '' and tgtlang == '':
            self.error_label.text = "Source or target language must be defined"
            self.telsis_text_label.text = ""
            self.translated_text_label.text = ""
        elif srclang == tgtlang:
            self.error_label.text = "Source and target language must be different"
            self.telsis_text_label.text = ""
            self.translated_text_label.text = ""
        else:
            translator = self.translator
            if srclang == 'telsis':  # From Telsis language to another language
                if tgtlang == '':
                    tgtlang = 'en'  # Defaults to English when translating from Telsis
                translator.telsis2lang(srctext, tgtlang)
                display_telsis_flag = False
            elif tgtlang == 'telsis':  # From another language to Telsis language
                translator.lang2telsis(srctext, srclang)
                display_telsis_flag = True
            elif srclang != 'telsis' and srclang != '':  # From another language to Telsis language
                translator.lang2telsis(srctext, srclang)
                display_telsis_flag = True
            elif tgtlang != 'telsis' and tgtlang != '':  # From Telsis language to another language
                if tgtlang == '':
                    tgtlang = 'en'  # Defaults to English when translating from Telsis
                translator.telsis2lang(srctext, tgtlang)
                display_telsis_flag = False
            self.translated_text_label.text = translator.results['tgt_text']  # Print out results of translation
            self.error_label.text = ""  # clear error message
            if display_telsis_flag:
                self.telsis_text_label.text = translator.results['tgt_text']  # Print out results of translation in Telsis font
            else:
                self.telsis_text_label.text = ""

    def on_press_display_button(self, instance):
        if self.source_text.text == "":
            self.error_label.text = "Nothing to display"
            self.telsis_text_label.text = ""
            self.translated_text_label.text = ""
            return
        else:
            self.error_label.text = ""
            self.telsis_text_label.text = self.source_text.text
            self.translated_text_label.text = ""
            return


def run_gui(translator):
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    if translator == "":
        from telsistrans import telsis_translator
        translator = telsis_translator()
    app = TelsisApp()
    app.set_translator(translator)
    Window.size = (480, 720)
    app.run()

if __name__ == '__main__':
    run_gui("")