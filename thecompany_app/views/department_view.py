from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from thecompany_app.service.dbservice import DBService

bp = Blueprint('departments', __name__)


@bp.route('/departments', methods=('GET',))
def index():
    return render_template('departments/index.html', departments=DBService.get_departments())

@bp.route('/department', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        department = request.form['department']
        error = None

        if not department:
            error = 'Department is required.'

        if error is None:
            DBService.add_department(department)
            return redirect(url_for('departments.index'))
        flash(error)

    return render_template('departments/create.html')


@bp.route('/departments/update/<uuid>', methods=('GET', 'POST'))
def update(uuid):
    department = DBService.get_department(uuid)
    if request.method == 'POST':
        dept = request.form['department']
        error = None
        if not dept:
            error = 'Department is required.'
        if error is None:
            DBService.update_department(uuid, dept)
            return redirect(url_for('departments.index'))
        flash(error)
    return render_template('departments/update.html', department=department)

@bp.route('/departments/delete/<uuid>', methods=('POST',))
def delete(uuid):
    DBService.delete_department(uuid)
    return redirect(url_for('departments.index'))

