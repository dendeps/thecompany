from marshmallow import Schema, fields, validates_schema, ValidationError, post_load, validate
from thecompany_app.models.department import Department


def validate_department(dept_name):
    if len(dept_name) < 3:
        raise ValidationError("Department name should be at least 3 letters")
    elif Department.find_by_name(dept_name):
        raise ValidationError("Department already exists")


class Department_schema(Schema):
    uuid = fields.Str()
    name = fields.Str(validate=validate.Length(min=3))
    ###average_salary = fields.Int(dump_only=True)
    ###average_salary = fields.Int(dump_only=True)

    @post_load
    def create_department(self, data, **kwargs):
        return Department(data.get("name"))
