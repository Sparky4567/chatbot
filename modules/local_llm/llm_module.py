import requests
import json
from config import DEFAULT_LLM_URL
from config import ENABLE_OFFLINE_RECOGNITION
from config import CONTINUOUS_LEARNING
from config import USE_VOICE_INPUT

from modules.speech_recognizers.speech_recognizers import Speech_recognizers
from modules.is_online.is_online import Is_Online


class Lama_Chat:
    def __init__(self):
        self.default_url = DEFAULT_LLM_URL
        self.model = ["phi","orca-mini","tinyllama","phi"]
        self.chosen_model = None
        self.speech_recognizers = Speech_recognizers()
        self.is_online = Is_Online()

    def recognizer_engine(self):
        if(ENABLE_OFFLINE_RECOGNITION is False):
            
            text = self.speech_recognizers.recognize_speech()
            if(text is False):
                print("/n/n{}/n/n".format("Recognition failure, trying again"))
                self.recognizer_engine()
        else:
            text = self.speech_recognizers.recognize_speech_pocketsphinx()
            if(text is False):
                print("/n/n{}/n/n".format("Recognition failure, trying again"))
                self.recognizer_engine()
        if text:
            # Use the 'text' variable for further processing
            print(str("\n\nRecognized text:{}\n\n").format(text))
            if(CONTINUOUS_LEARNING is False):
                user_input=input("\n\nWant to approve question ? (y)\n\n")
                if(str(user_input).lower()=="y"):
                    recognized_phrase = text
                    return recognized_phrase
                else:
                    self.recognizer_engine()
            else:
                recognized_phrase = text
                return recognized_phrase

        else:
            print("\n\nI did not manage to understand your voice input. Reinitiating.\n\n")
            self.recognizer_engine()
   
    def recognizer(self):
        if(CONTINUOUS_LEARNING is False):
            user_input = input("\n\nPress 'r' to record\n\n")
            if user_input.lower() == 'r':
                res = self.recognizer_engine()
                return res
            elif(user_input.lower()=="exit" or user_input.lower()=="end"):
                quit()        
            else:
                self.recognizer()
        else:
            res = self.recognizer_engine()
            return res

    def chosen_model_return(self,model_name):
        self.chosen_model = model_name
        return self.chosen_model

    def llm_chooser(self):
        for x,model in enumerate(self.model,start=1):
            print(f"{x}. {model}")
        model_choice = input("\n\nChoose a model\n\n")
        try:
            try:
                model_choice = int(str(model_choice).lower())
            except:
                self.chosen_model_return(None)
            model_from_list = self.model[model_choice-1]
            self.chosen_model_return(model_from_list)
        except:
            self.chosen_model_return(None)
            self.llm_chooser()

        

    def get_input(self):
        if(self.chosen_model is None):
            self.llm_chooser()
        else:
            self.chosen_model_return(None)
            self.llm_chooser()
        online_status = self.is_online.is_online()
        if(USE_VOICE_INPUT is True and online_status is True and ENABLE_OFFLINE_RECOGNITION is False):
            print("\n\nUsing Google recognizer\n\n")
            user_input = self.recognizer()
        elif(USE_VOICE_INPUT is True and online_status is True and ENABLE_OFFLINE_RECOGNITION is True):
            print("\n\nUsing Pocket Sphinx, because you're offline.\n\n")
            user_input = self.recognizer()
        elif(USE_VOICE_INPUT is True and online_status is False and ENABLE_OFFLINE_RECOGNITION is True):
            print("\n\nUsing Pocket Sphinx\n\n")
            user_input = self.recognizer()
        else:
            user_input = input("\n\nYour input:\n\n")
            user_input = str(user_input).lower()
        if(user_input and user_input!="exit" and user_input!="end"):
            return user_input
        else:
            self.get_input()

    async def make_a_request(self):
        request_body = {
            "prompt":self.get_input(),
            "model":self.chosen_model
        }
        print("\n\nWaiting for answer...\n\n")
        r = requests.post(self.default_url,json=request_body)
        try:
            self.chosen_model_return(None)
            if(r.text):
                data_list = r.text
                json_objects = [obj + '}' for obj in data_list.split('}') if obj.strip()]
                responses = [json.loads(obj)['response'] for obj in json_objects]
                response_line = ''.join(responses)
                bot_response = "\n\nBot response: {}\n\n".format(response_line) 
                return bot_response
            else:
                response_line = "No response"
                bot_response = "\n\nBot response: {}\n\n".format(response_line) 
                return bot_response
        except Exception as e:
            print("\n\nError: Reinitiating\n\n")