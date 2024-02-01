from config import SPEAK_BACK
import subprocess

class Speak_Back:
    def __init__(self):
        self.model = "en_US-amy-medium.onnx"

    def speak_back(self,answer):
        if(SPEAK_BACK is True):
            command = "cd ./venv/piper && echo '{}' | \
            ./piper --model {} --output-raw | \
            aplay -r 22050 -f S16_LE -t raw -".format(answer,self.model)
            result = subprocess.run(command, shell=True, check=True, text=True)
