from typingtest.database import get_connection

class User:
    def __init__(self, userid: int, username: str, password: str = None, email: str = None):
        self.user_id = userid
        self.username = username
        self.password = password
        self.email = email
        self.new_user = None

        #storing user settings
        self.dictionary_word_limit = None
        self.preferred_universe = None

        #self.fetch_user_detail()
        self.fetch_user_settings()

    def fetch_user_race_info(self, universe: str = None, text_id: int | str = None, order: bool = False) -> list | None:
        cursor = get_connection().cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS races (race_number INT AUTO_INCREMENT PRIMARY KEY, user_id INT, username VARCHAR(64), universe VARCHAR(64), text_id VARCHAR(64), wpm FLOAT(7,4), accuracy FLOAT(5, 4), epoch VARCHAR(64));")

        if universe is None and text_id is None: cursor.execute(f"SELECT * FROM races WHERE user_id = {self.user_id}" + (" ORDER BY wpm DESC;" if order else ";"))
        elif universe is not None and text_id is None: cursor.execute(f"SELECT * FROM races WHERE user_id = {self.user_id} && universe = '{universe}'" + (" ORDER BY wpm DESC;" if order else ";"))
        else: cursor.execute(f"SELECT * FROM races WHERE user_id = {self.user_id} && universe = '{universe}' && text_id = '{text_id}'" + (" ORDER BY wpm DESC;" if order else ";"))

        data = cursor.fetchall() #list of tuples (row -> tuple)
        cursor.close()

        if len(data) == 0: return None
        else: return data
    
    def fetch_race_info(self, universe: str, text_id: int | str = None) -> list | None:
        cursor = get_connection().cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS races (race_number INT AUTO_INCREMENT PRIMARY KEY, user_id INT, username VARCHAR(64), universe VARCHAR(64), text_id VARCHAR(64), wpm FLOAT(7,4), accuracy FLOAT(5, 4), epoch VARCHAR(64));")

        if text_id is None: cursor.execute(f"SELECT * FROM races WHERE universe = '{universe}' ORDER BY wpm DESC;")
        else: cursor.execute(f"SELECT * FROM races WHERE universe = '{universe}' && text_id = '{text_id}' ORDER BY wpm DESC;")

        data = cursor.fetchall()
        cursor.close()

        if len(data) == 0: return None
        else: return data

    def fetch_user_detail(self):
        pass
    
    def fetch_user_settings(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS settings (user_id INT PRIMARY KEY, username VARCHAR(64) UNIQUE, preferred_universe VARCHAR(64), dictionary_word_limit INT);")
        cursor.execute(f"SELECT * FROM settings WHERE user_id = {self.user_id}")
        data = cursor.fetchall()

        if len(data) == 0:
            cursor.execute(f"INSERT INTO settings (user_id, username, preferred_universe, dictionary_word_limit) VALUES({self.user_id}, '{self.username}', 'play', 50);")

            self.dictionary_word_limit = 50
            self.preferred_universe = 'play'
        else:
            self.preferred_universe = data[0][2]
            self.dictionary_word_limit = data[0][3]

        cursor.close()
        conn.commit()

        # return {
        #     "user_id": self.user_id,
        #     "preferred_universe": data[2] if len(data) != 0 else 'play',
        #     "dictionary_word_limit": data[3] if len(data) != 0 else 50
        # }
    
    def get_user_settings(self) -> dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "preferred_universe": self.preferred_universe,
            "dictionary_word_limit": self.dictionary_word_limit
        }
    
    def set_dictionary_word_limit(self, new_limit: int):
        self.dictionary_word_limit = new_limit

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"UPDATE settings SET dictionary_word_limit = {new_limit} WHERE user_id = '{self.user_id}';")
        cursor.close()
        conn.commit()

    def set_preferred_universe(self, new_universe: int):
        uni = ["play", "longtext", "dictionary"]
        self.preferred_universe = uni[new_universe]
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE settings SET preferred_universe = '{uni[new_universe]}' WHERE user_id = '{self.user_id}';")
        cursor.close()
        conn.commit()

    def set_user_email(self, email: str):
        if email == self.email: return
        self.email = email

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET email = '{email}' WHERE user_id = '{self.user_id}'")
        cursor.close()
        conn.commit()