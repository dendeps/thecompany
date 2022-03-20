from thecompany_app import db
import uuid


class Department(db.Model):
    __tablename__ = 'department'

    # id of the department in the table
    id = db.Column(db.Integer, primary_key=True)

    #: UUID of the department
    uuid = db.Column(db.String(36), unique=True)

    # Name of the department
    name = db.Column(db.String())

    # Employees in this department
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
        department = db.session.query(Department).filter_by(name=name).first()
        if department is None:
            return False
        else:
            return True

    @classmethod
    def find_by_name(self, name: str):
        department = db.session.query(Department).filter_by(name=name).first()
        return department

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        departments = db.session.query(Department).all()
        for dept in departments:
            salary = dept.get_average_salary()
            dept.average_salary = float(salary) if salary else 0
            dept.number_of_employees = dept.get_number_of_employees()
        return departments

    @classmethod
    def get_by_uuid(cls, uuid):
        department = db.session.query(Department).filter_by(uuid=uuid).first()
        if department is None:
            raise ValueError('Invalid department uuid')
        return department

    @classmethod
    def delete_by_uuid(cls, uuid):
        department = cls.get_by_uuid(uuid)
        if department is None:
            raise ValueError('Invalid department uuid')
        db.session.delete(department)
        db.session.commit()

    def get_average_salary(self):
        avg_salary = 0
        if self.employees:
            for empl in self.employees:
                avg_salary += empl.salary
            avg_salary /= len(self.employees)
        return round(avg_salary, 2)

    def get_number_of_employees(self):
        num_employees = len(self.employees)
        return num_employees

    @staticmethod
    def to_dict(uuid):
        dept = Department.get_by_uuid(uuid)
        return {
            'uuid': dept.id,
            'name': dept.name,
            'employees_count': len(dept.employees),
            'average_salary': dept.get_average_salary(dept),
            'employees': [dept.to_dict(employee.id)
                          for employee in dept.employees]
        }
