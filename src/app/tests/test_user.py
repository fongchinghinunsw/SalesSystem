"""Module to test the user model class"""
import pytest
from app.core.models.user import User


def test_user_password():
  """ Test user password
  """
  user = User(email="test@foo.bar", user_type=0)
  user.SetPassword("test_pwd")
  assert user.VerifyPassword("test_pwd")
  assert not user.VerifyPassword("wrong_pwd")
  assert not user.VerifyPassword(None)


def test_invalid_length_for_new_password():
  """ Test new password with invalid length (< 4 or > 20)
  provided by user
  """
  user = User(email="test@foo.bar", user_type=0)
  user_password = "ILoveHTML"
  user.SetPassword(user_password)

  new_password1 = "pwd"
  with pytest.raises(ValueError):
    user.SetPassword(new_password1)
  assert user.VerifyPassword(new_password1) is False
  assert user.VerifyPassword(user_password)

  new_password2 = "I love meatball and tuna."
  with pytest.raises(ValueError):
    user.SetPassword(new_password2)
  assert user.VerifyPassword(new_password2) is False
  assert user.VerifyPassword(user_password)
