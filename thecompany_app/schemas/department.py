from marshmallow import Schema, validates_schema, ValidationError, fields
from thecompany_app.models.department import Department
from thecompany_app.service import dbservice


class Department_schema(Schema):
    name = fields.Str()
