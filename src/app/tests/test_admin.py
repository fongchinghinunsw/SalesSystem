"""Module to test the admin blueprint"""


def test_index(client):
  """ Test admin index
  Arguments:
    client: flask client
  """
  response = client.get('/admin/')
  assert b"Admin Routes - hello world" in response.data
