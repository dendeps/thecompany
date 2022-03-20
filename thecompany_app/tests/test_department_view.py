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
        response1 = client.get('/departments')
        self.assertEqual(200, response1.status_code)
        response2 = client.post('/departments')
        self.assertEqual(405, response2.status_code)

        response1 = client.get('/')
        self.assertEqual(200, response1.status_code)
        response2 = client.post('/')
        self.assertEqual(405, response2.status_code)
