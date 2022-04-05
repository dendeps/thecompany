"""
Populates database with departments and employees.
"""
from thecompany_app import db
from .department import Department
from .employee import Employee


class Populate:
    """
    Initialises and populates database with departments and employees.
    """

    # pylint: disable=too-few-public-methods
    @staticmethod
    def populate():
        """
        Creates tables and populates database with departments and employees.
        :return: None
        """
        db.drop_all()
        db.create_all()
        department_1 = Department('Management')
        department_2 = Department('Development')
        department_3 = Department('Finance')
        employee_1 = Employee("Steve J", "Manager", "01-01-1990", 2000, 1)
        employee_2 = Employee("Bill Gates", "Java Dev", "02-02-1992", 3000, 2)
        employee_3 = Employee("Boom Finh", "Finman", "04-04-1994", 4000, 3)

        department_1.employees = [employee_1]
        department_2.employees = [employee_2]
        department_3.employees = [employee_3]
        db.session.add(department_1)
        db.session.add(department_2)
        db.session.add(department_3)

        db.session.add(employee_1)
        db.session.add(employee_2)
        db.session.add(employee_3)

        db.session.commit()
        db.session.close()