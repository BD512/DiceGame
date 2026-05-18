class Colour: # a class to store and perform operations of the hex
    def __init__(self, colour:str):
        self.colour_hex_code = colour

    def getLuminance(self): # gets how bright the colour is as an integer
        colour_number = self.colour_hex_code[1:]
        hex_red = int(colour_number[0:2], base=16)
        hex_green = int(colour_number[2:4], base=16)
        hex_blue = int(colour_number[4:6], base=16)
        return hex_red * 0.2126 + hex_green * 0.7152 + hex_blue * 0.0722

    def getTextColour(self): # returns whether the text colour with this colour as a background should be black or white based on luminance
        return "white" if self.getLuminance() < 140 else "black"