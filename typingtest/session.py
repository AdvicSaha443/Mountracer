class Session:
    def __init__(self):
        self.user = None
        self.state = "HOME"   # stores the current state, for example, home/idle, test, settings, etc.
        self.universe = "play"

    def set_current_state(self, state: str):
        if state not in ["HOME", "TEST", "SETTING"]: return 0
        self.state = state

    def get_current_user(self):
        return self.user

    def set_current_user(self, user_obj):
        self.user = user_obj
        print(f"The current user has been set to: {self.user.username}")

    def remove_current_user(self):
        if self.user != None:
            print(f"The user ({self.user.username}) has been removed!")
            self.user = None

    def get_session_data():
        pass

# Will be accessing this session variable everywhere
session = Session()