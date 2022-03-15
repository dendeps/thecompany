"""
REST API module for Departments
"""
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from thecompany_app.models.department import Department
from thecompany_app.schemas.schema_department import Department_schema


class Department_api_base(Resource):
    """
    Department API base class
    """
    # Marshmallow Department schema
    schema = Department_schema()


class Department_list_api(Department_api_base):
    def get(self):
        departments = Department.get_all()
        return self.schema.dump(departments, many=True), 200


class Department_api(Department_api_base):

    NOT_FOUND_MSG = "No department found with provided UUID"
    SUCCESS_MSG = "Operation successful"
    ALREADY_EXISTS_MSG = "Department with this name already exists"
    UUID_REQUIRED = "UUID is required"

    def get(self, uuid:str):
        try:
            department = Department.get_by_uuid(uuid)
        except ValueError:
            return self.NOT_FOUND_MSG, 404
        return self.schema.dump(department), 200

    def post(self):
        try:
            department = self.schema.load(request.json)
        except ValidationError as error:
            return error.messages, 400
        else:
            department.save_to_db()
            return self.schema.dump(department), 201

    def put(self, uuid=None):
        if uuid is None:
            return self.UUID_REQUIRED, 400
        error = self.schema.validate(request.json)
        if error:
            return error, 400
        try:
            department = Department.get_by_uuid(uuid)
        except ValueError:
            return self.NOT_FOUND_MSG, 404
        else:
            department.name = request.json.get("name")
            department.save_to_db()
            return self.schema.dump(department), 200

    def delete(self, uuid=None):
        if uuid is None:
            return self.UUID_REQUIRED, 400
        try:
            department = Department.get_by_uuid(uuid)
        except ValueError:
            return self.NOT_FOUND_MSG, 404
        department.delete_from_db()
        return self.SUCCESS_MSG, 204

