from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from

app = Flask(__name__)

# Optional Swagger Config
app.config['SWAGGER'] = {
    'title': 'Employee API',
    'uiversion': 3
}

# Automatically initialize Swagger
swagger = Swagger(app)

@app.route('/user', methods=['POST'])
@swag_from({
    'tags': ['User'],
    'summary': 'Create a new user',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'salary': {'type': 'integer'}
                    },
                    'required': ['name', 'salary']
                }
            }
        }
    },
    'responses': {
        201: {
            'description': 'User created successfully'
        },
        400: {
            'description': 'Invalid input'
        }
    }
})
def create_user():
    data = request.get_json()
    return jsonify({"message": f"User {data['name']} created!"}), 201

if __name__ == '__main__':
    app.run(debug=True)

