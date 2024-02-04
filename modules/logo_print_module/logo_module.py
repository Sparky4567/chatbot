from pyfiglet import Figlet

class Logo_Module:
    def __init__(self):
        self.name = "White Rabbit"

    def print_logo(self):
        f = Figlet(font="slant")
        print(f.renderText("{}".format(self.name)))
