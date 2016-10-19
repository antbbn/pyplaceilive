import requests

class PlaceiliveError(Exception):
  """Specific exception for placeilive.com API error"""
  pass

class AddressNotFoundError(Exception):
  """Specific exception for placeilive.com API error"""
  pass


# This function returns the Life Quality Index using the
# placeilive.com API. 
# The api is quite simple and the only input it requires is
# a string. It returns a JSON response.

def _request_placeilive(address, base_url = 'https://api.placeilive.com/v1/houses/search'):
  res = requests.get(base_url, params = {'q': address})
  if res.status_code != requests.codes.ok :
    raise PlaceiliveError("Error code {}".format(r.status_code))

  # A good request will return a JSON array of dictionaries.
  # every dictionary will contain a match and the relative 
  return res.json()

def get_lqi(address):
  result = _request_placeilive(address)
  lqi = []
  for entry in result:
    try:
      lqi.append(int(entry["lqi"]["value"]))
    except ValueError:
      lqi.append(-1)

  return lqi

#def get_category_lqi(address, category):
#  result = _request_placeilive(address)
#  lqi = []
#  for entry in result:
#    for cat in entry["lqi"]["lqi_category"]:
#      if cat["type"] == category:


print(get_lqi("Pankow"))
print(get_lqi("Kreuzberg"))

