from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, first_name, last_name, email, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    @staticmethod
    def from_tuple(user_tuple):
        return User(
            id=user_tuple[0],
            first_name=user_tuple[1],
            last_name=user_tuple[2],
            email=user_tuple[3],
            password=user_tuple[4]
        )
