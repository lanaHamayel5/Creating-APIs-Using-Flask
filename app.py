from flask import Flask, request, jsonify
from models import db
from models.user import User
from models.address import Address
from models.phone_number import PhoneNumber
 
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
 
 
@app.route("/users", methods=["POST"])
def add_user():
    user_info = request.json
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
 

@app.route("/users", methods=["GET"])
def get_all_users():
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
                {"type": phone.type, "number": phone.number}
                for phone in user.phone_numbers
            ]
        }
        all_users.append(user_data)
    return jsonify(all_users), 200


@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    if user:
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
 

@app.route('/users/<int:id>', methods=['PUT'])
def update_user_by_id(id):
    update_data = request.json
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found"}), 404

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

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

   
if __name__ == "__main__":
    with app.app_context():
        # create DB
        db.create_all()
    app.run(debug=True)
