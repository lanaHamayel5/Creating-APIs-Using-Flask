import json
from flask import Flask, request, jsonify


app = Flask(__name__)


def load_data():
    """
    Load user data from the 'user.json' file.add()
    
    Returns:
        list: A list of dictionaries, each representing a user's data.
    """
    with open('users.json', 'r') as file:
        return json.load(file)
    

def save_data(data):
    """
    Save the given user data to the 'users.json' file.
    
    Args:
        data (list): A list of dictionaries, each representing a user's data.
    """
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4)
        
@app.route('/')
@app.route('/users', methods=['GET'])
def get_users_list():
    """
    Retrieve the list of all users.

    Returns:
        Response: A JSON response containing a list of all users.
    """
    data = load_data()
    return jsonify(data)

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
    data = load_data()
    for user in data:
        if user['id'] == id:
            return jsonify(user),200
    return jsonify({"message": "User not found"}), 404

@app.route('/users', methods=['POST'])
def add_user():
    """
    Add a new user to the user list.

    The user information is provided in the request body as JSON.
    
    Returns:
        Response: The ID of the newly added user and a status code of 201.
    """
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
    return f"{new_user['id']}", 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    """
    Update the information of an existing user.

    The updated user information is provided in the request body as JSON.
    
    Args:
        id (int): The ID of the user to update.
    
    Returns:
        Response: A JSON response containing the updated user data if found,
                  or a 404 error message if not found.
    """
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
    """
    Delete a user by their ID.
    
    Args:
        id (int): The ID of the user to delete.
    
    Returns:
        Response: A JSON response with a success message if the user is deleted,
                  or a 404 error message if the user is not found.
    """
    data = load_data()
    for user in data:
        if user['id'] == id:
            data.remove(user)
            save_data(data)
            return jsonify({"message": "User deleted"}), 200

    return jsonify({"message": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
