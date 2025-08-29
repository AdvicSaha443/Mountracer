class Session:
    def __init__(self):
        self.user = None

    def get_current_user(self):
        return self.user

    def set_current_user(self, user_obj):
        self.user = user_obj
        print(f"The current user has been set to: {self.user.username}")

        return 1

    def remove_current_user(self):
        if self.user != None:
            print(f"The user ({self.user.username}) has been removed!")
            self.user = None

# Will be accessing this session variable everywhere
session = Session()
    