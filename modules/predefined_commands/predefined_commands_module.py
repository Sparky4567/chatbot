import subprocess
import webbrowser
from modules.speak_back.speak_module import Speak_Back

class Predefined_Commands:
    def __init__(self):
        self.error_message = "Predefined command was not found"
        self.error = "Executing error"
        self.speak = Speak_Back()
        self.default_web_url = "https://www.google.com"
        self.youtube_url = "https://www.youtube.com/"
        self.google_url = "https://www.google.com/"

    def construct_command(self,command_name, passed_terminal_command):
        command = passed_terminal_command
        try:
            self.speak.speak_back(command_name)
            subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except Exception:
            print("\n\n{}\n\n".format(self.error))
            return False
        
    def construct_output_command(self,command_name, passed_terminal_command):
        command = passed_terminal_command
        try:
            self.speak.speak_back(command_name)
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
            if result.returncode == 0:
                print("\n\nCommand executed successfully\n\n")
                print("Output:\n\n{}\n\n".format(result.stdout))
            return True
        except Exception:
            print("\n\n{}\n\n".format(self.error))
            return False
        
    def search_youtube(self,words,sentence,passed_url):
        # OPENS NEW TAB AND CONSTRUCTS YOUTUBE SEARCH URL
        if all(x in str(sentence).lower().split() for x in words):
            new_sentence = sentence
            for x in words:
                new_sentence=str(new_sentence).replace(x,"").strip()
            query_words = new_sentence.split()
            youtube_url="{}results?search_query=".format(passed_url)
            for word_index, word in enumerate(query_words):
                if(word_index==0):
                    youtube_url = "{}{}".format(youtube_url,word)
                else:
                    youtube_url = "{}+{}".format(youtube_url,word)
            webbrowser.open_new_tab(youtube_url)
            self.speak.speak_back("Searching youtube for {}".format(query_words))
            return True
        else:
            return False
        
    def search_google(self,words,sentence,passed_url):
        if all(x in str(sentence).lower().split() for x in words):
            new_sentence = sentence
            for x in words:
                new_sentence=str(new_sentence).replace(x,"").strip()
            query_words = new_sentence.split()
            google_url="{}search?q=".format(passed_url)
            for word_index, word in enumerate(query_words):
                if(word_index==0):
                    google_url = "{}{}".format(google_url,word)
                else:
                    google_url = "{}+{}".format(google_url,word)
            self.speak.speak_back("Searching google for {}".format(query_words))
            webbrowser.open_new_tab(google_url)
            return True
        else:
            return False

    def search_youtube_ini(self,passed_phrase):
        res = self.search_youtube(["search","youtube","for"],passed_phrase,self.youtube_url)
        return res
    
    def search_google_ini(self,passed_phrase):
        res = self.search_google(["search","google","for"],passed_phrase,self.google_url)
        return res
            
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
                res = self.construct_command("opening terminal","gnome-terminal")
                return res
            case "open thunderbird":
                res = self.construct_command("opening thunderbird email client",["thunderbird"])
                return res
            case "code":
                res = self.construct_command("opening vs code",["code","."])
                return res
            case "list directory":
                res = self.construct_output_command("list of a current directory",["ls","-la"])
                return res
            case "open browser":
                res = self.check_browser_command_list(passed_phrase)
                return res
            case "open new browser tab":
                res = self.check_browser_command_list(passed_phrase)
                return res
            case passed_phrase if "search youtube for" in passed_phrase:
                res = self.search_youtube_ini(passed_phrase)
                return res
            case passed_phrase if "search google for" in passed_phrase:
                res = self.search_google_ini(passed_phrase)
                return res
            case _:
                print("\n\n{}\n\n".format(self.error_message))
                return False
