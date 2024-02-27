import subprocess
import webbrowser
from modules.speak_back.speak_module import Speak_Back
import asyncio
from modules.local_llm.llm_module import Lama_Chat


from config import SPEAK_BACK
class Predefined_Commands:
    def __init__(self):
        self.error_message = "Predefined command was not found"
        self.error = "Executing error"
        self.speak = Speak_Back()
        self.default_web_url = "https://www.google.com"
        self.youtube_url = "https://www.youtube.com/"
        self.google_url = "https://www.google.com/"
        self.gpt_url = "https://chat.openai.com/"
        self.giphy_url = "https://giphy.com/"
        self.chat = Lama_Chat()

    def construct_command(self,command_name, passed_terminal_command):
        command = passed_terminal_command
        try:
            if(SPEAK_BACK) is True:
                self.speak.speak_back(command_name)
            subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except Exception:
            return False
        
    def construct_output_command(self,command_name, passed_terminal_command):
        command = passed_terminal_command
        try:
            if(SPEAK_BACK) is True:
                self.speak.speak_back(command_name)
            subprocess.run(command, stdout=subprocess.PIPE, text=True)
            return True
        except Exception:
            return False
        
    def search_youtube(self,words,sentence,passed_url):
        # OPENS NEW TAB AND CONSTRUCTS YOUTUBE SEARCH URL
        if all(x in str(sentence).lower().split() and x is not None for x in words ):
            new_sentence = str(sentence)
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
        if all(x in str(sentence).lower().split() and x is not None for x in words):
            new_sentence = str(sentence)
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
        
    def search_giphy(self,words,sentence,passed_url):
        if all(x in str(sentence).lower().split() and x is not None for x in words):
            new_sentence = sentence
            for x in words:
                new_sentence=str(new_sentence).replace(x,"").strip()
            query_words = new_sentence.split()
            giphy_url="{}/search/".format(passed_url)
            for word_index, word in enumerate(query_words):
                if(word_index==0):
                    giphy_url = "{}{}".format(giphy_url,word)
                else:
                    giphy_url = "{}-{}".format(giphy_url,word)
            if(SPEAK_BACK is True):
                self.speak.speak_back("Searching giphy for {}".format(query_words))
            webbrowser.open_new_tab(giphy_url)
            return True
        else:
            return False
        
    def ask_llm(self,words,sentence):
        if all(x in str(sentence).lower().split() and x is not None for x in words):
            new_sentence = str(sentence)
            for x in words:
                new_sentence=str(new_sentence).replace(x,"").strip()
            query_words = new_sentence.split()
            res = asyncio.run(self.chat.make_a_request())
            res = str(res).strip()
            if(SPEAK_BACK is True):
                self.speak.speak_back("Asking local LLM using your input: {}".format(query_words))
                self.speak.speak_back(res)
                print("\n\n{}\n\n".format(res))
            print("\n\n{}\n\n".format("Asking local LLM using your input: {}".format(query_words)))
            print("\n\n{}\n\n".format(res))
            return True
        else:
            return False

    def search_youtube_ini(self,passed_phrase):
        res = self.search_youtube(["search","youtube","for"],passed_phrase,self.youtube_url)
        return res
    
    def search_google_ini(self,passed_phrase):
        res = self.search_google(["search","google","for"],passed_phrase,self.google_url)
        return res
    
    def search_giphy_ini(self,passed_phrase):
        res = self.search_giphy(["search","giphy","for"],passed_phrase,self.giphy_url)
        return res
    
    def ask_llm__ini(self,passed_phrase):
        res = self.ask_llm(["ask","llm"],passed_phrase)
        return res
            
    def check_browser_command_list(self,passed_message,passed_phrase):
        self.speak.speak_back(passed_message)
        match passed_phrase:
            case "open browser":
                webbrowser.open(self.default_web_url)
                return True
            case "open new browser tab":
                webbrowser.open_new_tab(self.default_web_url)
                return True
            case "open gpt":
                webbrowser.open(self.gpt_url)
                return True
            case "open giphy":
                webbrowser.open(self.giphy_url)
                return True
            case _:
                return False

    def check_command_list(self,passed_phrase):
        match passed_phrase:
            case "open terminal":
                res = self.construct_command("opening terminal","gnome-terminal")
                return res
            case "open thunderbird":
                res = self.construct_command("opening thunderbird email client",["thunderbird"])
                return res
            case "open obsidian":
                res = self.construct_command("opening obsidian notes",["obsidian"])
                return res
            case "open cheese":
                res = self.construct_command("opening cheese application",["cheese"])
                return res
            case "open calculator":
                res = self.construct_command("opening calculator",["gnome-calculator"])
                return res
            case "open office application":
                res = self.construct_command("opening libre office",["libreoffice"])
                return res
            case "open vs code":
                res = self.construct_command("opening vs code",["code","."])
                return res
            case "go to store":
                res = self.construct_command("opening snap store",["snap-store"])
                return res
            case "list directory":
                res = self.construct_output_command("list of a current directory",["ls","-la"])
                return res
            case "open browser":
                res = self.check_browser_command_list("opening browser", passed_phrase)
                return res
            case "open gpt":
                res = self.check_browser_command_list("opening chat gpt", passed_phrase)
                return res
            case "open new browser tab":
                res = self.check_browser_command_list("opening new browser tab", passed_phrase)
                return res
            case "open giphy":
                res = self.check_browser_command_list("opening new browser tab", passed_phrase)
                return res
            case passed_phrase if "search youtube for" in str(passed_phrase) and hasattr(passed_phrase, '__iter__') is True:
                res = self.search_youtube_ini(str(passed_phrase))
                return res
            case passed_phrase if "search google for" in str(passed_phrase) and hasattr(passed_phrase, '__iter__') is True:
                res = self.search_google_ini(str(passed_phrase))
                return res
            case passed_phrase if "search giphy for" in str(passed_phrase) and hasattr(passed_phrase, '__iter__') is True:
                res = self.search_giphy_ini(str(passed_phrase))
                return res
            case passed_phrase if "ask llm" in passed_phrase and hasattr(passed_phrase, '__iter__') is True:
                res = self.ask_llm__ini(str(passed_phrase))
                return res
            case _:
                return False
