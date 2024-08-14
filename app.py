from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# Set the URI for the SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'


# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)


class Address(db.Model):
    # Define the Address model with fields
    id = db.Column(db.Integer(),primary_key=True)
    street_address = db.Column(db.String(100),nullable=False)
    city = db.Column(db.String(50),nullable=False)
    state = db.Column(db.String(50),nullable=False)
    postal_code = db.Column(db.String(20),nullable=False)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False)
    
    def __repr__(self):
        return (f"<Address(id={self.id}, street_address='{self.street_address}', "
                f"city='{self.city}', state='{self.state}', postal_code='{self.postal_code}')>")

     
class PhoneNumber(db.Model):
    # Define the PhoneNumber model with fields 
    id = db.Column(db.Integer(),primary_key= True)
    type = db.Column(db.String(20),nullable=False)
    number = db.Column(db.String(20),nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)    
    def __repr__(self):
        return f"<PhoneNumber(id={self.id}, type='{self.type}', number='{self.number}')>"
 
    
class User(db.Model):
    # Define the User model with fields 
    id = db.Column(db.Integer(),primary_key=True) 
    first_name = db.Column(db.String(20),unique=False,nullable=False)
    last_name = db.Column(db.String(20),unique=False,nullable=False)
    gender = db.Column(db.String(15),unique=False,nullable=False)
    age = db.Column(db.Integer(),unique=False,nullable=False)
    # lazy : determind the way to get the related data
    address = db.relationship('Address',backref='user',uselist=False)
    phone_numbers = db.relationship('PhoneNumber', backref='user', lazy=True)
    
    def __repr__(self):
        return (f"<User(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', "
                f"gender='{self.gender}', age={self.age}, address={self.address}, phone_numbers={self.phone_number})>")


@app.route("/users",methods=["POST"])
def add_user():
    # Retrieve the JSON data from the request
    user_info = request.json
    
    address_data = user_info.get('address',{})
    phone_number_data = user_info.get('phone_numbers', [])

    
    new_user = User(
        # database handle the id
        first_name = user_info.get('first_name'),
        last_name = user_info.get('last_name'),
        gender = user_info.get('gender'),
        age = user_info.get('age')
    )
    db.session.add(new_user)
    db.session.commit()
    
    # Create a new User instance 
    new_user.address = Address(
        street_address = address_data.get('street_address'),
        city = address_data.get('city'),
        state = address_data.get('state'),
        postal_code = address_data.get('postal_code'),
        user = new_user
    )
    
    for phone_data in phone_number_data:
        phone_number = PhoneNumber(
            type=phone_data.get('type'),
            number=phone_data.get('number'),
            user = new_user
        
        )
        db.session.add(phone_number)
        
    db.session.add(new_user)
    db.session.commit()  
    return jsonify({"id": new_user.id}), 201
 
    
@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    """
    Retrieve a user by their ID.

    Args:
        id (int): The ID of the user to retrieve.

    Returns:
        Response: A JSON response containing the user's data if found, 
                  or a 404 error message if not found.
    """

    # Query the database for a user with the given ID
    user = User.query.get(id)
    
    if user:
        # Convert the user object to a dictionary for JSON serialization
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'age': user.age,
            'address': {
                'street_address': user.address.street_address if user.address else None,
                'city': user.address.city if user.address else None,
                'state': user.address.state if user.address else None,
                'postal_code': user.address.postal_code if user.address else None
            } if user.address else None,
            'phone_numbers': [
                {'type': phone.type, 'number': phone.number}
                for phone in user.phone_numbers
            ]
        }
        return jsonify(user_data), 200
    
    return jsonify({"message": "User not found"}), 404
 
 
@app.route("/users", methods=["GET"])
def get_all_users():
    """
    Retrieve all users from the database.

    Returns:
        Response: A JSON response containing a list of all users, 
                  with each user's data.
    """
    users = User.query.all()
    all_users = []
    
    for user in users:
        user_data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "gender": user.gender,
            "age": user.age,
            "address": {
                "street_address": user.address.street_address,
                "city": user.address.city,
                "state": user.address.state,
                "postal_code": user.address.postal_code
            } if user.address else None,
            "phone_numbers": [
                {
                    "type": phone.type,
                    "number": phone.number
                } for phone in user.phone_numbers
            ]
        }
        all_users.append(user_data)
    
    return jsonify(all_users), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all() # Create all tables in the database
    app.run(debug=True)
