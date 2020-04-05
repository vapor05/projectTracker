import unittest

from trackerApp.tests.test_user_views import UserViewTests
from trackerApp.tests.test_core_views import CoreViewTests
from trackerApp.tests.test_models import ModelTests
from trackerApp.tests.test_project_views import ProjectViewTests
from trackerApp.tests.test_task_views import TaskViewTests
from trackerApp.tests.test_item_views import ItemViewTests
from trackerApp.tests.test_comment_views import CommentViewTests

def suite():
    suite = unittest.TestSuite()
    suite.addTest(UserViewTests("test_register"))
    suite.addTest(UserViewTests("test_login"))
    suite.addTest(UserViewTests("test_home_page"))
    suite.addTest(UserViewTests("test_logout"))

    suite.addTest(CoreViewTests("test_index"))

    suite.addTest(ModelTests("test_user"))
    suite.addTest(ModelTests("test_project"))
    suite.addTest(ModelTests("test_task"))

    suite.addTest(ProjectViewTests("test_create_project"))
    suite.addTest(ProjectViewTests("test_update_project"))

    suite.addTest(TaskViewTests("test_add_task"))
    suite.addTest(TaskViewTests("test_update_task"))

    suite.addTest(ItemViewTests("test_add_item"))
    suite.addTest(ItemViewTests("test_update_item"))

    suite.addTest(CommentViewTests("test_add_project_comment"))
    suite.addTest(CommentViewTests("test_add_task_comment"))
    suite.addTest(CommentViewTests("test_add_item_comment"))
    suite.addTest(CommentViewTests("test_update_project_comment"))
    suite.addTest(CommentViewTests("test_update_task_comment"))
    suite.addTest(CommentViewTests("test_update_item_comment"))

    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
