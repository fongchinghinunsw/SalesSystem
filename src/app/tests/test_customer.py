"""Module to test the customer blueprint"""


def test_index(client):
  """ Test customer index
  Arguments:
    client: flask client
  """
  response = client.get('/')
  assert b"Customer Routes - hello world" in response.data
