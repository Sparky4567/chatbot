import sqlite3
from fuzzywuzzy import fuzz, process
import subprocess
import random
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
    if(len(answers)>1):
        for answer in answers:
            cursor.execute('INSERT INTO answers (question_id, answer) VALUES (?, ?)', (question_id, str(answer).lower()))
            conn.commit()
    else:
        cursor.execute('INSERT INTO answers (question_id, answer) VALUES (?, ?)', (question_id, str(answers[0]).lower()))
        conn.commit()

def speak_back(answer):
    model = "en_US-amy-medium.onnx"        
    command = "cd ./venv/piper && echo '{}' | \
    ./piper --model {} --output-raw | \
    aplay -r 22050 -f S16_LE -t raw -".format(answer,model)
    result = subprocess.run(command, shell=True, check=True, text=True)

def chatbot():
    print("Welcome to the Chatbot! Type 'exit' to end the conversation.")

    while True:
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


