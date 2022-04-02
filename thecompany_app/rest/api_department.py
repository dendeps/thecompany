"""
REST API module for Departments
"""
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from thecompany_app.models.department import Department
from thecompany_app.schemas.schema_department import DepartmentSchema


class DepartmentApiBase(Resource):
    """
    Department API base class
    """
    # Marshmallow Department schema
    schema = DepartmentSchema()


class DepartmentListApi(DepartmentApiBase):
    """
    Class for DepartmentListApi Resource available at '/api/departments' url
    """
    def get(self):
        """
        Called when GET request is sent
        :returns: list of all departments
        """
        departments = Department.get_all()
        return self.schema.dump(departments, many=True), 200


class DepartmentApi(DepartmentApiBase):
    """
    Class for DepartmentApi Resource available at '/api/department' url
    """
    NOT_FOUND_MSG = "No department found with provided UUID"
    SUCCESS_MSG = "Operation successful"
    ALREADY_EXISTS_MSG = "Department with this name already exists"
    UUID_REQUIRED = "UUID is required"

    def get(self, uuid: str):
        """
        Called when GET request is sent
        :returns: department with given UUID
        """
        try:
            department = Department.get_by_uuid(uuid)
        except ValueError:
            return self.NOT_FOUND_MSG, 404
        return self.schema.dump(department), 200

    def post(self):
        """
        Called when POST request is sent
        Creates a new department with given name
        :returns: created department
        """
        try:
            department = self.schema.load(request.json)
        except ValidationError as error:
            return error.messages, 400

        if Department.check_if_exists(department.name):
            return self.ALREADY_EXISTS_MSG, 400

        department.save_to_db()
        return self.schema.dump(department), 201

    def put(self, uuid=None):
        """
        Called when PUT request is sent
        Updates a department with given UUID
        :returns: updated department
        """
        if uuid is None:
            return self.UUID_REQUIRED, 400

        new_dept_name = request.json.get("name")
        error = self.schema.validate(request.json)
        if error:
            return error, 400
        if Department.check_if_exists(new_dept_name):
            return self.ALREADY_EXISTS_MSG, 400

        try:
            department = Department.get_by_uuid(uuid)
        except ValueError:
            return self.NOT_FOUND_MSG, 404

        department.name = new_dept_name
        department.save_to_db()
        return self.schema.dump(department), 200

    def delete(self, uuid=None):
        """
        Called when DEL request is sent
        Deletes a department with given UUID
        """
        if uuid is None:
            return self.UUID_REQUIRED, 400
        try:
            department = Department.get_by_uuid(uuid)
        except ValueError:
            return self.NOT_FOUND_MSG, 404
        department.delete_from_db()
        return self.SUCCESS_MSG, 204
