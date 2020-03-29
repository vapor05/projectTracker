import os
import unittest

from trackerApp import app, db
from trackerApp.models import User, Project
from trackerApp.tests.BaseTest import BaseTest

TEST_DB = 'test.db'

class CoreViewTests(BaseTest, unittest.TestCase):

    def test_index(self):
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Track Your Projects', response.data)

if __name__ == "__main__":
    unittest.main()
