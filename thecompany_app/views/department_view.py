from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from thecompany_app.service.dbservice import DBService

bp = Blueprint('departments', __name__)


@bp.route('/departments')
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


@bp.route('/departments/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    department = DBService.get_department(id)
    if request.method == 'POST':
        dept = request.form['department']
        error = None
        if not dept:
            error = 'Department is required.'
        if error is None:
            DBService.update_department(id, dept)
            return redirect(url_for('departments.index'))
        flash(error)
    return render_template('departments/update.html', department=department)

@bp.route('/departments/delete/<int:id>', methods=('POST',))
def delete(id):
    DBService.delete_department(id)
    return redirect(url_for('departments.index'))

