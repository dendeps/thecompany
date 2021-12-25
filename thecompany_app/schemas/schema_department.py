from marshmallow import Schema, fields, validates_schema, ValidationError, post_load, validate
from thecompany_app.models.department import Department


class Department_schema(Schema):
    name = fields.Str(validate=validate.Length(min=3))
    uuid = fields.Str()

    @post_load
    def create_department(self, data, **kwargs):
        return Department(data.get("name"))
