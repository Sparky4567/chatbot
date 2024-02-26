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
                    return False
                
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
                        return False
                except sr.UnknownValueError:
                    # THE THINGY CAN NOT UNDERSTAND THE PHRASE, SO IT STARTS THE RECOGNITION AGAIN
                    print("\n{}\n".format(self.default_not_recognized_message))
                    return False
                except Exception as e:
                    # THE THINGY CAN NOT UNDERSTAND THE PHRASE, SO IT STARTS THE RECOGNITION AGAIN
                    if(str(e).lower().strip()=="" or str(e).lower().strip()==None):
                        print("\nSorry, can not recognize\n")
                        return False
                    else:
                        print("\nException: {}\n".format(e))
                        return False
                except sr.WaitTimeoutError:
                    print("\nTimeout\n")
                    return False

    def recognize_speech(self):
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = True
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("\n{}\n".format("Okay, say something! [Google service]"))
            try:
                audio = recognizer.listen(source, phrase_time_limit=DEFAULT_MIC_TIMEOUT, timeout=DEFAULT_MIC_TIMEOUT)
                print("\n\n{}\n\n".format("Timeout error"))
            except:
                return False
        try:
            result = ""
            text = str(recognizer.recognize_google(audio))
            result = result + text
            result = str(result).strip().lower()
            if(result!=""):
                return result
            else:
                print("\n\n{}\n\n".format(self.default_google_not_recognized_message))
                return False
            
        except sr.WaitTimeoutError:
            return False
        except sr.UnknownValueError:
            return False
        except sr.RequestError as e:
            print("\n\Request error.\n\n")
            return False

