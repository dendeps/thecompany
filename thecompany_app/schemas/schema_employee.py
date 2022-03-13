from marshmallow import Schema, validates_schema, ValidationError, fields, post_load, validate, pre_load

from thecompany_app.models.department import Department
from thecompany_app.models.employee import Employee
from thecompany_app.schemas.schema_department import Department_schema


class DepartmentNested(fields.Nested):
    def __init__(self):
        super().__init__(
            'Department_schema', exclude=('employees',), required=True
        )

    def _deserialize(self, value, attr, data, partial=None, **kwargs):
        try:
            dept_uuid = data['department']['uuid']
            return Department.get_by_uuid(dept_uuid)
        except KeyError as error:
            raise ValidationError(
                'Invalid or missing Department uuid'
            ) from error


class Employee_schema(Schema):
    name = fields.Str(validate=validate.Length(min=5))
    position = fields.Str(validate=validate.Length(min=3))
    salary = fields.Int(required=True)
    dob = fields.Str(validate=validate.Length(min=8))
    department = fields.Pluck(Department_schema, 'name')
    #department = fields.Nested(Department_schema(only=("name",)))
    uuid = fields.Str()

    class Meta(Schema.Meta):
        model = Employee
        #dump_only = 'department'


    def get_dept_id(self, data, **kwargs):
        dept = data.get("department")
        if Department.find_by_name(dept.name):
            dept = Department.find_by_name(dept.name)
        data["department"] = dept.id
        return data

    @post_load
    def create_employee(self, data, **kwargs):
        dept = data.get("department")
        if Department.find_by_name(dept.name):
            dept = Department.find_by_name(dept.name)
            return Employee(data.get("name"),
                            data.get("position"),
                            data.get("dob"),
                            data.get("salary"),
                            dept.id
                            )
        else:
            raise ValidationError("Department doesn't exist")