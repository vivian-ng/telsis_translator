#!/usr/bin/env python3
'''
Helper function that installs the required fonts depending on
the type of system.

Currently available for Linux and Windows because I do not
own a Mac.

In Linux, running this script by itself will install TelsisTyped.otf
in the .fonts directory of the user's home directory.
'''
import os, sys, base64

#from fontNoto64 import noto64
from font_telsis64 import telsis64

from os.path import expanduser
home = expanduser("~")

if sys.platform.startswith('win'):
    '''
    This portion for Windows was taken from
    https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter
    '''

    from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
    FR_PRIVATE  = 0x10
    FR_NOT_ENUM = 0x20

    def loadfont(fontpath, private=True, enumerable=False):
        '''
        Makes fonts located in file `fontpath` available to the font system.

        `private`     if True, other processes cannot see this font, and this 
                    font will be unloaded when the process dies
        `enumerable`  if True, this font will appear when enumerating fonts

        See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx

        '''
        # This function was taken from
        # https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
        # This function is written for Python 2.x. For 3.x, you
        # have to convert the isinstance checks to bytes and str
        if isinstance(fontpath, str):
            pathbuf = create_string_buffer(fontpath)
            AddFontResourceEx = windll.gdi32.AddFontResourceExA
        elif isinstance(fontpath, unicode):
            pathbuf = create_unicode_buffer(fontpath)
            AddFontResourceEx = windll.gdi32.AddFontResourceExW
        else:
            raise TypeError('fontpath must be of type str or unicode')

        flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
        numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
        return bool(numFontsAdded)

def font2base64(fontpath):
    '''
    Loads a font at fontpath returns it as a base64-encoded string.
    '''
    with open(fontpath, "rb") as font_file:
        encoded_string = base64.b64encode(font_file.read())
    return encoded_string

def savefont(base64font, destpath):
    '''
    Saves a font, encoded in base64, to the destination given
    by destpath.
    Does nothing if the file given by destpath already exists.
    '''
    if not os.path.exists(destpath):
        with open(destpath, "wb") as fh:
            fh.write(base64.b64decode(base64font))
    if os.path.exists(destpath):
        return True  # font file now exists at the destpath
    else:
        return False

def copyfont(fontpath, destpath):
    '''
    Copies a font located at fontpath to the destination given
    by destpath.
    '''
    return savefont(font2base64(fontpath), destpath)

def install_fonts():
    if sys.platform.startswith('win'):
        #if savefont(noto64, './NotoSansCJK-Regular.ttc') and savefont(telsis64, './TelsisTyped.otf'):
        if savefont(telsis64, './TelsisTyped.otf'):
            pass  # required fonts now in current working directory
        else:
            print('Unable to install fonts: unable to save font files')
        #loadfont('./NotoSansCJK-Regular.ttc')
        loadfont('./TelsisTyped.otf')
    elif sys.platform.startswith('linux'):
        #if savefont(noto64, home + '/.fonts/NotoSansCJK-Regular.ttc') and savefont(telsis64, home + '/.fonts/TelsisTyped.otf'):
        if savefont(telsis64, home + '/.fonts/TelsisTyped.otf'):
            return True  # required fonts now in .fonts directory
        else:
            print('Unable to install fonts: unable to save font files')
    else:
        print('Unable to install fonts: unsupported OS')

if __name__ == "__main__":
    # execute only if run as a script
    install_fonts()