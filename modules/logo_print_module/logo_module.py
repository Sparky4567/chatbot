from pyfiglet import Figlet

class Logo_Module:
    def __init__(self):
        self.name = "Amy Bot"

    def print_logo(self):
        f = Figlet(font="slant")
        print(f.renderText("{}".format(self.name)))
