#!/usr/bin/env python
#
# Code to insert text in poster jpg files.
#
# Copyright: Surhud More (IUCAA) 2020
#
# Bug reports/comments: Open github issues, or send pull requests

import textwrap
from PIL import Image, ImageDraw, ImageFont
from os import path
import numpy as np
import sys
import pandas

class fill_poster:
    def __init__(self, image):
        self.imagename = image
        self.image = Image.open(image+".png.jpg")
        self.fullwidth = self.image.width

    def output_text(self, message, y, font=None, width=None, color='rgb(0, 0, 0)', margin=40, offsety=30, printoffset=False):

        # This class will write out the line in the file in multiple lines and center it.
        for line in textwrap.wrap(message, width):
            w, h = self.draw.textsize(line, font=font)
            self.draw.text(((self.image.width-w)/2, y + offsety), line, font=font, fill=color)
            offsety += font.getsize(line)[1]

    def convert(self, ii, strings, pl, language, fonts, widthreduce):
        # Initiate image
        self.draw = ImageDraw.Draw(self.image)

        # Add a common The Hoaxbusters line
        self.output_text("The Hoaxbusters", 200, font=fonts["4"],  width=30)

        # Add all the strings at the right places with the right fonts
        self.output_text(strings["1"], pl["1"], font=fonts["1"], width=30-widthreduce, color='rgb(94, 94, 94)')
        self.output_text(strings["2"], pl["2"], font=fonts["2"], width=30-widthreduce)
        self.output_text(strings["3"], pl["3"], font=fonts["1"], width=40-widthreduce, color='rgb(94, 94, 94)')
        self.output_text(strings["4"], pl["4"], font=fonts["2"], width=45-widthreduce, color='rgb(189, 23, 23)')
        if pl["5"] != 0:
            self.output_text(strings["5"], pl["5"], font=fonts["5"], width=45-widthreduce, color='rgb(0, 0, 0)')
        self.output_text(strings["6"], pl["6"], font=fonts["1"], width=45-widthreduce, color='rgb(94, 94, 94)')
        self.output_text(strings["7"], pl["7"], font=fonts["3"], width=48-widthreduce)

        # Save the file
        self.image.save("Final/"+self.imagename+"_%s_hires.jpg" % language)

if __name__ == "__main__":

    language = sys.argv[1]

    # Read the placements file
    placements = np.loadtxt("%s/placements_%s.txt" % (language, language))

    # Read the fonts information
    from yaml import load, Loader
    fin = open("Master_config_hires.yaml", "r")
    config = load(fin, Loader=Loader)

    # Setup fonts
    fonts = {}
    fonts["1"] = ImageFont.truetype(config[language]["font1"], size=5*config[language]["size1"])
    fonts["2"] = ImageFont.truetype(config[language]["font2"], size=5*config[language]["size2"])
    fonts["3"] = ImageFont.truetype(config[language]["font3"], size=5*config[language]["size3"])
    fonts["5"] = ImageFont.truetype(config[language]["font5"], size=5*config[language]["size5"])
    fonts["4"] = ImageFont.truetype('Noto/English/Montserrat-Bold.ttf', size=200)

    # Some languages required a width reduction in the text compared to default
    widthreduce = 0
    if "widthreduce" in config[language]:
        widthreduce = config[language]["widthreduce"]

    # Read the translations
    df = pandas.read_csv("Hoaxbuster.csv")
    df.fillna("", inplace = True) 

    # Setup translation strings and placements in strings dictionary and pl dictionary
    jj = 0
    for ii in range(1, 19):
        strings = {}
        pl = {}
        pl["1"] = placements[ii-1][1]*5
        pl["2"] = placements[ii-1][2]*5
        pl["3"] = placements[ii-1][3]*5
        pl["4"] = placements[ii-1][4]*5
        pl["5"] = placements[ii-1][5]*5
        pl["6"] = placements[ii-1][6]*5
        pl["7"] = placements[ii-1][7]*5 
        strings["1"] = df[language].values[jj]
        jj = jj + 1
        strings["2"] = df[language].values[jj]
        jj = jj + 1
        strings["3"] = df[language].values[jj]
        jj = jj + 1
        strings["4"] = df[language].values[jj]
        jj = jj + 1
        strings["5"] = df[language].values[jj]
        jj = jj + 1
        strings["6"] = df[language].values[jj]
        jj = jj + 1
        strings["7"] = df[language].values[jj]
        jj = jj + 1
        
        # Some images did not exist in the beginning, so ignore them
        if not path.exists("Sample_images/%05d.jpg" % ii) :
            print("could not find", ii)
            continue

        # Initiate a class
        a = fill_poster("Sample_images/%05d" % ii)

        # Fill in the poster with strings, and save file
        a.convert(ii, strings, pl, language, fonts, widthreduce)
