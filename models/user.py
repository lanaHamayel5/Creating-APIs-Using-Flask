from models import db

class User(db.Model):
    """Model representing a user with relevant details."""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(15), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.relationship('Address', backref='user', uselist=False)
    phone_numbers = db.relationship('PhoneNumber', backref='user', lazy=True)

    def __repr__(self):
        return (f"<User(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', "
                f"gender='{self.gender}', age={self.age}, address={self.address}, phone_numbers={self.phone_numbers})>")
