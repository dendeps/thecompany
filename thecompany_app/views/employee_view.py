import requests as requests
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, make_response
)
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from thecompany_app.models.department import Department
from thecompany_app.models.employee import Employee
from thecompany_app.schemas.schema_employee import Employee_schema

HOST = 'http://127.0.0.1:5000/'

class EmployeeForm(FlaskForm):
    name = StringField('Full name', validators=[InputRequired(), Length(5, 128), ])
    department = SelectField(choices=[''])
    position = StringField('Position', validators=[InputRequired(), Length(3, 128), ])
    dob = StringField('Date Of Birth', validators=[InputRequired(), Length(8, 128), ])
    salary = DecimalField('Salary', validators=[InputRequired()])
    submit = SubmitField('Submit')

    @classmethod
    def get_departments_list(cls):
        """
        Gets the list of departments from database for the form

        """
        departments = Department.get_all()
        cls.department = SelectField(choices=[department.name for department in departments])


bp = Blueprint('employees', __name__)
schema = Employee_schema()


@bp.route('/employees')
def index():
    return render_template('employees/index.html', employees=Employee.get_all())
    #url = f'{HOST}api/employees'
    #employees = requests.get(url).json()
    #return render_template('employees/index.html', employees=employees)


@bp.route('/employee', methods=('GET', 'POST'))
def create():
    EmployeeForm.get_departments_list()
    form = EmployeeForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            dep_name_selected = form.department.data
            dep = Department.query.filter_by(name=dep_name_selected).first()
            if not dep:
                return make_response({'message': 'Incorrect department'}, 400)
            data = {
                'name': form.name.data,
                'position': form.position.data,
                'department': dep.name,
                'dob': form.dob.data,
                'salary': form.salary.data
            }
            #url = f'{HOST}api/employee'
            #requests.post(url, data=data).json()
            try:
                employee = schema.load(data)
            except ValidationError as err:
                flash(err)
                return redirect(url_for('employees.index')), 400
            else:
                employee.save_to_db()
            return redirect(url_for('employees.index'))
    return render_template('employees/create.html', form=form)


@bp.route('/employees/update/<uuid>', methods=('GET', 'POST'))
def update(uuid):
    employee = Employee.get_by_uuid(uuid)
    EmployeeForm.get_departments_list()
    form = EmployeeForm(obj=employee)

    if form.validate_on_submit():
        dep_name_selected = form.department.data
        dep = Department.query.filter_by(name=dep_name_selected).first()
        data = {
            'name': form.name.data,
            'position': form.position.data,
            'department': form.department.data,
            'dob': form.dob.data,
            'salary': form.salary.data
        }

        #url = f'{HOST}api/employee'
        #requests.post(url, data=data).json()
        employee.name = form.name.data
        employee.position = form.position.data
        employee.department_id = dep.id
        employee.dob = form.dob.data
        employee.salary = form.salary.data
        employee.save_to_db()
        return redirect(url_for('employees.index'))
    elif form.errors:
        flash(form.errors)

    form.name.data = employee.name
    form.position.data = employee.position
    # form.department.data = employee.department
    form.dob.data = employee.dob
    form.salary.data = employee.salary
    return render_template('employees/update.html', employee=employee, form=form)

@bp.route('/employees/delete/<uuid>', methods=('POST',))
def delete(uuid):
    employee = Employee.get_by_uuid(uuid)
    employee.delete_from_db()
    return redirect(url_for('employees.index'))
