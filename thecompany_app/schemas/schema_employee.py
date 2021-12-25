from marshmallow import Schema, validates_schema, ValidationError, fields, post_load, validate
from thecompany_app.models.employee import Employee


class Employee_schema(Schema):
    name = fields.Str(validate=validate.Length(min=5))
    position = fields.Str(validate=validate.Length(min=3))
    salary = fields.Int(required=True)
    dob = fields.Str(validate=validate.Length(min=8))
    department = fields.Str(validate=validate.Length(min=3))
    uuid = fields.Str()

    @post_load
    def create_employee(self, data, **kwargs):
        return Employee(data.get("name"),
                        data.get("position"),
                        data.get("dob"),
                        data.get("salary"),
                        data.get("department")
                        )
