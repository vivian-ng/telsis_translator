#!/usr/bin/env python3
import unidecode
from google_trans_new import google_translator
from telsis_alphabet import alphabet
import requests
import argparse, sys

__version__ = "0.2"

from PIL import Image, ImageDraw, ImageFont

def telsis2image(telsis_text, font_file):
    # Displays in Telsis characters.
    # Requires font file "Violet_evergardenV14-Regular.ttf"
    # from https://www.reddit.com/r/anime/comments/7t789w/violet_evergarden_how_to_be_an_optimal_dollfont/
    # with the link at https://goo.gl/PUiwDe
    # Alternative font from https://www.reddit.com/r/VioletEvergarden/comments/fzkvc3/i_made_the_font_update/
    # with the link at https://drive.google.com/file/d/1a2FY8_Yyyk3ULGhpq7sPQ2N5KurLKyIk/view?usp=sharing
    # create an image
    out = Image.new("RGB", (720, 100), (255, 255, 255))
    # get a font
    fnt = ImageFont.truetype(font_file, 40)
    #fnt = ImageFont.truetype("Violet_evergardenV14-Regular.ttf", 40)
    #fnt = ImageFont.truetype("Automemoryfont.otf", 40)
    # get a drawing context
    d = ImageDraw.Draw(out)
    d.rectangle([0,0,720,100], fill=(255,255,255))
    d.text((10,10), telsis_text, fill=(0,0,0), font=fnt, stroke_width=1)
    out.show()

#translator = google_translator()
#tamil_script_url = 'https://inputtools.google.com/request?text={text}&itc=ta-t-i0-und'

class telsis_translator:
    def __init__(self):
        self.translator = google_translator()
        self.tamil_script_url = 'https://inputtools.google.com/request?text={text}&itc=ta-t-i0-und'
        self.results = {}
        self.results['src_text'] = ""
        self.results['tamil_text'] = ""
        self.results['tamil_script'] = ""
        self.results['tamil_sound'] = ""
        self.results['tgt_text'] = ""
        self.names = []
        self.names_converted = {}
        self.current_name_number = 0

    def tamil2telsis(self, tamil_string):
        # convert tamil string of unaccented characters to Telsis
        converted_text = ""
        literal_flag = False
        for char in tamil_string:
            if char == '\\':
                literal_flag = not literal_flag
                tchar = ''
            elif char not in alphabet:
                #telsis += char
                tchar = char
            else:
                if literal_flag:
                    tchar = char
                else:
                    tchar = alphabet[char]
            if tchar:
                converted_text += tchar
            else:
                #converted_text += "?"
                converted_text += ""
        return converted_text

    def replace_names(self, textstring):
        for name in self.names_converted.keys():
            textstring = textstring.replace(name, self.names_converted[name])
        return textstring

    def telsis2tamil(self, telsis_string):
        # convert Telssi to tamil string of unaccented characters
        converted_text = self.tamil2telsis(telsis_string)
        return converted_text

    def preprocess_source_text(self, source_text):
        literal_flag = False
        processed_text = ""
        self.names = []
        self.names_converted = {}
        name = ""
        for char in source_text:
            if not literal_flag:
                if char != '\\':  # just copy, not part of name
                    processed_text += char
                else:  # start of new name
                    literal_flag = True
                    self.current_name_number += 1  # increment the number to append behind XXX
                    name = ""
            else:
                if char != '\\':  # copy and also part of name
                    name += char
                    processed_text += char
                else:  # end of name
                    literal_flag = False
                    name_code = "XXX" + str(self.current_name_number)
                    self.names_converted[name_code] = name  # add name and code to dictionary
                    name = ""
        # Replace names with their corresponding name codes
        for name_code in self.names_converted.keys():
            processed_text = processed_text.replace(self.names_converted[name_code], name_code)
        return processed_text

    def tamil2lang(self, source_text, tgt_lang):
        tamil_res = requests.get(self.tamil_script_url.format(text=source_text), headers={
            'Content-Type': 'application/json'
        }).json()
        
        if (tamil_res[0] == 'SUCCESS'):
            tamil_script = tamil_res[1][0][1][0]
        self.results['tamil_text'] = source_text
        self.results['tamil_script'] = tamil_script
        self.results['tamil_sound'] = ""
        self.results['tgt_text'] = self.translator.translate(f'{tamil_script}', lang_src='ta', lang_tgt=tgt_lang)

    def lang2tamil(self, source_text, src_lang):
        translated_results = self.translator.translate(source_text, lang_src=src_lang, lang_tgt='ta', pronounce=True)
        self.results['src_text']= source_text
        self.results['tamil_script'] = translated_results[0]
        self.results['tamil_sound'] = translated_results[2]
        # results in unaccented characters
        self.results['tamil_text'] = unidecode.unidecode(translated_results[2])

    def lang2telsis(self, source_text, src_lang):
        source_text = self.preprocess_source_text(source_text)
        self.lang2tamil(source_text, src_lang)
        tgt_text = self.tamil2telsis(self.results['tamil_text'])
        self.results['tgt_text'] = self.replace_names(tgt_text)

    def telsis2lang(self, source_text, tgt_lang):
        self.tamil2lang(self.telsis2tamil(source_text), tgt_lang)
        self.results['src_text'] = source_text

