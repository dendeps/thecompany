import os
import unittest
from thecompany_app.models.department import Department

class TestDepartmentModel(unittest.TestCase):
    """
    Department model test case
    """

    def test_department(self):
        """
        Tests Department model,
        :return: None
        """
        deptName = "TestDepartmentName"
        dept = Department(deptName)
        self.assertEqual(repr(dept), "Department: "+deptName)

