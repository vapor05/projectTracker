import unittest

from trackerApp.tests.test_user_views import UserViewTests
from trackerApp.tests.test_core_views import CoreViewTests

def suite():
    suite = unittest.TestSuite()
    suite.addTest(UserViewTests("test_register"))
    suite.addTest(UserViewTests("test_login"))
    suite.addTest(UserViewTests("test_home_page"))
    suite.addTest(UserViewTests("test_logout")) 

    suite.addTest(CoreViewTests("test_index"))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
