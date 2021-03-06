import uuid
from thecompany_app import db


class Employee(db.Model):
    """
    Data model and methods which represents Employee
    """
    __tablename__ = 'employee'

    # id of the employee in the table
    id = db.Column(db.Integer, primary_key=True)

    #: UUID of the department
    uuid = db.Column(db.String(36), unique=True)

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

    def __init__(self, name, position, dob, salary=0, department_id=None):
        #: employee's name
        self.name = name

        #: employee's position
        self.position = position

        #: employee's date of birth
        self.dob = dob

        #: employee's salary
        self.salary = salary

        #: department where employee works in
        self.department_id = department_id

        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'Employee: {self.name}, {self.dob}, {self.position}, {self.salary}'

    def save_to_db(self):
        """
        Saves updates of the current Employee to the DB
        """
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        """
        Deletes the current Employee from the DB
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        """
        Returns a list of all Employees from the DB
        """
        return db.session.query(Employee).all()

    @classmethod
    def get_by_uuid(cls, uuid):
        """
        Returns the Employee with given uuid or raises ValueError
        """
        employee = db.session.query(Employee).filter_by(uuid=uuid).first()
        if employee is None:
            raise ValueError('Invalid employee uuid')
        return employee

    @classmethod
    def delete_by_uuid(cls, uuid: str):
        """
        Deletes the Employee with given uuid or raises ValueError
        """
        employee = db.session.query(Employee).filter_by(uuid=uuid).first()
        if employee is None:
            raise ValueError('Invalid employee uuid')
        db.session.delete(employee)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name: str):
        """
        Returns the Employee with given name or None
        """
        employee = db.session.query(Employee).filter_by(name=name).first()
        return employee
