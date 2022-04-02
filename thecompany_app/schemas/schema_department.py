"""
This module contains the serialization-deserialization schemas for Department data model
"""
from marshmallow import Schema, fields, ValidationError, post_load
from thecompany_app.models.department import Department


def validate_department(dept_name):
    """
    Defines custom validation for Department
    """
    if dept_name is None or len(dept_name) < 3:
        raise ValidationError("Department name should be at least 3 letters")


class DepartmentSchema(Schema):
    """
    Defines schema for Department
    """
    uuid = fields.Str()
    name = fields.Str(validate=validate_department)
    #name = fields.Str(validate=validate.Length(min=3))

    @post_load
    def create_department(self, data, **kwargs):
        """
        Defines actions to do for the Deserialization
        """
        return Department(data.get("name"))
