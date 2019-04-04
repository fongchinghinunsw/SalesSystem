"""Module to test the admin blueprint"""


def test_index(client):
  """ Test admin index
  Arguments:
    client: flask client
  """
  response = client.get('/admin/')
  assert b"Hello this is admin" in response.data

def test_order_list(client):
  response = client.get('/admin/order/')
  rsp = str(response.data)
  assert "id" in rsp
  assert "user_name" in rsp
  assert "price" in rsp
  assert "create_at" in rsp
  assert "updated_at" in rsp
  assert "status" in rsp
>>>>>>> admin:tests of displaying order list
