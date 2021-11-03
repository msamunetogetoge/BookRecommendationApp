from django.test import TestCase

from Login.models import M_User
from Login.views import canlogin

# Create your tests here.

class ViewTests(TestCase):
    def test_cannot_login(self):
        """[summary]
        存在しないID,PASSは見つからない事を確かめる
        """
        id=""
        passw=""
        self.assertEqual(canlogin(id,passw), False)
    
    def test_can_login(self):
        """[summary]
        存在するID,PASSが見つかる事を確かめる
        """
        test_id = "test"
        test_name = "test"
        test_pass = "test"
        test_email="test@test.com"
        M_User.objects.get_or_create(id=test_id, name=test_name, password=test_pass, email=test_email)
        try:
            self.assertEqual(canlogin(test_name,test_pass), True)
        except Exception as e:
            self.AssertionError(e)
        finally:
            test_user = M_User.objects.get(id=test_id)
            test_user.delete()
        