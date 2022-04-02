"""
Defines application web view for managing Departments.
"""
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from marshmallow import ValidationError

from thecompany_app.models.department import Department
from thecompany_app.schemas.schema_department import DepartmentSchema

bp = Blueprint('departments', __name__)
schema = DepartmentSchema()
HOST = 'http://127.0.0.1:5000/'


@bp.route('/', methods=('GET',))
@bp.route('/departments', methods=('GET',))
def index():
    """
    Renders Departments List page
    """
    return render_template('departments/index.html', departments=Department.get_all())


@bp.route('/department', methods=('GET', 'POST'))
def create():
    """
    Renders Create Department page
    """
    if request.method == 'POST':
        dept_name = request.form['department']
        error = None
        if Department.check_if_exists(dept_name):
            error = 'Department with this name already exists.'
        try:
            department = schema.load({'name': dept_name})
        except ValidationError as err:
            error = err.messages
        else:
            if error is None:
                department.save_to_db()
                return redirect(url_for('departments.index'))
        flash(error)
    return render_template('departments/create.html')


@bp.route('/departments/update/<uuid>', methods=('GET', 'POST'))
def update(uuid):
    """
    Renders Update Department page
    """
    department = Department.get_by_uuid(uuid)
    if request.method == 'POST':
        dept_name = request.form.get('department')
        error = schema.validate({'name': dept_name})
        if Department.check_if_exists(dept_name):
            error = 'Department with this name already exists.'
        if not dept_name:
            error = 'Department is required.'
        if not error:
            department.name = dept_name
            department.save_to_db()
            return redirect(url_for('departments.index'))
        flash(error)
    return render_template('departments/update.html', department=department)


@bp.route('/departments/delete/<uuid>', methods=('POST',))
def delete(uuid):
    """
    Renders Delete Department page
    """
    error = None
    try:
        department = Department.get_by_uuid(uuid)
    except ValueError:
        error = "No department found with provided UUID"
        flash(error)
    else:
        if error is None:
            department.delete_from_db()
            return redirect(url_for('departments.index'))
