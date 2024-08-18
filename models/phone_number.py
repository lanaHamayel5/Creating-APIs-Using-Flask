from models import db

class PhoneNumber(db.Model):
    """Model representing a user's phone_number with relevant details."""
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<PhoneNumber(id={self.id}, type='{self.type}', number='{self.number}')>"
