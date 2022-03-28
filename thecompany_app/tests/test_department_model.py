from thecompany_app.models.department import Department
from thecompany_app.models.employee import Employee
from thecompany_app.tests.conftest import Conftest


class TestDepartmentModel(Conftest):
    """
    Department model test case
    """

    def test_new_dept(self):
        """
        Tests Department model,
        :return: None
        """
        deptName = "TestDepartmentName"
        dept = Department(deptName)
        self.assertEqual(repr(dept), "Department: "+deptName)

    def test_check_if_exists(self):
        """
        Tests checking if dept already exists
        """
        name = "TestDepartmentName"
        dept = Department(name)
        self.assertFalse(Department.check_if_exists(name))
        dept.save_to_db()
        self.assertTrue(Department.check_if_exists(name))

    def test_find_by_name(self):
        """
        Tests checking if dept already exists
        """
        dept = Department("FindMe")
        dept.save_to_db()
        self.assertEqual(dept, Department.find_by_name("FindMe"))

    def test_delete_from_db(self):
        dept = Department("DeleteMe")
        dept.save_to_db()
        dept.delete_from_db()
        self.assertIsNone(Department.find_by_name("DeleteMe"))

    def test_get_all(self):
        depts = Department.get_all()
        self.assertEqual(3, len(depts))

    def test_get_dept_by_uuid(self):
        dept = Department("ItsMe")
        dept.save_to_db()
        self.assertEqual(dept, Department.get_by_uuid(dept.uuid))
        with self.assertRaises(ValueError) as e:
            Department.get_by_uuid("invalid_uuid")
        self.assertEqual('Invalid department uuid', e.exception.args[0])

    def test_delete_dept_by_uuid(self):
        dept = Department("DeleteMe")
        dept.save_to_db()
        Department.delete_by_uuid(dept.uuid)
        self.assertIsNone(Department.find_by_name("DeleteMe"))

    def test_get_avg_salary(self):
        Department('GosDep').save_to_db()
        department = Department.find_by_name("GosDep")
        employee_1 = Employee("Steve J", "Manager", "01-01-1990", 8000, department.id)
        employee_2 = Employee("Bill Gates", "Java Dev", "02-02-1992", 3000, department.id)
        employee_1.save_to_db()
        employee_2.save_to_db()
        department.employees = [employee_1, employee_2]
        self.assertEqual(department.get_average_salary(), (employee_1.salary + employee_2.salary)/2)








