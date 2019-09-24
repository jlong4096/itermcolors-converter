#!/usr/bin/env python
#
# Convert .itermcolors files to hex colors for html

import re
import sys
import xml.etree.ElementTree as ET

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def iterm_key_to_kitty_key(key):
    if key == "Background Color":
        return "background"
    elif key == "Foreground Color":
        return "foreground"
    elif key == "Selection Color":
        return "selection_background"
    elif key == "Selection Text Color":
        return "selection_foreground"
    elif key == "Cursor Color":
        return "cursor"
    elif key == "Cursor Text Color":
        return "cursor_text_color"
    else:
        m = re.match(r'Ansi (\d\d?) Color', key)
        if m is not None:
            return "color" + m.group(1)

# MAIN
def main():

    if len(sys.argv) < 2:
        print "usage: ./convert_itermcolors.py file.itermcolors"
        exit()

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    keys = root.findall("./dict/key")
    dicts = root.findall("./dict/dict")

    for i in range(len(keys)):
        b = 0
        g = 0
        r = 0
        for j in range(len(dicts[i])):
            if dicts[i][j].text == "Blue Component":
                b = int(float(dicts[i][j+1].text) * 255.0)
            elif dicts[i][j].text == "Green Component":
                g = int(float(dicts[i][j+1].text) * 255.0)
            elif dicts[i][j].text == "Red Component":
                r = int(float(dicts[i][j+1].text) * 255.0)
        k = iterm_key_to_kitty_key(keys[i].text)
        if k is not None:
            print '{:22}{}'.format(k, rgb_to_hex((r,g,b)))

if __name__ == '__main__':
    main()
