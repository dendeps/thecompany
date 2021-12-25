from thecompany_app import app
from . import employee_view
from . import department_view


def init_views():
    """
    Register views
    :return: None
    """

    from . import department_view
    app.register_blueprint(department_view.bp)

    from . import employee_view
    app.register_blueprint(employee_view.bp)