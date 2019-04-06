def GetDetailsString(item, prefix=""):
  """Recursively get the details string for an order item node
  for invoice and order details"""
  ret = ""
  if item["type"] == "ig":
    prefix += item["name"] + ":"
    for child in item["options"]:
      ret += GetDetailsString(child, prefix)
  else:
    ret = "%s%s%s ......$%.2f\n" % (prefix, item['name'], "*%d" % item['num']
                                    if item['num'] > 1 else "", item['price'])

    prefix = (len(prefix) - len(prefix.lstrip()) + 2) * " "
    for child in item["igs"]:
      ret += GetDetailsString(child, prefix)
  return ret
