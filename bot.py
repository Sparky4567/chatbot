import sqlite3
from fuzzywuzzy import fuzz, process
import subprocess
import random
from googletrans import Translator
import requests
import speech_recognition as sr
from config import USE_TRANSLATION_SERVICE
from config import SPEAK_BACK
from config import USE_VOICE_INPUT
# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('chatbot_database.db')
cursor = conn.cursor()

# Create a table to store questions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT
    )
''')

# Create a table to store answers linked to questions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        answer TEXT,
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )
''')

conn.commit()

def recognize_speech():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("\n\nSay something:\n\n")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return None


def get_answers_from_database(question):
    # Check if the question exists in the database
    cursor.execute('SELECT id FROM questions WHERE question = ?', (question,))
    question_id = cursor.fetchone()

    if question_id:
        # Retrieve all answers associated with the question
        cursor.execute('SELECT answer FROM answers WHERE question_id = ?', question_id)
        results = cursor.fetchall()
        return [result[0] for result in results]
    else:
        return None

def is_online():
    try:
        # Try to send a request to a well-known server (e.g., Google's public DNS server)
        response = requests.get("http://8.8.8.8", timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

def return_translated_text(passed_phrase):
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



def find_best_match(question):
    # Check if the question exists in the database
    cursor.execute('SELECT question FROM questions')
    stored_questions = cursor.fetchall()

    # Extract questions from the tuple list
    stored_questions = [q[0] for q in stored_questions]
    question = str(question)
    stored_questions = [str(q) for q in stored_questions]
    # Using process.extractOne to find the best match
    result = process.extractOne(question, stored_questions, scorer=fuzz.ratio)
    similarity_threshold = 70  # Adjust as needed
    if result and result[1] >= similarity_threshold:
        best_match, similarity_score = result
        return best_match, similarity_score
    else:
        return None, 0  # Return a default value when no match is found or the similarity is below the threshold


def save_question_and_answers_to_database(question, answers):
    # Save the question to the questions table
    cursor.execute('INSERT INTO questions (question) VALUES (?)', (question,))
    conn.commit()

    # Retrieve the question_id for the newly inserted question
    cursor.execute('SELECT id FROM questions WHERE question = ?', (question,))
    question_id = cursor.fetchone()[0]

    # Save each answer to the answers table, linked to the question
    if(is_online is False):
        if(len(answers)>1):
            for answer in answers:  
                cursor.execute('INSERT INTO answers (question_id, answer) VALUES (?, ?)', (question_id, str(answer).lower()))
                conn.commit()
        else:
            cursor.execute('INSERT INTO answers (question_id, answer) VALUES (?, ?)', (question_id, str(answers[0]).lower()))
            conn.commit()
    else:
        if(len(answers)>1):
            for answer in answers:  
                answer = return_translated_text(answer)
                cursor.execute('INSERT INTO answers (question_id, answer) VALUES (?, ?)', (question_id, str(answer).lower()))
                conn.commit()
        else:
            answer = return_translated_text(answers[0])
            cursor.execute('INSERT INTO answers (question_id, answer) VALUES (?, ?)', (question_id, str(answer).lower()))
            conn.commit()


def speak_back(answer):
    if(SPEAK_BACK is True):
        model = "en_US-amy-medium.onnx"        
        command = "cd ./venv/piper && echo '{}' | \
        ./piper --model {} --output-raw | \
        aplay -r 22050 -f S16_LE -t raw -".format(answer,model)
        result = subprocess.run(command, shell=True, check=True, text=True)

   
def recognizer():
    user_input = input("\n\nPress 'r' to record\n\n")

    if user_input.lower() == 'r':
        text = recognize_speech()

        if text:
            # Use the 'text' variable for further processing
            print(str("\n\nRecognized text:{}\n\n").format(text))
            user_input=input("\n\nWant to approve question ? (y)\n\n")
            if(str(user_input).lower()=="y"):
                recognized_phrase = text
                return recognized_phrase
        else:
            print("\n\nI did not manage to understand your voice input. Reinitiating.\n\n")
            recognizer()
    else:
        recognizer()
def chatbot():
    print("Welcome to the Chatbot! Type 'exit' to end the conversation.")

    while True:
        if(USE_VOICE_INPUT is True and is_online() is True):
            user_input = recognizer()
        else:
            user_input = input("You: ")

        # Check for exit command
        if user_input.lower() == 'exit':
            break

        # Find the best matching question
        best_match, similarity_score = find_best_match(user_input)

        # Check if similarity score is above a certain threshold
        similarity_threshold = 70  # Adjust as needed
        
        if best_match is not None and similarity_score >= similarity_threshold:
            stored_answers = get_answers_from_database(best_match)
            if(len(stored_answers)>1):
                stored_answers = random.choice(stored_answers)
                if stored_answers:
                    answer = stored_answers
                    speak_back(answer)
                    print(f"Chatbot: {str(answer.upper())}")
                else:
                    new_answers = input("Chatbot: I don't know the answer. What should I say? (Separate multiple answers with |): ")
                    if(str(new_answers).__contains__("|")):
                        new_answers_list = [ans.strip() for ans in new_answers.split('|')]
                        save_question_and_answers_to_database(best_match, new_answers_list)
                    else:
                        save_question_and_answers_to_database(best_match, [new_answers])
            else:
                stored_answers = random.choice(stored_answers)
                if stored_answers:
                    answer = stored_answers
                    speak_back(answer)
                    print(f"Chatbot: {str(answer.upper())}")
                else:
                    new_answers = input("Chatbot: I don't know the answer. What should I say? (Separate multiple answers with |): ")
                    if(str(new_answers).__contains__("|")):
                        new_answers_list = [ans.strip() for ans in new_answers.split('|')]
                        save_question_and_answers_to_database(best_match, new_answers_list)
                    else:
                        save_question_and_answers_to_database(best_match, [new_answers])
                    
        else:
            new_answers = input("Chatbot: I don't know the answer. What should I say? (Separate multiple answers with |): ")
            if(str(new_answers).__contains__("|")):
                new_answers_list = [ans.strip() for ans in new_answers.split('|')]
                save_question_and_answers_to_database(user_input, new_answers_list)
            else:
                save_question_and_answers_to_database(user_input, [new_answers])

    # Close the database connection when done
    conn.close()

# Run the chatbot
chatbot()


