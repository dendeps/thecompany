import http
import json

from thecompany_app import app
from thecompany_app.models.department import Department
from thecompany_app.models.employee import Employee
from thecompany_app.tests.conftest import Conftest


class TestEmployeeView(Conftest):
    """
    Department View page test cases
    """

    """
        This is the class for home_page view test case
        """

    def test_employees_page(self):
        """
        Testing /employee page
        """
        client = app.test_client()
        resp = client.get('/employees')
        self.assertEqual(200, resp.status_code)

        resp = client.get('/')
        self.assertEqual(200, resp.status_code)

        resp = client.post('/')
        self.assertEqual(405, resp.status_code)


        #self.assertNotEqual(None, Employee.find_by_name('NewEmployeeName'))

    def test_employee_delete_page(self):
        """
        Testing /departments/delete/<:uuid> page
        """
        client = app.test_client()
        uuid = Employee.get_all()[0].uuid
        resp = client.post('/employees/delete/' + uuid)
        assert resp.status_code == http.HTTPStatus.FOUND
        with self.assertRaises(ValueError):
            Employee.get_by_uuid(uuid)