from . import api_employee
from . import api_department
from thecompany_app import api
from .api_department import Department_api, Department_list_api
from .api_employee import Employee_list_api, Employee_api


def init_api():
    pass
    api.add_resource(Department_list_api, '/api/departments')
    api.add_resource(Department_api, '/api/department/<uuid>', '/api/department')

    api.add_resource(Employee_list_api, '/api/employees')
    api.add_resource(Employee_api, '/api/employee/<uuid>', '/api/employee')
