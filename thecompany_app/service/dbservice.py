import uuid

from thecompany_app import db
from thecompany_app.models.department import Department
from thecompany_app.models.employee import Employee


class DBService:
    """
    Department service used to make database queries
    """

    @classmethod
    def update_uuid(cls):
        depts = db.session.query(Department).all()
        empls = db.session.query(Employee).all()
        for dept in depts:
            department = db.session.query(Department).filter_by(id=dept.id).first()
            department.uuid = str(uuid.uuid4())
            db.session.commit()

        for e in empls:
            empl = db.session.query(Department).filter_by(id=e.id).first()
            empl.uuid = str(uuid.uuid4())
            db.session.commit()
        return

    @classmethod
    def get_departments(cls):
        return db.session.query(Department).all()

    @classmethod
    def get_department(cls, uuid):
        department = db.session.query(Department).filter_by(uuid=uuid).first()
        if department is None:
            raise ValueError('Invalid department uuid')
        return department

    @classmethod
    def add_department(cls, name):
        department = Department(name=name)
        db.session.add(department)
        db.session.commit()
        return department

    @classmethod
    def delete_department(cls, uuid):
        department = cls.get_department(uuid)
        if department is None:
            raise ValueError('Invalid department uuid')
        db.session.delete(department)
        db.session.commit()

    @classmethod
    def update_department(cls, uuid, name: str):
        department = cls.get_department(uuid)
        if department is None:
            raise ValueError('Invalid department uuid')
        department.name = name
        db.session.commit()

    @classmethod
    def get_employees(cls):
        return db.session.query(Employee).all()

    @classmethod
    def get_employee(cls, uuid):
        employee = db.session.query(Employee).filter_by(uuid=uuid).first()
        if employee is None:
            raise ValueError('Invalid department uuid')
        return employee

    @classmethod
    def add_employee(cls, name, position, dob, salary, department):
        employee = Employee(name, position, dob, salary, department)
        db.session.add(employee)
        db.session.commit()
        return employee

    @classmethod
    def delete_employee(cls, uuid):
        employee = cls.get_employee(uuid)
        if employee is None:
            raise ValueError('Invalid employee uuid')
        db.session.delete(employee)
        db.session.commit()

    @classmethod
    def update_employee(cls, uuid, name, position, dob, salary, department):
        employee = cls.get_employee(uuid)
        if employee is None:
            raise ValueError('Invalid employee uuid')
        employee.name = name
        employee.position = position
        employee.dob = dob
        employee.salary = salary
        employee.department = department
        db.session.commit()

