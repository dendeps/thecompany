from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import InputRequired, Length, ValidationError

from thecompany_app.service.dbservice import DBService


class EmployeeForm(FlaskForm):
    fullname = StringField('Full name', validators=[InputRequired(), Length(4, 128), ])
    department = StringField('Department', validators=[InputRequired(), Length(4, 128), ])
    position = StringField('Position', validators=[InputRequired(), Length(4, 128), ])
    dob = StringField('Date Of Birth', validators=[InputRequired(), Length(4, 128), ])
    salary = DecimalField('Salary', validators=[InputRequired()])


bp = Blueprint('employees', __name__)


@bp.route('/employees')
def index():
    return render_template('employees/index.html', employees=DBService.get_employees())


@bp.route('/employee', methods=('GET', 'POST'))
def create():
    form = EmployeeForm()
    if request.method == 'POST':
        error = None

        form.fullname = request.form['fullname']
        form.department = request.form['department']
        form.position = request.form['position']
        form.dob = request.form['dob']
        form.salary = request.form['salary']

        if form.validate_on_submit():
            name = request.form['fullname']
            department = request.form['department']
            position = request.form['position']
            dob = request.form['dob']
            salary = request.form['salary']
        else:
            error = form.errors
            for err in error:
                flash(err)

        if error is None:
            DBService.add_employee(name, position, dob, salary, department)
            return redirect(url_for('employees.index'))
        flash(error)

    return render_template('employees/create.html', form=form)


@bp.route('/employees/update/<uuid>', methods=('GET', 'POST'))
def update(uuid):
    employee = DBService.get_employee(uuid)
    form = EmployeeForm()
    if request.method == 'POST':
        error = None

        form.fullname = request.form['fullname']
        form.department = request.form['department']
        form.position = request.form['position']
        form.dob = request.form['dob']
        form.salary = request.form['salary']

        if form.validate_on_submit():
            name = request.form['fullname']
            department = request.form['department']
            position = request.form['position']
            dob = request.form['dob']
            salary = request.form['salary']
        else:
            error = form.errors
            for err in error:
                flash(err)

        if error is None:
            DBService.update_employee(uuid, name, position, dob, salary, department)
            return redirect(url_for('employees.index'))
        flash(error)
    return render_template('employees/update.html', employee=employee, form=form)


@bp.route('/employees/delete/<uuid>', methods=('POST',))
def delete(uuid):
    DBService.delete_employee(uuid)
    return redirect(url_for('employees.index'))
