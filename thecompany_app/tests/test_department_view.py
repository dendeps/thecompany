import http
import json

from thecompany_app import app
from thecompany_app.models.department import Department
from thecompany_app.tests.conftest import Conftest


class TestDepartmentView(Conftest):
    """
    Department View page test cases
    """

    """
        This is the class for home_page view test case
        """

    def test_departments_page(self):
        """
        Testing /department page
        """
        client = app.test_client()
        resp = client.get('/departments')
        self.assertEqual(200, resp.status_code)
        resp = client.post('/departments')
        self.assertEqual(405, resp.status_code)

        resp = client.get('/')
        self.assertEqual(200, resp.status_code)

        resp = client.post('/')
        self.assertEqual(405, resp.status_code)

        resp = client.post('/department', data={'department': 'Webdepartment'}
                                )
        self.assertEqual(302, resp.status_code)
        self.assertTrue(Department.check_if_exists('Webdepartment'))

    def test_department_update_page(self):
        """
        Testing /departments/update/<uuid>/update page
        """
        client = app.test_client()
        uuid = Department.get_all()[0].uuid
        resp = client.post('/departments/update/'+uuid, data={'department': 'ShitDepartment'}
                                )
        assert resp.status_code == http.HTTPStatus.FOUND
        self.assertTrue(Department.check_if_exists('ShitDepartment'))

    def test_department_delete_page(self):
        """
        Testing /departments/delete/<:uuid> page
        """
        client = app.test_client()
        uuid = Department.get_all()[0].uuid
        resp = client.post('/departments/delete/' + uuid)
        assert resp.status_code == http.HTTPStatus.FOUND
        with self.assertRaises(ValueError):
            Department.get_by_uuid(uuid)