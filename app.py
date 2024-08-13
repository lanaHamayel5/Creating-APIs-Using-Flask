import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def load_data():
    with open('users.json', 'r') as file:
        return json.load(file)

def save_data(data):
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4)
@app.route('/')
@app.route('/users', methods=['GET'])
def get_users_list():
    data = load_data()
    return jsonify(data)

@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    data = load_data()
    for user in data:
        if user['id'] == id:
            return jsonify(user)
    return jsonify({"message": "User not found"}), 404

@app.route('/users', methods=['POST'])
def add_user():
    user_info = request.json
    data = load_data()

    address = user_info.get('address', {})
    phone_numbers = user_info.get('phone_numbers', [])

    new_user = {
        'id': user_info.get('id'),
        'first_name': user_info.get('first_name'),
        'last_name': user_info.get('last_name'),
        'gender': user_info.get('gender'),
        'age': user_info.get('age'),
        'address': {
            'street_address': address.get('street_address'),
            'city': address.get('city'),
            'state': address.get('state'),
            'postal_code': address.get('postal_code')
        },
        'phone_numbers': [
            {
                'type': phone.get('type'),
                'number': phone.get('number')
            } for phone in phone_numbers
        ]
    }
    
    data.append(new_user)
    save_data(data)
    
    return jsonify(new_user['id']), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = load_data()
    for user in data:
        if user['id'] == id:
            updated_data = request.json
            user.update(updated_data)
            save_data(data)
            return jsonify(user)
    return jsonify({"message": "User not found"}), 404

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    data = load_data()
    for user in data:
        if user['id'] == id:
            data.remove(user)
            save_data(data)
            return jsonify({"message": "User deleted"}), 200

    return jsonify({"message": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
