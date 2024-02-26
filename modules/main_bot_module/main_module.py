import sqlite3
from fuzzywuzzy import fuzz, process
import random
from googletrans import Translator
import requests
import speech_recognition as sr
from config import USE_TRANSLATION_SERVICE
from config import USE_VOICE_INPUT
from config import ENABLE_OFFLINE_RECOGNITION
from config import SIMILARITY_SCORE
from modules.is_online.is_online import Is_Online
from modules.speak_back.speak_module import Speak_Back
from modules.speech_recognizers.speech_recognizers import Speech_recognizers
from modules.random_emoji_module.random_emoji import Random_Emoji
from modules.predefined_commands.predefined_commands_module import Predefined_Commands
from modules.logo_print_module.logo_module import Logo_Module
from config import USE_PREDEFINED_COMMANDS
from config import CONTINUOUS_LEARNING
class Main_Module:
    def __init__(self):
        self.temp = ""
        self.conn = sqlite3.connect('database/chatbot_database.db')
        self.cursor = self.conn.cursor()
        self.is_online = Is_Online()
        self.speak_module = Speak_Back()
        self.speech_recognizers = Speech_recognizers()
        self.emoji_picker = Random_Emoji()
        self.offline_message = "Your offline. Translation services won't be used."
        self.predefined_commands = Predefined_Commands()
        self.logo = Logo_Module()
        
    def manage_database_creation(self):
        
        # Create a table to store questions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT
            )
        ''')
        # Create a table to store answers linked to questions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER,
                answer TEXT,
                FOREIGN KEY (question_id) REFERENCES questions (id)
            )
        ''')
        self.conn.commit()

    def get_answers_from_database(self,question):
        # Check if the question exists in the database
        self.cursor.execute('SELECT id FROM questions WHERE question = ?', (question,))
        question_id = self.cursor.fetchone()

        if question_id:
            # Retrieve all answers associated with the question
            self.cursor.execute('SELECT answer FROM answers WHERE question_id = ?', question_id)
            results = self.cursor.fetchall()
            return [result[0] for result in results]
        else:
            return None

    def return_translated_text(self,passed_phrase):
        if(USE_TRANSLATION_SERVICE is True):
            translator = Translator()
            # Detect the language of the input text
            detected_language = translator.detect(passed_phrase).lang
            # Translate the text to English (you can choose a different target language if needed)
            translated_text = translator.translate(passed_phrase, src=detected_language, dest='en').text
            user_approval=str(input(str("\n\nDo you want to approve translation: {}? (y)\n\n").format(translated_text)))
            if(user_approval == "y"):
                return translated_text
            else:
                user_input=str(input("\n\nWrite your answer:\n\n"))
                return user_input
        else:
            return passed_phrase

    def find_best_match(self,question):
        # Check if the question exists in the database
        self.cursor.execute('SELECT question FROM questions')
        stored_questions = self.cursor.fetchall()

        # Extract questions from the tuple list
        stored_questions = [q[0] for q in stored_questions]
        question = str(question)
        stored_questions = [str(q) for q in stored_questions]
        # Using process.extractOne to find the best match
        result = process.extractOne(question, stored_questions, scorer=fuzz.ratio)
        similarity_threshold = SIMILARITY_SCORE  # Adjust as needed
        if result and result[1] >= similarity_threshold:
            best_match, similarity_score = result
            return best_match, similarity_score
        else:
            return None, 0  # Return a default value when no match is found or the similarity is below the threshold


    def save_question_and_answers_to_database(self,question, answers):
        # Save the question to the questions table
        self.cursor.execute('INSERT INTO questions (question) VALUES (?)', (question,))
        self.conn.commit()

        # Retrieve the question_id for the newly inserted question
        self.cursor.execute('SELECT id FROM questions WHERE question = ?', (question,))
        question_id = self.cursor.fetchone()[0]

        # Save each answer to the answers table, linked to the question
        if(self.is_online.is_online() is False):
            if(len(answers)>1):
                for answer in answers:  
                    self.cursor.execute('INSERT INTO answers (question_id, answer) VALUES (?, ?)', (question_id, str(answer).lower()))
                    self.conn.commit()
            else:
                self.cursor.execute('INSERT INTO answers (question_id, answer) VALUES (?, ?)', (question_id, str(answers[0]).lower()))
                self.conn.commit()
        else:
            if(self.is_online.is_online() is False):
                    print("\n\n{}\n\n".format(self.offline_message))
            if(len(answers)>1):
                for answer in answers:  
                    answer = self.return_translated_text(answer)
                    self.cursor.execute('INSERT INTO answers (question_id, answer) VALUES (?, ?)', (question_id, str(answer).lower()))
                    self.conn.commit()
            else:
                answer = self.return_translated_text(answers[0])
                self.cursor.execute('INSERT INTO answers (question_id, answer) VALUES (?, ?)', (question_id, str(answer).lower()))
                self.conn.commit()


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
            if(USE_PREDEFINED_COMMANDS is True and self.predefined_commands.check_command_list(str(text)) is True):
                print("\n\n{}\n\n".format("Recognized a predefined command and executing it"))
                if(USE_VOICE_INPUT is True):
                    print("\n\n{}\n\n".format("Reinitiating speech recognition"))
                self.recognizer_engine()
            else:
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
            if(res == "exit" or res =="end"):
                quit()
            return res

    def chatbot(self):
        self.logo.print_logo()
        print("Welcome to the Chatbot! Type 'exit' to end the conversation.")

        while True:
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
                user_input = input("You: ")
                user_input = str(user_input).lower()

            # Check for exit command
            if user_input == 'exit':
                # Close the database connection when done
                self.conn.close()
                quit()
                break

            if(USE_PREDEFINED_COMMANDS is True and self.predefined_commands.check_command_list(user_input) is True):
                print("\n\n{}\n\n".format("Recognized a predefined command and executing it"))
                print("\n\n{}\n\n".format("Reinitiating speech recognition"))
                self.chatbot()

            # Find the best matching question
            best_match, similarity_score = self.find_best_match(user_input)

            # Check if similarity score is above a certain threshold
            similarity_threshold = SIMILARITY_SCORE  # Adjust as needed
            
            if best_match is not None and similarity_score >= similarity_threshold:
                stored_answers = self.get_answers_from_database(best_match)
                if(len(stored_answers)>1):
                    stored_answers = random.choice(stored_answers)
                    if stored_answers:
                        answer = stored_answers
                        self.speak_module.speak_back(answer)
                        print(f"Chatbot: {str(answer.upper())} {self.emoji_picker.pick_random()}")
                    else:
                        new_answers = input("Chatbot: I don't know the answer. What should I say? (Separate multiple answers with |): ")
                        if(str(new_answers).__contains__("|")):
                            new_answers_list = [ans.strip() for ans in new_answers.split('|')]
                            self.save_question_and_answers_to_database(best_match, new_answers_list)
                        else:
                            self.save_question_and_answers_to_database(best_match, [new_answers])
                else:
                    stored_answers = random.choice(stored_answers)
                    if stored_answers:
                        answer = stored_answers
                        self.speak_module.speak_back(answer)
                        print(f"Chatbot: {str(answer.upper())} {self.emoji_picker.pick_random()}")
                    else:
                        new_answers = input("Chatbot: I don't know the answer. What should I say? (Separate multiple answers with |): ")
                        if(str(new_answers).__contains__("|")):
                            new_answers_list = [ans.strip() for ans in new_answers.split('|')]
                            self.save_question_and_answers_to_database(best_match, new_answers_list)
                        else:
                            self.save_question_and_answers_to_database(best_match, [new_answers])
                    
            else:
                new_answers = input("Chatbot: I don't know the answer. What should I say? (Separate multiple answers with |): ")
                if(str(new_answers).__contains__("|")):
                    new_answers_list = [ans.strip() for ans in new_answers.split('|')]
                    self.save_question_and_answers_to_database(user_input, new_answers_list)
                else:
                    self.save_question_and_answers_to_database(user_input, [new_answers])

                



