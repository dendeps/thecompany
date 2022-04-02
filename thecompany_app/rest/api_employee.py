"""
REST API module for Employees
"""
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from thecompany_app.models.employee import Employee
from thecompany_app.schemas.schema_employee import EmployeeSchema


class EmployeeApiBase(Resource):
    """
    Employee API base class
    """
    # Marshmallow Employee schema
    schema = EmployeeSchema()


class EmployeeListApi(EmployeeApiBase):
    """
    Class for EmployeesListApi Resource available at '/api/employees' url
    """
    def get(self):
        """
        Called when GET request is sent
        :returns: list of all Employees
        """
        employees = Employee.get_all()
        return self.schema.dump(employees, many=True), 200


class EmployeeApi(EmployeeApiBase):
    """
    Class for EmployeeApi Resource available at '/api/employee' url
    """
    NOT_FOUND_MSG = "No employee found with provided UUID"
    SUCCESS_MSG = "Operation successful"
    UUID_REQUIRED = "UUID is required"

    def get(self, uuid=None):
        """
        Called when GET request is sent
        :returns: Employee with given UUID
        """
        if uuid is None:
            return self.UUID_REQUIRED, 400
        try:
            employee = Employee.get_by_uuid(uuid)
        except ValueError:
            return self.NOT_FOUND_MSG, 404
        return self.schema.dump(employee), 200

    def post(self):
        """
        Called when POST request is sent
        Creates a new Employee with data provided
        :returns: created Employee
        """
        try:
            employee = self.schema.load(request.json)
        except ValidationError as error:
            return error.messages, 400
        #except ValueError as error:
        #    return error.message, 400
        else:
            employee.save_to_db()
        return self.schema.dump(employee), 201

    def put(self, uuid=None):
        """
        Called when PUT request is sent
        Updates an Employee with data provided with the given UUID
        :returns: updated Employee
        """
        if uuid is None:
            return self.UUID_REQUIRED, 400
        try:
            employee = Employee.get_by_uuid(uuid)
        except ValueError:
            return self.NOT_FOUND_MSG, 404
        try:
            upd_employee = self.schema.load(request.json)
        except ValidationError as error:
            return error.messages, 400
        else:
            employee.name = upd_employee.name
            employee.position = upd_employee.position
            employee.salary = upd_employee.salary
            employee.dob = upd_employee.dob
            employee.department_id = upd_employee.department_id
            employee.save_to_db()
            return self.schema.dump(employee), 200

    def delete(self, uuid=None):
        """
        Called when DEL request is sent
        Deletes an Employee with given UUID
        """
        if uuid is None:
            return self.UUID_REQUIRED, 400
        try:
            employee = Employee.get_by_uuid(uuid)
        except ValueError:
            return self.NOT_FOUND_MSG, 404
        employee.delete_from_db()
        return self.SUCCESS_MSG, 204
