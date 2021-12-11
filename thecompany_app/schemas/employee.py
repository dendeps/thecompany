from marshmallow import Schema, validates_schema, ValidationError, fields
from thecompany_app.models.department import Department
from thecompany_app.service import dbservice


class Employee_schema(Schema):
    name = fields.Str()
    position = fields.Str()
    dob = fields.Str()
    salary = fields.Str()
    department = fields.Str()
