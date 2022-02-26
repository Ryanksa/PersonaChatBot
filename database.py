import sqlite3


def connect_to_db():
    global connection
    global cursor
    connection = sqlite3.connect('lite.db', check_same_thread=False)
    cursor = connection.cursor()


def disconnect_from_db():
    connection.close()


def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatbot
        (id TEXT, name TEXT)
    ''')
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS personas 
      (id INTEGER PRIMARY KEY AUTOINCREMENT, bot_id TEXT, content TEXT, FOREIGN KEY (bot_id) REFERENCES chatbot (id))
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dialogues 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, bot_id TEXT, content TEXT, FOREIGN KEY (bot_id) REFERENCES chatbot (id))
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_personas 
        ON personas (bot_id);
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_dialogues 
        ON dialogues (bot_id);
    ''')

    connection.commit()


def get_chatbot(id):
    chatbots = cursor.execute('''
        SELECT * FROM chatbot WHERE id = ? 
    ''', (id,))
    return chatbots.fetchone()


def create_chatbot(id, name):
    cursor.execute('''
        INSERT INTO chatbot VALUES (?, ?)
    ''', (id, name,))
    connection.commit()


def get_persona(bot_id):
    persona = cursor.execute('''
        SELECT * FROM personas WHERE bot_id = ? 
    ''', (bot_id,))
    return persona.fetchall()


def add_persona(bot_id, content):
    cursor.execute('''
        INSERT INTO personas (bot_id, content) VALUES (?, ?)
    ''', (bot_id, content,))
    connection.commit()


def get_dialogue(bot_id):
    dialogues = cursor.execute('''
        SELECT * FROM dialogues WHERE bot_id = ? ORDER BY id ASC
    ''', (bot_id,))
    return dialogues.fetchall()


def add_dialogue(bot_id, content):
    cursor.execute('''
        INSERT INTO dialogues (bot_id, content) VALUES (?, ?)
    ''', (bot_id, content,))
    connection.commit()
