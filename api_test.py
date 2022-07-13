import requests
import unittest


class APITest(unittest.TestCase):
    API_URL = 'http://localhost:8080/test-api/bank/'

    def test_delete_all(self):
        resp = requests.delete(self.API_URL)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json(), list)
        resp = requests.get(self.API_URL)
        self.assertEqual(len(resp.json()), 0)

    def test_get_all(self):
        resp = requests.get(self.API_URL)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json(), list)
        self.assertEqual(len(resp.json()), 0)

    def test_post(self):
        resp = requests.post(self.API_URL, json={
                             'accountName': 'vlad', 'accountWallet': 56})
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['accountName'], 'vlad')
        self.assertEqual(resp.json()['accountWallet'], 56)
        resp = requests.get(self.API_URL)
        self.assertEqual(len(resp.json()), 1)

    def test_get_id(self):
        resp = requests.get(self.API_URL+"1")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['accountName'], 'vlad')
        self.assertEqual(resp.json()['accountWallet'], 56)
        resp = requests.get(self.API_URL+"2")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json()['message'], 'Index 2 not found')

    def test_put_id(self):
        resp = requests.put(self.API_URL+"5", json={})
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json()['message'], 'Index 5 not found')

        resp = requests.put(self.API_URL+"1", json={})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['accountName'], 'vlad')
        self.assertEqual(resp.json()['accountWallet'], 56)

        resp = requests.put(self.API_URL+"1", json={'accountName': 'qwert'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['accountName'], 'qwert')
        self.assertEqual(resp.json()['accountWallet'], 56)

        resp = requests.put(self.API_URL+"1", json={'accountWallet': 526})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['accountName'], 'qwert')
        self.assertEqual(resp.json()['accountWallet'], 526)

        resp = requests.put(
            self.API_URL+"1", json={'accountName': 'qwertq', 'accountWallet': 5326})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['accountName'], 'qwertq')
        self.assertEqual(resp.json()['accountWallet'], 5326)

    def test_del_id(self):
        resp = requests.delete(self.API_URL+"5")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json()['message'], 'Index 5 not found')

        resp = requests.delete(self.API_URL+"1")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['accountName'], 'qwertq')
        self.assertEqual(resp.json()['accountWallet'], 5326)

        resp = requests.get(self.API_URL)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 0)
