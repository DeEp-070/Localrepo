from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flasgger import Swagger,swag_from

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Dark%400077@localhost:5432/practiceapi'

db = SQLAlchemy(app)
ma=Marshmallow(app)
Swagger(app)

class user(db.Model):
    __tablename__ = 'user'
    emp_id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    emp_name=db.Column(db.String(200),nullable=False)
    emp_salary=db.Column(db.Integer)
class userSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = user
        load_instance = True

    emp_id=ma.auto_field()
    emp_name=ma.auto_field()
    emp_salary=ma.auto_field()
user_schema=userSchema()
user_schemas=userSchema(many=True)

with app.app_context():
    db.create_all()


@app.route('/user', methods=['POST'])
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
    
    data = request.get_json()
    user=user_schema.load(data)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Employee added successfully"}), 201


@app.route('/user',methods=['GET'])
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
    emp=user.query.all()
    return user_schemas.dump(emp)


@app.route('/user/<int:emp_id>',methods=['GET'])
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
    emp=user.query.get_or_404(emp_id)
    return user_schema.dump(emp)



@app.route('/user/<int:emp_id>',methods=['PUT'])
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
    emp=user.query.get_or_404(emp_id)
    data=request.get_json()
    updated_emp=user_schema.load(data)
    emp.emp_id=updated_emp.emp_id
    emp.emp_name=updated_emp.emp_name
    emp.emp_salary=updated_emp.emp_salary
    db.session.commit()
    return jsonify({"message": "Employee updated successfully"}), 200


@app.route('/user/<int:emp_id>',methods=['PATCH'])
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
    emp=user.query.get_or_404(emp_id)
    data=request.get_json()
    user_schema.load(data, instance=emp, partial=True)
    db.session.commit()
    return jsonify({"message": "Employee updated successfully"}), 200


@app.route('/user/<int:emp_id>',methods=['DELETE'])
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
    emp=user.query.get_or_404(emp_id)
    db.session.delete(emp)
    db.session.commit()
    return jsonify({"message": "Employee deleted successfully"}), 200
    


if __name__ == '__main__':
    app.run(debug=True)