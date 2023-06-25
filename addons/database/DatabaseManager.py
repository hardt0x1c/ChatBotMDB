import sqlite3


class DatabaseManager:
    def __init__(self, db_file):
        # Принимаем путь до БД
        self.db_file = db_file
        # Создание подключения к базе данных
        self.conn = sqlite3.connect(self.db_file)
        # Создание курсора для выполнения SQL-запросов
        self.cursor = self.conn.cursor()

    def create_database(self):
        # SQL-запрос для создания таблицы "users"
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY NOT NULL,
                    user_id INTEGER UNIQUE NOT NULL,
                    username TEXT UNIQUE NOT NULL
                )
                ''')

        # Сохранение изменений и закрытие соединения
        self.conn.commit()

    def get_user(self, user_id):
        return self.cursor.execute("SELECT * FROM users WHERE user_id=?;", (user_id,)).fetchone()

    def add_user(self, user_id):
        try:
            self.cursor.execute("INSERT INTO users (user_id) VALUES (?);", (user_id,))
            self.conn.commit()
            return True
        except:
            return False

    def get_users(self):
        self.cursor.execute('''SELECT user_id FROM users''')
        spam_base = self.cursor.fetchall()
        return spam_base
