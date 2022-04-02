"""
Package contains all Blueprints
"""
from thecompany_app import app
from . import employee_view
from . import department_view


def init_views():
    """
    Initializes Blueprints and imports all submodules from views.
    :return: None
    """

    from . import department_view
    app.register_blueprint(department_view.bp)

    from . import employee_view
    app.register_blueprint(employee_view.bp)