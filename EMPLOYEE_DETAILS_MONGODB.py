from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import pymongo
from flasgger import Swagger, swag_from

#initialize the flask app and swagger
app = Flask(__name__)
load_dotenv('config.env')
database_name = os.getenv('database')
print(database_name)
#connect to the mongodb database
#load the environment variables from the config.env file
collection_name = os.getenv('collection')
print(collection_name)
client = pymongo.MongoClient(host='localhost', port=27017)
db = client[str(database_name)]
collection = db[str(collection_name)]
Swagger(app)


#single user entry
@app.route('/user', methods=['POST'])
@swag_from({ #importing the swagger documentation
    'tags':['Employee'],
    'parameters': [#name, in, required, type, description
        {
            'name': 'body', 
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['emp_name', 'emp_salary'],
                'properties': {
                    'emp_name': {
                        'type': 'string',
                        'description': 'Name of the employee',
                        'example': 'John Doe'
                    },
                    'emp_salary': {
                        'type': 'integer',
                        'description': 'Salary of the employee',
                        'example': 50000
                    }
                }
            }
        }
    ],
    'responses':{
        201:{
            "description":"user added successfully"
        }
    }
})
def create_user():#create a new user
    #get the data from the request
    data=request.get_json()
    if collection.find_one({'emp_id': data['emp_id']}):
        return jsonify({'message': 'emp_id already exists'}), 400 
    #add the data to the database
    collection.insert_one(data)
    return jsonify({'message':'user added successfully'}),200

#bulk user entry
@app.route('/user/bulk', methods=['POST'])
@swag_from({ #swagger documentation
    'tags':['Employee'],
    'parameters': [ #name, in, required, type, description
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'required': ['emp_name', 'emp_salary'],
                    'properties': {
                        'emp_name': {
                            'type': 'string',
                            'description': 'Name of the employee',
                            'example': 'John Doe'
                        },
                        'emp_salary': {
                            'type': 'integer',
                            'description': 'Salary of the employee',
                            'example': 50000
                        }
                    }
                }
            }
        }
    ],
    'responses':{
        201:{
            "description":"users added successfully"
        }
    }
})
def create_bulk_users():#create multiple users
    #get the data from the request
    data=request.get_json()
    for user in data:
        if collection.find_one({'emp_id': user['emp_id']}):
            return jsonify({'message': f"emp_id {user['emp_id']} already exists"}), 409
    #add the data to the database
    result = collection.insert_many(data)
    return jsonify({'message':'users added successfully'}),201    

#fetch the details of user
@app.route('/user/get',methods=['GET'])
@swag_from({ #swagger documentation
    'tags':['Employee'],
    'parameters':[],#name, in, required, type, description
    'responses':{
        200:{
            'description':'List of all employees',
            'schema':{
                'type':'array',
                'items':{
                    'type':'object',
                    'properties':{
                        'emp_name': {
                            'type': 'string',
                            'description': 'Name of the employee'
                        },
                        'emp_salary': {
                            'type': 'integer',
                            'description': 'Salary of the employee'
                        }
                    }
                }
            }
        }
    }
})
def get_user():#fetch all users
    #get the data from the database
    data=collection.find()
    result=[]
    for i in data:
        result.append({'emp_name':i['emp_name'],'emp_salary':i['emp_salary']})
    return jsonify(result),200

#fetch the details of user by id
@app.route('/user/get/<int:emp_id>',methods=['GET'])
@swag_from({#swagger documentation
    'tags':['Employee'],
    'parameters': [#name, in, required, type, description
        {
            'name': 'emp_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the employee'
        }
    ],
    'responses':{
        200:{
            'description':'Details of the employee',
            'schema':{
                'type':'object',
                'properties':{
                    'emp_name': {
                        'type': 'string',
                        'description': 'Name of the employee'
                    },
                    'emp_salary': {
                        'type': 'integer',
                        'description': 'Salary of the employee'
                    }
                }
            }
        },
        404:{
            'description':'user not found'
        }
    }
})
def get_user_by_id(emp_id):#fetch user by id
    #get the data from the database
    data=collection.find_one({'emp_id':emp_id})
    if data:
        return jsonify({'emp_id': data['emp_id'], 'emp_name': data['emp_name'], 'emp_salary': data['emp_salary']}), 200
    else:
        return jsonify({'message':'user not found'}),404
    

#update the details of user by id
@app.route('/user/update/<int:emp_id>',methods=['PUT'])
@swag_from({#swagger documentation
    'tags':['Employee'],
    'parameters': [#name, in, required, type, description
        {
            'name': 'emp_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the employee'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'emp_name': {
                        'type': 'string',
                        'description': 'Name of the employee'
                    },
                    'emp_salary': {
                        'type': 'integer',
                        'description': 'Salary of the employee'
                    }
                }
            }
        }
    ],
    'responses':{
        200:{
            "description":"user updated successfully"
        },
        404:{
            "description":"user not found"
        }
    }
})
def update_user(emp_id):#update user by id
    #get the data from the request
    data=request.get_json()
    result=collection.update_one({'emp_id':emp_id},{'$set':data})
    if result.modified_count>0:
        return jsonify({'message':'user updated successfully'}),200
    else:
        return jsonify({'message':'user not found'}),404
    

#partially update the details of user by id
@app.route('/user/patch/<int:emp_id>',methods=['PATCH'])
@swag_from({#swagger documentation
    'tags':['Employee'],
    'parameters': [#name, in, required, type, description
        {
            'name': 'emp_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the employee'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'emp_name': {
                        'type': 'string',
                        'description': 'Name of the employee'
                    },
                    'emp_salary': {
                        'type': 'integer',
                        'description': 'Salary of the employee'
                    }
                }
            }
        }
    ],
    'responses':{
        200:{
            "description":"user updated successfully"
        },
        404:{
            "description":"user not found"
        }
    }
})
def patch_user(emp_id):#update user by id
    #get the data from the request
    data=request.get_json()
    result=collection.update_one({'emp_id':emp_id},{'$set':data})
    if result.modified_count>0:
        return jsonify({'message':'user updated successfully'}),200
    else:
        return jsonify({'message':'user not found'}),404

#delete the details of user by id
@app.route('/user/delete/<int:emp_id>',methods=['DELETE'])
@swag_from({#swagger documentation
    'tags':['Employee'],
    'parameters': [#name, in, required, type, description
        {
            'name': 'emp_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the employee'
        }
    ],
    'responses':{
        200:{
            "description":"user deleted successfully"
        },
        404:{
            "description":"user not found"
        }
    }
})
def delete_user(emp_id):#delete user by id
    #get the data from the database
    result=collection.delete_one({'emp_id':emp_id})
    if result.deleted_count>0:
        return jsonify({'message':'user deleted successfully'}),200
    else:
        return jsonify({'message':'user not found'}),404

if __name__ == '__main__':
    app.run(debug=True)