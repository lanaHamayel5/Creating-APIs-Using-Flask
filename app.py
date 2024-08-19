from flask import Flask, request, jsonify
from models import db,ma
from models.user import User
from models.address import Address
from models.phone_number import PhoneNumber
from models.schemas import UserSchema
 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)
ma.init_app(app)

 
@app.route('/')
def home():
    return get_all_users()


@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(users)), 200


@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    # if user is not None
    if user:
        user_schema = UserSchema()
        return jsonify(user_schema.dump(user)), 200
    return jsonify({"message": "User not found"}), 404


@app.route("/users", methods=["POST"])
def add_user(): 
    user_info = request.json
    
    # Validate required data
    if not user_info.get('first_name') or not user_info.get('last_name'):
        return jsonify({"message": "First name and last name are required"}), 400

    address_data = user_info.get('address', {})
    phone_number_data = user_info.get('phone_numbers', [])
 
    new_user = User(
        first_name=user_info.get('first_name'),
        last_name=user_info.get('last_name'),
        gender=user_info.get('gender'),
        age=user_info.get('age')
    )
    db.session.add(new_user)
    db.session.commit()
 
    new_user.address = Address(
        street_address=address_data.get('street_address'),
        city=address_data.get('city'),
        state=address_data.get('state'),
        postal_code=address_data.get('postal_code'),
        user=new_user
    )
   
    for phone_data in phone_number_data:
        phone_number = PhoneNumber(
            type=phone_data.get('type'),
            number=phone_data.get('number'),
            user=new_user
        )
        db.session.add(phone_number)
   
    db.session.commit()
    return jsonify({"id": new_user.id}), 201


@app.route('/users/<int:id>', methods=['PUT'])
def update_user_by_id(id):
    update_data = request.json
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Validate required fields
    if 'first_name' in update_data and not update_data['first_name']:
        return jsonify({"message": "First name cannot be empty"}), 400

    # Update user attributes
    user.first_name = update_data.get('first_name', user.first_name)
    user.last_name = update_data.get('last_name', user.last_name)
    user.gender = update_data.get('gender', user.gender)
    user.age = update_data.get('age', user.age)

    # Update or create address
    address_data = update_data.get('address')
    if address_data:
        if user.address:
            user.address.street_address = address_data.get('street_address', user.address.street_address)
            user.address.city = address_data.get('city', user.address.city)
            user.address.state = address_data.get('state', user.address.state)
            user.address.postal_code = address_data.get('postal_code', user.address.postal_code)
        else:
            user.address = Address(
                street_address=address_data['street_address'],
                city=address_data['city'],
                state=address_data['state'],
                postal_code=address_data['postal_code'],
                user=user
            )

    # Replace phone numbers
    phone_number_data = update_data.get('phone_numbers', [])
    if phone_number_data:
        # Remove existing phone numbers
        PhoneNumber.query.filter_by(user_id=id).delete()
        # Add new phone numbers
        for phone_data in phone_number_data:
            phone_number = PhoneNumber(
                type=phone_data['type'],
                number=phone_data['number'],
                user=user
            )
            db.session.add(phone_number)

    db.session.commit()
    return jsonify({"id": user.id}), 200


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user_by_id(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Delete associated address and phone numbers if they exist
    if user.address:
        db.session.delete(user.address)

    PhoneNumber.query.filter_by(user_id=id).delete()

    # Delete the user from the DB
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

   
if __name__ == "__main__":
    with app.app_context():
        # creating DB
        db.create_all()
    app.run(debug=True)
