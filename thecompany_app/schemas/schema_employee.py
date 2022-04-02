"""
This module contains the de-serialization schemas for Employee data model
"""
from marshmallow import Schema, ValidationError, fields, post_load, validate

from thecompany_app.models.department import Department
from thecompany_app.models.employee import Employee
from thecompany_app.schemas.schema_department import DepartmentSchema


class DepartmentNested(fields.Nested):
    """
    Defines Nested relations between Department - Employee
    """
    def __init__(self):
        super().__init__(
            'Department_schema', exclude=('employees',), required=True
        )

    def _deserialize(self, value, attr, data, partial=None, **kwargs):
        """
        Defines actions to do before the Deserialization
        """
        try:
            dept_uuid = data['department']['uuid']
            return Department.get_by_uuid(dept_uuid)
        except KeyError as error:
            raise ValidationError(
                'Invalid or missing Department uuid'
            ) from error


class EmployeeSchema(Schema):
    """
    Defines schema for Employee
    """
    name = fields.Str(validate=validate.Length(min=5))
    position = fields.Str(validate=validate.Length(min=3))
    salary = fields.Int(required=True)
    dob = fields.Str(validate=validate.Length(min=8))
    department = fields.Pluck(DepartmentSchema, 'name')
    uuid = fields.Str()

    @post_load
    def create_employee(self, data, **kwargs):
        """
        Defines actions to do for the Deserialization
        """
        dept = data.get("department")
        if Department.find_by_name(dept.name):
            dept = Department.find_by_name(dept.name)
            return Employee(data.get("name"),
                            data.get("position"),
                            data.get("dob"),
                            data.get("salary"),
                            dept.id
                            )
        raise ValidationError("Department doesn't exist")
