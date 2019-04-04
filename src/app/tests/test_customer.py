"""Module to test the customer blueprint"""


def test_index(client):
  """ Test customer index
  Arguments:
    client: flask client
  """
  response = client.get('/')
  assert b"Hello this is customer" in response.data
