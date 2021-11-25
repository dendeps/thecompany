from thecompany_app import db


class Employee(db.Model):
    __tablename__ = 'employee'

    # id of the employee in the table
    id = db.Column(db.Integer, primary_key=True)

    # Name of the Employee
    name = db.Column(db.String(), nullable=False)

    # Employees position
    position = db.Column(db.String(), nullable=False)

    # Employees date of Birth
    dob = db.Column(db.String(), nullable=False)

    # Salary
    salary = db.Column(db.Integer)

    #: department id of the department that employee works in
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def __init__(self, name, dob, salary=0, department=None):
        #: employee's name
        self.name = name

        #: employee's date of birth
        self.dob = dob

        #: employee's salary
        self.salary = salary

        #: department employee works in
        self.department = department

    def __repr__(self):
        return f'Employee({self.name}, {self.date_of_birth}, {self.salary})'
