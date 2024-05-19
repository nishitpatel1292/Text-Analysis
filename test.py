import unittest
from main import app
from werkzeug.datastructures import FileStorage

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_analyze_sentiment(self):
        with open('test.txt', 'rb') as f:
            response = self.app.post('/sentiment-analyze', data={'file': (f, 'test.txt')})
        self.assertEqual(response.status_code, 200)

    def test_generate_keywords(self):
        with open('test.txt', 'rb') as f:
            response = self.app.post('/keyword-cloud', data={'file': (f, 'test.txt')})
        self.assertEqual(response.status_code, 200)

    def test_topic_detection(self):
        with open('test.txt', 'rb') as f:
            response = self.app.post('/topic-detection', data={'file': (f, 'test.txt')})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()