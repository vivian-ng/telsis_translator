"""
Telsis language translator

Example on how to use telsistrans module

Copyright (c) 2021 Vivian Ng
"""

from telsistrans import telsis_translator
translator = telsis_translator()
srctext = "I love you"
srclang = 'en'
translator.lang2telsis(srctext, srclang)
print(translator.results['tgt_text'])  # Print out results of translation
srctext = "Nunki posuk"
tgtlang = 'ja'
translator.telsis2lang(srctext, tgtlang)
print(translator.results['tgt_text'])  # Print out results of translation