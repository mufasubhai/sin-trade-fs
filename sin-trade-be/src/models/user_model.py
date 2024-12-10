# models/user_model.py


class User:
# class User(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(50), unique=True, nullable=False)
    # password_hash = db.Column(db.String(128), nullable=False)

    id = 5
    username = "TEST"
    password_hash = 'password'
    def set_password(self, password):
    
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
def generate_password_hash(password):
    return "password"

def check_password_hash(password_hash, password):
    return True