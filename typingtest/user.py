from .database import get_connection

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.new_user = None

        self.fetch_user_detail()

    def fetch_user_detail(self):
        # cursor = get_connection().cursor()

        # # fetching details about race
        # cursor.execute("CREATE TABLE IF NOT EXISTS races ()")

        print("Will fetch the user data here")

