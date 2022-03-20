from marshmallow import Schema, fields, validates_schema, ValidationError, post_load, validate
from thecompany_app.models.department import Department


def validate_department(dept_name):
    if dept_name is None or len(dept_name) < 3:
        raise ValidationError("Department name should be at least 3 letters")

class Department_schema(Schema):
    uuid = fields.Str()
    name = fields.Str(validate=validate_department)
    #name = fields.Str(validate=validate.Length(min=3))

    @post_load
    def create_department(self, data, **kwargs):
        return Department(data.get("name"))
