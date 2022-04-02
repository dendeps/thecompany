"""
This package contains modules to provide the REST API endpoints for the application:

Modules:
- `department.py`: defines REST API for departments
- `employee.py`: defines REST API for employees
"""
from . import api_employee
from . import api_department
from thecompany_app import api
from .api_department import DepartmentApi, DepartmentListApi
from .api_employee import EmployeeListApi, EmployeeApi


def init_api():
    pass
    api.add_resource(DepartmentListApi, '/api/departments')
    api.add_resource(DepartmentApi, '/api/department/<uuid>', '/api/department')

    api.add_resource(EmployeeListApi, '/api/employees')
    api.add_resource(EmployeeApi, '/api/employee/<uuid>', '/api/employee')
