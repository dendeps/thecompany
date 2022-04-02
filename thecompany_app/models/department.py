import uuid
from thecompany_app import db


class Department(db.Model):
    """
    Data model and methods which represents Department
    """
    __tablename__ = 'department'

    # id of the department in the table
    id = db.Column(db.Integer, primary_key=True)

    #: UUID of the department
    uuid = db.Column(db.String(36), unique=True)

    # Name of the department
    name = db.Column(db.String())

    # Employees belong in this department
    employees = db.relationship(
        'Employee',
        cascade="all,delete",
        backref=db.backref('department',
                           lazy=True)
    )

    def __init__(self, name, employees=None):
        self.name = name
        self.uuid = str(uuid.uuid4())

        if employees is None:
            employees = []
            #: Employees working in the department
        self.employees = employees

    def __repr__(self):
        return f"Department: {self.name}"

    @classmethod
    def check_if_exists(cls, name: str):
        """
        Checks if department with given name already exists
        """
        department = db.session.query(Department).filter_by(name=name).first()
        return False if department is None else True

    @classmethod
    def find_by_name(cls, name: str):
        """
        Returns department with given name or None
        """
        department = db.session.query(Department).filter_by(name=name).first()
        return department

    def save_to_db(self):
        """
        Saves updates of the current department to the DB
        """
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        """
        Deletes the current department from the DB
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        """
        Returns a list of all departments from the DB
        """
        departments = db.session.query(Department).all()
        for dept in departments:
            salary = dept.get_average_salary()
            dept.average_salary = float(salary) if salary else 0
            dept.number_of_employees = dept.get_number_of_employees()
        return departments

    @classmethod
    def get_by_uuid(cls, uuid):
        """
        Returns department with given uuid or raises ValueError
        """
        department = db.session.query(Department).filter_by(uuid=uuid).first()
        if department is None:
            raise ValueError('Invalid department uuid')
        return department

    @classmethod
    def delete_by_uuid(cls, uuid):
        """
        Deletes department with given uuid or raises ValueError
        """
        department = cls.get_by_uuid(uuid)
        if department is None:
            raise ValueError('Invalid department uuid')
        db.session.delete(department)
        db.session.commit()

    def get_average_salary(self):
        """
        Calculates and returns the average salary for the current department
        """
        avg_salary = 0
        if self.employees:
            for empl in self.employees:
                avg_salary += empl.salary
            avg_salary /= len(self.employees)
        return round(avg_salary, 2)

    def get_number_of_employees(self):
        """
        Returns the number of employees in the current department
        """
        num_employees = len(self.employees)
        return num_employees

    @staticmethod
    def to_dict(uuid):
        """
        Returns the Dict representation of the department by uuid or raises ValueError
        """
        dept = Department.get_by_uuid(uuid)
        if dept is None:
            raise ValueError('Invalid department uuid')
        return {
            'uuid': dept.id,
            'name': dept.name,
            'employees_count': len(dept.employees),
            'average_salary': dept.get_average_salary(dept),
            'employees': [dept.to_dict(employee.id)
                          for employee in dept.employees]
        }