def interactive_console(display_flag, font_file):
    translator = telsis_translator()
    while True:
        source_language = input("Source language: ")
        if source_language.lower() == 'quit':
            return
        source_text = input("Input source text: ")
        target_language = input("Target language: ")
        if target_language == '' and source_language == '':
            print("Source or target language must be defined")
            continue
        if target_language == '' and source_language.lower() == 'telsis':
            target_language = 'en'  # default target language is English
        if source_language.lower() == 'telsis':
            translator.telsis2lang(source_text, target_language)
        else:
            translator.lang2telsis(source_text, source_language)
        print(f"In Tamil script: {translator.results['tamil_script']}")
        print(f"Pronunciation: {translator.results['tamil_sound']}")
        print(f"In unaccented characters: {translator.results['tamil_text']}")
        print(f"In target language: {translator.results['tgt_text']}")
        # uncomment following line to display in Telsis characters
        if source_language.lower() != 'telsis' and display_flag:
            telsis2image(translator.results['tgt_text'], font_file)
    
def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-g", "--gui", help="graphical mode",
                    action="store_true")
    group.add_argument("-i", "--interactive", help="interactive console mode",
                    action="store_true")
    group.add_argument("-t", "--text", type=str, 
                    help="source text")
    parser.add_argument("-sl", "--srclang", type=str, 
                    help="source language")
    parser.add_argument("-tl", "--tgtlang", type=str, 
                    help="target language")
    parser.add_argument("-d", "--display", help="display results in Telsis font",
                    action="store_true")
    parser.add_argument("-f", "--font", type=str, 
                    help="font file")
    
    # Show help and exit if no arguments passed
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Prepare arguments for processing
    args = parser.parse_args()
    srclang = args.srclang
    if srclang:
        srclang = srclang.lower()
    else:
        srclang = ''
    tgtlang = args.tgtlang
    if tgtlang:
        tgtlang = tgtlang.lower()
    else:
        tgtlang = ''
    if args.display:  # Display results in Telsis font
        if args.font:
            pass
        else:  # Font file must be specified to display results
            print("Please specify font file to display results in Telsis font.")
            sys.exit(1)

    # Handle arguments
    if args.gui:
        from gui import run_gui
        translator = telsis_translator()
        run_gui(translator)
    elif args.interactive:  # Interactive mode
        if args.display:  # Display results in Telsis font
            interactive_console(True, args.font)
        else:  # Do not display results in Telsis font
            interactive_console(False, "")
    elif srclang == '' and tgtlang == '':
        print("Source or target language must be defined")
    elif srclang == tgtlang:
        print("Source and target language must be different")
    else:
        translator = telsis_translator()
        if srclang == 'telsis':  # From Telsis language to another language
            if tgtlang == '':
                tgtlang = 'en'  # Defaults to English when translating from Telsis
            translator.telsis2lang(args.text, tgtlang)
        elif tgtlang == 'telsis':  # From another language to Telsis language
            translator.lang2telsis(args.text, srclang)
            if args.display:  # Display results in Telsis font
                telsis2image(translator.results['tgt_text'], args.font)
        elif srclang != 'telsis' and srclang != '':  # From another language to Telsis language
            translator.lang2telsis(args.text, srclang)
            if args.display:  # Display results in Telsis font
                telsis2image(translator.results['tgt_text'], args.font)
        elif tgtlang != 'telsis' and tgtlang != '':  # From Telsis language to another language
            if tgtlang == '':
                tgtlang = 'en'  # Defaults to English when translating from Telsis
            translator.telsis2lang(args.text, tgtlang)
        print(translator.results['tgt_text'])  # Print out results of translation

if __name__ == "__main__":
    # execute only if run as a script
    main()