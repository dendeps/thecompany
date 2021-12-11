from thecompany_app import db
from thecompany_app.models.department import Department
from thecompany_app.models.employee import Employee


class DBService:
    """
    Department service used to make database queries
    """

    @classmethod
    def get_departments(cls):
        return db.session.query(Department).all()

    @classmethod
    def get_department(cls, id: int):
        department = db.session.query(Department).filter_by(id=id).first()
        if department is None:
            raise ValueError('Invalid department id')
        return department

    @classmethod
    def add_department(cls, name):
        department = Department(name=name)
        db.session.add(department)
        db.session.commit()
        return department

    @classmethod
    def delete_department(cls, id: int):
        department = cls.get_department(id)
        if department is None:
            raise ValueError('Invalid department id')
        db.session.delete(department)
        db.session.commit()

    @classmethod
    def update_department(cls, id: int, name: str):
        department = cls.get_department(id)
        if department is None:
            raise ValueError('Invalid department id')
        department.name = name
        db.session.commit()

    @classmethod
    def get_employees(cls):
        return db.session.query(Employee).all()

    @classmethod
    def get_employee(cls, id: int):
        employee = db.session.query(Employee).filter_by(id=id).first()
        if employee is None:
            raise ValueError('Invalid department id')
        return employee

    @classmethod
    def add_employee(cls, name, position, dob, salary, department):
        employee = Employee(name, position, dob, salary, department)
        db.session.add(employee)
        db.session.commit()
        return employee

    @classmethod
    def delete_department(cls, id: int):
        department = cls.get_department(id)
        if department is None:
            raise ValueError('Invalid department id')
        db.session.delete(department)
        db.session.commit()

    @classmethod
    def update_department(cls, id: int, name: str):
        department = cls.get_department(id)
        if department is None:
            raise ValueError('Invalid department id')
        department.name = name
        db.session.commit()

