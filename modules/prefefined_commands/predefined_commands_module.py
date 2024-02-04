import subprocess
import webbrowser
from modules.speak_back.speak_module import Speak_Back

class Predefined_Commands:
    def __init__(self):
        self.error_message = "Predefined command was not found"
        self.error = "Executing error"
        self.speak = Speak_Back()
        self.default_web_url = "https://www.google.com"

    def construct_command(self,command_name, passed_terminal_command):
        command = passed_terminal_command
        try:
            self.speak.speak_back(command_name)
            subprocess.run(command, shell=True, check=True, text=True)
        except Exception:
            print("\n\n{}\n\n".format(self.error))
            return False
            
    def check_browser_command_list(self,passed_phrase):
        match passed_phrase:
            case "open browser":
                self.speak.speak_back("opening webbrowser")
                webbrowser.open(self.default_web_url)
                return True
            case "open new browser tab":
                self.speak.speak_back("opening new browser tab")
                webbrowser.open_new_tab(self.default_web_url)
                return True
            case _:
                print("\n\n{}\n\n".format(self.error_message))
                return False

    def check_command_list(self,passed_phrase):
        match passed_phrase:
            case "open terminal":
                self.construct_command("opening terminal","gnome-terminal")
                return True
            case "open browser":
                res = self.check_browser_command_list(passed_phrase)
                return res
            case "open new browser tab":
                res = self.check_browser_command_list(passed_phrase)
                return res
            case _:
                print("\n\n{}\n\n".format(self.error_message))
                return False
