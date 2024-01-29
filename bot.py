import sqlite3
from fuzzywuzzy import fuzz, process

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('chatbot_database.db')
cursor = conn.cursor()

# Create a table to store questions and answers
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chatbot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
''')
conn.commit()

def get_answer_from_database(question):
    # Check if the question exists in the database
    cursor.execute('SELECT question, answer FROM chatbot')
    stored_questions = cursor.fetchall()

    # Find the most similar question using fuzzywuzzy
    similarity_threshold = 70  # Adjust as needed

    # Extract questions from the tuple list
    stored_questions = [q[0] for q in stored_questions]

    # Using process.extractOne to find the best match
    best_match, similarity_score = process.extractOne(question, stored_questions, scorer=fuzz.ratio)

    if similarity_score >= similarity_threshold:
        # Retrieve the answer using the matched question
        cursor.execute('SELECT answer FROM chatbot WHERE question = ?', (best_match,))
        result = cursor.fetchone()
        return result[0] if result else None
    else:
        return None

def save_answer_to_database(question, answer):
    # Save the question and answer to the database
    cursor.execute('INSERT INTO chatbot (question, answer) VALUES (?, ?)', (question, answer))
    conn.commit()

def chatbot():
    print("Welcome to the Chatbot! Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ")
        
        # Check for exit command
        if user_input.lower() == 'exit':
            break

        # Check if the question is in the database
        stored_answer = get_answer_from_database(user_input)

        if stored_answer:
            print(f"Chatbot: {stored_answer}")
        else:
            new_answer = input("Chatbot: I don't know the answer. What should I say? ")
            save_answer_to_database(user_input, new_answer)

    # Close the database connection when done
    conn.close()

# Run the chatbot
chatbot()
import sqlite3
from fuzzywuzzy import fuzz, process

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('chatbot_database.db')
cursor = conn.cursor()

# Create a table to store questions and answers
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chatbot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
''')
conn.commit()

def get_answer_from_database(question):
    # Check if the question exists in the database
    cursor.execute('SELECT question, answer FROM chatbot')
    stored_questions = cursor.fetchall()

    # Find the most similar question using fuzzywuzzy
    similarity_threshold = 70  # Adjust as needed

    # Extract questions from the tuple list
    stored_questions = [q[0] for q in stored_questions]

    # Using process.extractOne to find the best match
    best_match, similarity_score = process.extractOne(question, stored_questions, scorer=fuzz.ratio)

    if similarity_score >= similarity_threshold:
        # Retrieve the answer using the matched question
        cursor.execute('SELECT answer FROM chatbot WHERE question = ?', (best_match,))
        result = cursor.fetchone()
        return result[0] if result else None
    else:
        return None

def save_answer_to_database(question, answer):
    # Save the question and answer to the database
    cursor.execute('INSERT INTO chatbot (question, answer) VALUES (?, ?)', (question, answer))
    conn.commit()

def chatbot():
    print("Welcome to the Chatbot! Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ")
        
        # Check for exit command
        if user_input.lower() == 'exit':
            break

        # Check if the question is in the database
        stored_answer = get_answer_from_database(user_input)

        if stored_answer:
            print(f"Chatbot: {stored_answer}")
        else:
            new_answer = input("Chatbot: I don't know the answer. What should I say? ")
            save_answer_to_database(user_input, new_answer)

    # Close the database connection when done
    conn.close()

# Run the chatbot
chatbot()
