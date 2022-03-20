import http
import json

from thecompany_app import app
from thecompany_app.models.department import Department
from thecompany_app.tests.conftest import Conftest


class TestDepartmentAPI(Conftest):
    """
    Department API test cases
    """

    def test_get_all(self):
        """
        Testing the get request to /api/departments.
        It should return the status code 200
        """
        client = app.test_client()
        response = client.get('/api/departments')

        assert response.status_code == http.HTTPStatus.OK
        self.assertEqual(3, len(response.json))

    def test_get_by_uuid(self):
        client = app.test_client()
        dept = Department("TestDepartment")
        dept.save_to_db()
        response = client.get('/api/department/' + dept.uuid)
        assert response.status_code == http.HTTPStatus.OK
        self.assertEqual(response.json.get("uuid"), dept.uuid)
        self.assertEqual(response.json.get("name"), dept.name)

        response = client.get('/api/department/wronguuid')
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        client = app.test_client()
        with client:
            response = client.post('/api/department')
            self.assertEqual(response.status_code, 400)
            response = client.post('/api/department', data=json.dumps(dict(name='TestDep')),
                                   content_type='application/json')
            departments = json.loads(response.data)
            self.assertEqual(departments.get("name"), 'TestDep')
            response = client.post('/api/department', data=json.dumps(dict(name='TestDep')),
                                   content_type='application/json')
            self.assertEqual(response.status_code, 400)
            #self.assertTrue(str(json.loads(response.data)).find("Department with this name already exists'"))
            response = client.post('/api/department', data=json.dumps(dict(name='01')),
                                   content_type='application/json')
            self.assertTrue(str(json.loads(response.data)).find("Shorter than minimum length 3"))

    def test_put(self):
        client = app.test_client()
        with client:
            response = client.put('/api/department')
            self.assertEqual(response.status_code, 400)

            response = client.put('/api/department/wrongudid', data=json.dumps(dict(name='TestDep')),
                                  content_type='application/json')
            self.assertEqual(response.status_code, 404)

            dept = Department.get_all()[0]
            response = client.put('/api/department/' + dept.uuid, data=json.dumps(dict(name='NewName')),
                                  content_type='application/json')
            self.assertEqual(response.status_code, 200)

            response = client.put('/api/department/' + dept.uuid, data=json.dumps(dict(name='01')),
                                  content_type='application/json')
            self.assertTrue(str(json.loads(response.data)).find("Shorter than minimum length 3"))

            response = client.put('/api/department/' + dept.uuid, data=json.dumps(dict(name='NewName')),
                                  content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_delete(self):
        client = app.test_client()
        with client:
            response = client.delete('/api/department')
            self.assertEqual(response.status_code, 400)

            response = client.delete('/api/department/blabla')
            self.assertEqual(response.status_code, 404)

            dept = Department.get_all()[0]
            response = client.delete('/api/department/' + dept.uuid)
            self.assertEqual(204, response.status_code)
