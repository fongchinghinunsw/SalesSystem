"""Module to test the user model class"""

from app.core.models.user import User


def test_user_password():
  """ Test user password
  """
  user = User(email="test@foo.bar", user_type=0)
  user.SetPassword("test_pwd")
  assert user.VerifyPassword("test_pwd")
  assert not user.VerifyPassword("wrong_pwd")
  assert not user.VerifyPassword(None)
