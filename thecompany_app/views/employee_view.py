from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import InputRequired, Length, ValidationError
from thecompany_app.models.employee import Employee
from thecompany_app.schemas.schema_employee import Employee_schema


class EmployeeForm(FlaskForm):
    fullname = StringField('Full name', validators=[InputRequired(), Length(4, 128), ])
    department = StringField('Department', validators=[InputRequired(), Length(4, 128), ])
    position = StringField('Position', validators=[InputRequired(), Length(4, 128), ])
    dob = StringField('Date Of Birth', validators=[InputRequired(), Length(4, 128), ])
    salary = DecimalField('Salary', validators=[InputRequired()])


bp = Blueprint('employees', __name__)
schema = Employee_schema()


@bp.route('/employees')
def index():
    return render_template('employees/index.html', employees=Employee.get_all())


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

        try:
            employee = schema.load({'name': name,
                                    'department': department,
                                    'position': position,
                                    'dob': dob,
                                    'salary': salary
                                    })
        except ValidationError as err:
            error = err.messages
        if error is None:
            employee.save_to_db()
            return redirect(url_for('employees.index'))
        flash(error)
    return render_template('employees/create.html', form=form)


@bp.route('/employees/update/<uuid>', methods=('GET', 'POST'))
def update(uuid):
    employee = Employee.get_employee(uuid)
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
            employee.name = name
            employee.position = position
            employee.dob = dob
            employee.salary = salary
            employee.department = department
            employee.save_to_db()
            return redirect(url_for('employees.index'))
        flash(error)
    return render_template('employees/update.html', employee=employee, form=form)


@bp.route('/employees/delete/<uuid>', methods=('POST',))
def delete(uuid):
    employee = Employee.get_employee(uuid)
    employee.delete_from_db()
    return redirect(url_for('employees.index'))
