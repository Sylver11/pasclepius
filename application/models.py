from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):

    def details(self, name, username, email):
        self.name = name
        self.username = username
        self.email = email

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
        return self.password

    def check_password(self, hashed_password, password):
        """Check hashed password."""
        return check_password_hash(hashed_password, password)

    pass
