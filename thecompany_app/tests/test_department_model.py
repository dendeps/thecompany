from thecompany_app.models.department import Department
from thecompany_app.tests.basetest import BaseTestCase


class TestDepartmentModel(BaseTestCase):
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
        dept = Department("TestDepartmentName")
        self.assertFalse(dept.check_if_exists())
        dept.save_to_db()
        self.assertTrue(dept.check_if_exists())

    def test_find_by_name(self):
        dept = Department("FindMe")
        dept.save_to_db()
        self.assertEqual(dept, Department.find_by_name("FindMe"))

    def test_delete_from_db(self):
        dept = Department("DeleteMe")
        dept.save_to_db()
        dept.delete_from_db()
        self.assertIsNone(Department.find_by_name("DeleteMe"))

    def test_get_all(self):
        Department("DeptOne").save_to_db()
        Department("DeptTwo").save_to_db()
        Department("DeptThree").save_to_db()
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






