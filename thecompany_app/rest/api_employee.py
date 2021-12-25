"""
REST API module for Employees
"""
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from thecompany_app.models.employee import Employee
from thecompany_app.schemas.schema_employee import Employee_schema


class Employee_api_base(Resource):
    """
    Employee API base class
    """
    # Marshmallow Employee schema
    schema = Employee_schema()


class Employee_list_api(Employee_api_base):
    def get(self):
        employees = Employee.get_all()
        return self.schema.dump(employees, many=True), 200


class Employee_api(Employee_api_base):

    NOT_FOUND_MSG = "No employee found with provided UUID"
    SUCCESS_MSG = "Operation successful"

    def get(self, uuid:str):
        try:
            employee = Employee.get_employee(uuid)
        except ValueError:
            return self.NOT_FOUND_MSG, 404
        return self.schema.dump(employee), 200

    def post(self):
        try:
            employee = self.schema.load(request.json)
        except ValidationError as error:
            return error.messages, 400
        except ValueError as error:
            return error.message, 400
        else:
            employee.save_to_db()
        return self.schema.dump(employee), 201

    def put(self, uuid):
        error = self.schema.validate(request.json)
        if error:
            return error, 400
        try:
            employee = Employee.get_employee(uuid)
        except ValueError:
            return self.NOT_FOUND_MSG, 404
        else:
            employee.name = request.json.get("name")
            employee.position = request.json.get("position")
            employee.salary = request.json.get("salary")
            employee.dob = request.json.get("dob")
            employee.department = request.json.get("department")
            employee.save_to_db()
            return self.schema.dump(employee), 200

    def delete(self, uuid):
        try:
            employee = Employee.get_employee(uuid)
        except ValueError:
            return self.NOT_FOUND_MSG, 404
        employee.delete_from_db()
        return self.SUCCESS_MSG, 204