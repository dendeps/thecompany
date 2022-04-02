import bdb

from thecompany_app.models.department import Department
from thecompany_app.models.employee import Employee
from thecompany_app.tests.conftest import Conftest
from marshmallow import ValidationError
from thecompany_app.schemas.schema_employee import EmployeeSchema


class TestEmployeeModel(Conftest):
    """
    Department model test case
    """

    def test_new_empl(self):
        """
        Tests Employee model,
        :return: None
        """
        empl = Employee("Tanya Mai", "Jobless", "01-02-2003", salary=10000, department_id=1)
        self.assertEqual(f'Employee: {empl.name}, {empl.dob}, {empl.position}, {empl.salary}', repr(empl))

    def test_save_to_db(self):
        """
        Tests saving employee to the database
        """
        empl = Employee("Tanya Mai", "Jobless", "01-02-2003", salary=10000, department_id=1)
        empl.save_to_db()
        self.assertEqual(empl, Employee.get_by_uuid(empl.uuid))

    def test_delete_from_db(self):
        empl = Employee("Delete Me", "Jobless", "01-02-2003", salary=10000, department_id=1)
        empl.save_to_db()
        empl.delete_from_db()
        with self.assertRaises(ValueError):
            Employee.get_by_uuid(empl.uuid)

    def test_delete_by_uuid(self):
        empl = Employee("Delete Me", "Jobless", "01-02-2003", salary=10000, department_id=1)
        empl.save_to_db()
        Employee.delete_by_uuid(empl.uuid)
        with self.assertRaises(ValueError):
            Employee.get_by_uuid(empl.uuid)

    def test_get_all(self):
        empls = Employee.get_all()
        self.assertEqual(3, len(empls))

    def test_get_by_uuid(self):
        empl = Employee("Delete Me", "Jobless", "01-02-2003", salary=10000, department_id=1)
        empl.save_to_db()
        self.assertEqual(empl, Employee.get_by_uuid(empl.uuid))
        with self.assertRaises(ValueError) as e:
            Employee.get_by_uuid("invalid_uuid")
        self.assertEqual('Invalid employee uuid', e.exception.args[0])






