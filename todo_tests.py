import unittest
import json
from app import app

class TodoTest(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		rp = self.app.post('/login', data=dict(
		username='test',
		password='secret'
		), follow_redirects=True)
		for item in rp.response:
			access_token = json.loads(item)["access_token"]
			self.head = {'Authorization': 'Bearer {}'.format(access_token) }

	def tearDown(self):
		pass

	def test_bad_login(self):
		rp = self.app.post('/login', data=dict(
		username='test',
		password='incorrect_secret'
		), follow_redirects=True)
		self.assertEqual(rp.status_code, 401)

	def test_good_login(self):
		rp = self.app.post('/login', data=dict(username='test', password='secret'), follow_redirects=True)
		for item in rp.response:
			self.access_token = json.loads(item)["access_token"]
		self.assertEqual(rp.status_code, 200)

	def test_list(self):
		rp = self.app.get('/list', headers=self.head, follow_redirects=True)
		currentList = json.loads(next(x for x in rp.response))
		self.assertEqual(rp.status_code, 200)
		self.assertIn("list", currentList)
		self.assertGreaterEqual(len(currentList["list"]), 0)

	def test_add(self):
		rp = self.app.post('/add', data=dict(name='test_task_1'), headers=self.head, follow_redirects=True)
		newTask = json.loads(next(x for x in rp.response))
		self.assertEqual(rp.status_code, 200)
		self.assertEqual(newTask["name"], "test_task_1")

	def test_update(self):
		rp = self.app.post('/add', data=dict(name='test_task_2'), headers=self.head, follow_redirects=True)
		self.assertEqual(rp.status_code, 200)
		newTask = json.loads(next(x for x in rp.response))
		self.assertEqual(newTask["name"], "test_task_2")

		rp = self.app.post('/update', data=dict(id=newTask["id"],name='test_task_2_modified'), headers=self.head, follow_redirects=True)
		newTaskModified = json.loads(next(x for x in rp.response))
		self.assertEqual(rp.status_code, 200)
		self.assertEqual(newTaskModified["name"], "test_task_2_modified")

	def test_delete(self):
		rp = self.app.post('/add', data=dict(name='test_task_3'), headers=self.head, follow_redirects=True)
		self.assertEqual(rp.status_code, 200)
		newTask = json.loads(next(x for x in rp.response))
		self.assertEqual(newTask["name"], "test_task_3")

		rp = self.app.post('/delete', data=dict(id=newTask["id"]), headers=self.head, follow_redirects=True)
		deletedTask = json.loads(next(x for x in rp.response))
		self.assertEqual(rp.status_code, 200)
		self.assertEqual(deletedTask["id"], newTask["id"])
		self.assertEqual(deletedTask["name"], "test_task_3")

if __name__ == "__main__":
	unittest.main()