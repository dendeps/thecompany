from thecompany_app import app

from . import employee_view
from . import department_view


def init_views():
    """
    Register views
    :return: None
    """
    employee_view.EmployeeView.register(app)
    department_view.DepartmentView.register(app)