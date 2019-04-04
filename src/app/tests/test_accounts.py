"""Module to test the accounts blueprint"""


def test_index(client):
  """ Test accounts index
  Arguments:
    client: flask client
  """
  response = client.get('/accounts/')
  assert b"Hello this is accounts" in response.data
