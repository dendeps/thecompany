from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, json
)
from marshmallow import ValidationError
from werkzeug.exceptions import abort

from thecompany_app.models.department import Department
from thecompany_app.schemas.schema_department import Department_schema

bp = Blueprint('departments', __name__)
schema = Department_schema()


@bp.route('/', methods=('GET',))
@bp.route('/departments', methods=('GET',))
def index():
    return render_template('departments/index.html', departments=Department.get_all())


@bp.route('/department', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['department']
        error = None
        if not name:
            error = 'Department is required.'
        try:
            department = schema.load({'name': name})
        except ValidationError as err:
            error = err.messages
        if error is None:
            department.save_to_db()
            return redirect(url_for('departments.index'))
        flash(error)

    return render_template('departments/create.html')


@bp.route('/departments/update/<uuid>', methods=('GET', 'POST'))
def update(uuid):
    department = Department.get_department(uuid)
    if request.method == 'POST':
        dept_name = request.form['department']
        error = None
        if not dept_name:
            error = 'Department is required.'
        if error is None:
            department.name = dept_name
            department.save_to_db()
            return redirect(url_for('departments.index'))
        flash(error)
    return render_template('departments/update.html', department=department)

@bp.route('/departments/delete/<uuid>', methods=('POST',))
def delete(uuid):
    error = None
    try:
        department = Department.get_department(uuid)
    except ValueError:
        error = "No department found with provided UUID"
    if error is None:
        department.delete_from_db()
        return redirect(url_for('departments.index'))
    flash(error)

