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
        print(f"The current user has been set to: {self.user.username}")

        #adding code here to change universe to user's preferred universe as the user has currently logged in
        self.universe = self.user.preferred_universe

    def remove_current_user(self) -> None:
        if self.user != None:
            print(f"The user ({self.user.username}) has been removed!")
            self.user = None

    def get_session_data():
        pass

    def set_current_universe(self, universe: int) -> None:
        uni = ["play", "longtext", "dictionary"]
        self.universe = uni[universe]

# Will be accessing this session variable everywhere
session = Session()