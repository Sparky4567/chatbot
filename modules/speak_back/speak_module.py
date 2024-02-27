from config import SPEAK_BACK
import subprocess

class Speak_Back:
    def __init__(self):
        self.model = "en_US-amy-medium.onnx"

    def speak_back(self,answer):
        
        answer = str(answer).replace(":",".").replace("!",".").replace("\\",".").replace("/",".").replace("-",".").replace("~",".").replace("'",".").split(".")
        final_answer = ""
        for a in answer:
            a = str(a).strip()
            final_answer = final_answer+a
        final_answer = str(final_answer).strip()
        if(SPEAK_BACK is True):
            command = "cd ./venv/piper && echo '{}' | \
            ./piper --model {} --output-raw | \
            aplay -r 22050 -f S16_LE -t raw -".format(final_answer,self.model)
            result = subprocess.run(command, shell=True, check=True, text=True)
