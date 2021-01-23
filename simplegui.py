#!/usr/bin/env python3
"""
Telsis language translator

GUI using PySimpleGUI

Copyright (c) 2021 Vivian Ng
"""
import os
import sys
import io

try:
    import PySimpleGUI as sg
except ImportError as e:
    print("PySimeplGUI is needed to run the GUI.")
    sys.exit(1)

from languages import *


USER_FONT_SIZE = 24
UI_FONT_SIZE = 20
DEFAULT_FONT = "Courier"
TELSIS_FONT = "TelsisTyped"

def find_key(x, d):
    # Helper function: find key in dictionary d with value of x
    for key, value in d.items():
         if x == value:
             return key
    return "key doesn't exist"

def on_press_translate_button(window, values, translator):
    if values['source_text'] == "":
        window['error_text'].update("Nothing to translate")
        window['target_text'].update("")
        window['telsis_text'].update("")
        return
    srclang = values['source_lang']
    display_telsis_flag = False
    if srclang != '':
        srclang = find_key(values['source_lang'], avail_languages)
    tgtlang = values['target_lang']
    if tgtlang != '':
        tgtlang = find_key(values['target_lang'], avail_languages)
    srctext = values['source_text']
    if srclang == '' and tgtlang == '':
        window['error_text'].update("Source or target language must be defined")
        window['target_text'].update("")
        window['telsis_text'].update("")
    elif srclang == tgtlang:
        window['error_text'].update("Source and target language must be different")
        window['target_text'].update("")
        window['telsis_text'].update("")
    else:
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
        window['target_text'].update(translator.results['tgt_text'])  # Print out results of translation
        window['error_text'].update("")  # clear error message
        if display_telsis_flag:
            window['telsis_text'].update(translator.results['tgt_text'])  # Print out results of translation in Telsis font
        else:
            window['telsis_text'].update("")

def on_press_display_button(window, values):
    if values['source_text'] == '':
        window['telsis_text'].update("")
        window['error_text'].update("Nothing to display")
    else:
        window['telsis_text'].update(values['source_text'])
        window['error_text'].update("")

def run_app(translator):
    sg.theme("Default")

    avail_languages_list = []
    for lang_code in avail_languages.keys():
        avail_languages_list.append(avail_languages[lang_code])

    source_label = sg.Text("Source language: ")
    target_label = sg.Text("Target language: ")
    source_list = sg.Combo(avail_languages_list, enable_events=True, key='source_lang')
    target_list = sg.Combo(avail_languages_list, enable_events=True, key='target_lang')

    source_text_label = sg.Text("Source text:")
    source_text_input = sg.Multiline("", size=(45,5), key="source_text")

    translate_button = sg.Button("Translate", key="_TRANSLATE_BUTTON_")
    display_button = sg.Button("Display", key="_DISPLAY_BUTTON_")

    target_text_label = sg.Text("Target text:")
    target_text_input = sg.Multiline("", size=(45,5), key="target_text")

    telsis_text_input = sg.Multiline("", size=(45,5), font=(TELSIS_FONT, UI_FONT_SIZE),
                            key="telsis_text")
    error_text_label = sg.Multiline("", size=(45,1), key="error_text")

    layout = [[source_label, source_list],
            [target_label, target_list],
            [source_text_label],
            [source_text_input],
            [translate_button, display_button],
            [target_text_label],
            [target_text_input],
            [telsis_text_input],
            [error_text_label]]
    window = sg.Window('Telsis Translator', layout, font=(DEFAULT_FONT, UI_FONT_SIZE))

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == '_TRANSLATE_BUTTON_':
            on_press_translate_button(window, values, translator)
        if event == '_DISPLAY_BUTTON_':
            on_press_display_button(window, values)

    window.close()


def run_gui(trans):
    if trans == "":
        from telsistrans import telsis_translator
        translator = telsis_translator()
    else:
        translator = trans
    run_app(translator)

if __name__ == '__main__':
    run_gui("")