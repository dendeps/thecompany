import http
import json

from thecompany_app import app
from thecompany_app.models.employee import Employee
from thecompany_app.tests.conftest import Conftest


class TestEmployeeAPI(Conftest):
    """
    Employee API test cases
    """

    def test_get_all(self):
        """
        Testing the get request to /api/employee.
        It should return the status code 200
        """
        client = app.test_client()
        response = client.get('/api/employees')

        assert response.status_code == http.HTTPStatus.OK
        self.assertEqual(3, len(response.json))

    def test_get_by_uuid(self):
        client = app.test_client()
        empl = Employee("Tanya Mai", "Jobless", "01-02-2003", salary=10000, department_id=1)
        empl.save_to_db()
        response = client.get('/api/employee/' + empl.uuid)
        assert response.status_code == http.HTTPStatus.OK
        self.assertEqual(response.json.get("uuid"), empl.uuid)

        response = client.get('/api/employee/wronguuid')
        self.assertEqual(response.status_code, 404)
        response = client.get('/api/employee')
        self.assertEqual(response.status_code, 400)

    def test_post(self):
        client = app.test_client()
        with client:
            response = client.post('/api/employee')
            self.assertEqual(response.status_code, 400)
            response = client.post('/api/employee', data=json.dumps(dict(name="Tanya",
                                                                         position="Jobless",
                                                                         dob="01-02-2003",
                                                                         salary=10000,
                                                                         department="Management")),
                                   content_type='application/json')
            empl = json.loads(response.data)
            self.assertEqual(empl.get("name"), "Tanya")
            response = client.post('/api/employee', data=json.dumps(dict(name='01')),
                                   content_type='application/json')
            self.assertTrue(str(json.loads(response.data)).find("Shorter than minimum length 3"))

    def test_put(self):
        client = app.test_client()
        with client:
            response = client.put('/api/employee')
            self.assertEqual(response.status_code, 400)

            response = client.put('/api/employee/wrongudid', data=json.dumps(dict(name='TestData')),
                                  content_type='application/json')
            self.assertEqual(response.status_code, 404)

            empl = Employee.get_all()[0]
            response = client.put('/api/employee/' + empl.uuid, data=json.dumps(dict(name="Tanya",
                                                                         position="Jobless",
                                                                         dob="01-02-2003",
                                                                         salary=10000,
                                                                         department="Management")),
                                   content_type='application/json')
            self.assertEqual(response.status_code, 200)
            response = client.put('/api/employee/' + empl.uuid, data=json.dumps(dict(name="Tanya",
                                                                                     position="Jobless",
                                                                                     dob="01-02-2003",
                                                                                     salary=10000,
                                                                                     department="no")),
                                  content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_delete(self):
        client = app.test_client()
        with client:
            response = client.delete('/api/employee')
            self.assertEqual(response.status_code, 400)

            response = client.delete('/api/employee/wrongudid')
            self.assertEqual(response.status_code, 404)

            empl = Employee.get_all()[0]
            response = client.delete('/api/employee/' + empl.uuid)
            self.assertEqual(204, response.status_code)
