from models import db

class Address(db.Model):
    """Model representing a user's address with relevant details."""
    id = db.Column(db.Integer, primary_key=True)
    street_address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return (f"<Address(id={self.id}, street_address='{self.street_address}', "
                f"city='{self.city}', state='{self.state}', postal_code='{self.postal_code}')>")
