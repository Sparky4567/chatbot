import speech_recognition as sr
from config import DEFAULT_MIC_TIMEOUT

class Speech_recognizers:
    def __init__(self):
        self.default_not_recognized_message = "Sphinx Recognition could not understand audio."
        self.default_google_not_recognized_message = "Could not understand audio."

    def recognize_speech_pocketsphinx(self):
        # INITIATING RECOGNIZER
            r = sr.Recognizer()
            # STARTING TO LISTEN TO MIC INPUT
            with sr.Microphone() as source:
                print("\n{}\n".format("Okay, say something! [Sphinx]"))
                # SETTING TIME LIMTIS
                try:
                    r.adjust_for_ambient_noise(source)
                    r.dynamic_energy_threshold = True
                except Exception as e:
                    print("\nException: {}\n".format(e))
                    self.recognize_speech_pocketsphinx()
                
                try:
                    audio = r.listen(source,phrase_time_limit=DEFAULT_MIC_TIMEOUT,timeout=DEFAULT_MIC_TIMEOUT)
                    # SETTING A DEFAULT LANGUAGE
                    # AND STARTING RECOGNISER
                    result = r.recognize_sphinx(audio,language="en-US")
                    # WAITING FOR A RESULT AND RETURNING IT BACK
                    final_result = ""
                    final_result = final_result + str("{}".format(result)).lower().strip()
                    final_result = str(final_result).strip().lower()
                    if(final_result!=""):
                        return final_result
                    else:
                        print("\n{}\n".format(self.default_not_recognized_message))
                        self.recognize_speech_pocketsphinx()
                except sr.UnknownValueError:
                    # THE THINGY CAN NOT UNDERSTAND THE PHRASE, SO IT STARTS THE RECOGNITION AGAIN
                    print("\n{}\n".format(self.default_not_recognized_message))
                    self.recognize_speech_pocketsphinx()
                except Exception as e:
                    # THE THINGY CAN NOT UNDERSTAND THE PHRASE, SO IT STARTS THE RECOGNITION AGAIN
                    if(str(e).lower().strip()=="" or str(e).lower().strip()==None):
                        print("\nSorry, can not recognize\n")
                        self.recognize_speech_pocketsphinx()
                    else:
                        print("\nException: {}\n".format(e))
                        self.recognize_speech_pocketsphinx()
                except sr.WaitTimeoutError:
                    print("\nTimeout\n")
                    self.recognize_speech_pocketsphinx()

    def recognize_speech(self):
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = True
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("\n{}\n".format("Okay, say something! [Google service]"))
            audio = recognizer.listen(source, phrase_time_limit=DEFAULT_MIC_TIMEOUT, timeout=DEFAULT_MIC_TIMEOUT)
        try:
            result = ""
            text = str(recognizer.recognize_google(audio))
            result = result + text
            result = str(result).strip().lower()
            if(result!=""):
                return result
            else:
                print("\n\n{}\n\n".format(self.default_google_not_recognized_message))
                self.recognize_speech()
            
        except sr.WaitTimeoutError:
            print("\n\nRecognition timed out.\n\n")
            self.recognize_speech()
        except sr.UnknownValueError:
            print("\n\n{}\n\n").format(self.default_google_not_recognized_message)
            self.recognize_speech()
        except sr.RequestError as e:
            print("\n\Request error.\n\n")
            self.recognize_speech()

