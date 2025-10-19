from typingtest.database import get_connection
from typingtest.user import User

class Session:
    def __init__(self):
        self.user = None
        self.state = "HOME"   # stores the current state, for example, home/idle, test, settings, etc.
        self.universe = None
        self.test_performed = 0

    def set_current_state(self, state: str) -> None:
        if state not in ["HOME", "TEST", "SETTING"]: return 0
        self.state = state

    def get_current_user(self) -> User:
        return self.user

    def set_current_user(self, user_obj) -> None:
        self.user = user_obj
        self.universe = self.user.preferred_universe

    def remove_current_user(self) -> None:
        if self.user != None:
            print(f"The user ({self.user.username}) has been removed!")
            self.user = None

    def set_current_universe(self, universe: int) -> None:
        uni = ["play", "longtext", "dictionary"]
        self.universe = uni[(universe-1)]
    
    def fetch_user(self, username: str = None, user_id: int = None) -> User | None:
        cursor = get_connection().cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(64) UNIQUE, password VARCHAR(64), email VARCHAR(254));")
        cursor.execute("SELECT * FROM users;") # selecting all the data, and then checking as to add the ability to tell the user whether the username/password is wrong
        users_data = cursor.fetchall()
        cursor.close()

        for user in users_data:
            if user[1] == username or user[0] == user_id:
                return User(userid = user[0], username=user[1], email = user[3])
        else:
            return None

# Will be accessing this session variable everywhere
session = Session()