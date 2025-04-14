from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flasgger import Swagger,swag_from
#creating app
app = Flask(__name__)
# connect postgre with flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Dark%400077@localhost:5432/practiceapi'
# initialize database and marshmallow
db = SQLAlchemy(app)
ma=Marshmallow(app)
Swagger(app)
#initialize table name and adding attributes
class user(db.Model):
    __tablename__ = 'user' #initialize the name of the table
    emp_id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    emp_name=db.Column(db.String(200),nullable=False)
    emp_salary=db.Column(db.Integer)

#creating schema with marshmallow
class userSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = user
        load_instance = True

    emp_id=ma.auto_field()
    emp_name=ma.auto_field()
    emp_salary=ma.auto_field()
user_schema=userSchema()
user_schemas=userSchema(many=True)
#creating the table
with app.app_context():
    db.create_all()

#adding post method
@app.route('/user', methods=['POST'])
#using swagger to create the api documentation
@swag_from({
    'tags':['Employee'],
    'parameters': [
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
        201: {
            'description':'Employee added successfully',
            'content':{
                'application/json':{
                    'example':{'message':'Employee added successfully'}
                }
            }
        },
        400:{
            'description':'Invalid input data'
        }
    }
})
def create_employee():
    
    data = request.get_json() #get the details of employees in json format
    user=user_schema.load(data) #access the data from database
    db.session.add(user) #adding the employee details in the table
    db.session.commit() #save the updated database and table
    return jsonify({"message": "Employee added successfully"}), 201

#adding get method
@app.route('/user',methods=['GET'])
#using swagger to create the api documentation
@swag_from({
    'tags':['Employee'],
    'parameters':[],
    'responses':{
        200:{
            'description':'List of all employees ',
            'schema':{
                'type':'array',
                'items':{
                    'type':'object',
                    'properties':{
                        'emp_id':{'type':'integer'},
                        'emp_name':{'type':'string'},
                        'emp_salary':{'type':'integer'}
                    }
                }
            }
        },
        404:{
            'description':'Employee/Employees not found'
        }
    }
})
def get_employee():
    emp=user.query.all() #get the details of all the employees
    return user_schemas.dump(emp) #provide the data to user

# adding get method (search or get the details of employee by emp_id)
@app.route('/user/<int:emp_id>',methods=['GET'])
#using swagger to create the api documentation
@swag_from({
    'tags':['Employee'],
    'parameters':[
        {
            'name':'emp_id',
            'in':'path',
            'type':'integer',
            'required':True,
            'description':'Id of the employee'
        }
    ],
    'responses':{
        200: {'description':'Employee data',
            'schema':{
                'type':'array',
                'items':{
                    'type':'object',
                    'properties':{
                        'emp_id':{'type':'integer'},
                        'emp_name':{'type':'string'},
                        'emp_salary':{'type':'integer'}
                    }
                }
            }
        },
        404:{
            'description':'Employee not found'
        }
    }
})
def get_users(emp_id):
    emp=user.query.get_or_404(emp_id) #get the employee details by emp_id
    return user_schema.dump(emp) #provide the data to user


# adding put method for whole updation
@app.route('/user/<int:emp_id>',methods=['PUT'])
#using swagger to create the api documentation
@swag_from({
    'tags':['Employee'],
    'parameters': [
        {
            'name': 'emp_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Employee ID'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'emp_id': {'type': 'integer', 'example': 1},
                    'emp_name': {'type': 'string', 'example': 'John Doe'},
                    'emp_salary': {'type': 'integer', 'example': 50000}
                },
                'required': ['emp_id', 'emp_name', 'emp_salary']
            }
        }
    ],
    'responses':{
        200: {
            'description':'Employee updated successfully',
            'schema':{
                'type':'object',
                'properties':{
                    'message':{'type':'string'}
                }
            }
        },
        400:{
            'description':'Invalid input data'
        }
    }
})
def update_employee(emp_id):
    emp=user.query.get_or_404(emp_id) #get the details of employee with the help of emp_id
    data=request.get_json() #get the details from the user in json format
    updated_emp=user_schema.load(data) #adding the provided data
    emp.emp_id=updated_emp.emp_id #overwrite the data of emp_id
    emp.emp_name=updated_emp.emp_name #overwrite the data of emp_name
    emp.emp_salary=updated_emp.emp_salary #overwrite the data of emp_salary
    db.session.commit() #save the updated database and table
    return jsonify({"message": "Employee updated successfully"}), 200

# adding patch method for patially updation
@app.route('/user/<int:emp_id>',methods=['PATCH'])
#using swagger to create the api documentation
@swag_from({
    'tags':['Employee'],
    'parameters':[
        {
        'name':'emp_id',
        'in':'path',
        'type':'integer',
        'required':True
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
                        'example': 'Alice Updated'
                    },
                    'emp_salary': {
                        'type': 'integer',
                        'example': 55000
                    }
                }
            }
        }
    ],
    'responses':{
        200: {
            'description':'Employee updated successfully',
            'schema':{
                'type':'object',
                'properties':{
                    'message':{'type':'string'}
                }
            }
        },
        400:{
            'description':'Invalid input data'
        }
    }
})
def updatep_employee(emp_id):
    emp=user.query.get_or_404(emp_id) #get the details of employee with the help of emp_id
    data=request.get_json() #get the details from the user in json format
    user_schema.load(data, instance=emp, partial=True) #adding the data in the table
    db.session.commit() #save the updated database and table
    return jsonify({"message": "Employee updated successfully"}), 200

# adding delete method
@app.route('/user/<int:emp_id>',methods=['DELETE'])
#using swagger to create the api documentation
@swag_from({
    'tags':['Employee'],
    'parameters':[{
        'name':'emp_id',
        'in':'path',
        'type':'integer',
        'required':True
    }],
    'responses':{
        200:{
            'description':'Employee added successfully',
            'schema':{
                'type':'object',
                'properties':{
                    'message':{'type':'string'}
                }
            }
        },
        404:{
            'description':'Employee not found'
        }
    }
})
def delete_employee(emp_id):
    emp=user.query.get_or_404(emp_id) #get the details of employee with the help of emp_id
    db.session.delete(emp) #delete the desired employee details
    db.session.commit() #save the updated database and table
    return jsonify({"message": "Employee deleted successfully"}), 200
    

# starts the flask development server along with debug mode
if __name__ == '__main__':
    app.run(debug=True)
