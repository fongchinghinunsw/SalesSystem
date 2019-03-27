"""Create test fixtures"""

import pytest

from app.core import create_app


@pytest.fixture
def app():
  app = create_app('app.tests.settings')  #pylint: disable=redefined-outer-name

  yield app


@pytest.fixture
def client(app):  #pylint: disable=redefined-outer-name
  return app.test_client()
