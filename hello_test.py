import hello
import unittest

class topTestCase(unittest.TestCase):

    def setUp(self):
        hello.app.testing = True
        self.app = hello.app.test_client()

    def tearDown(self):
        pass

    def test_top(self):
        response = self.app.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('ユーザ一覧', html)
        self.assertIn('admin', html)
        self.assertIn('user', html)


if __name__ == '__main__':
    unittest.main()
