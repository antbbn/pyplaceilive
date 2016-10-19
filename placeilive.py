import requests

class PlaceiliveError(Exception):
  """Specific exception for placeilive.com API error"""
  pass

class AddressNotFoundError(Exception):
  """Specific exception for placeilive.com API error"""
  pass


def _request_placeilive(address, base_url = 'https://api.placeilive.com/v1/houses/search'):
  """ This function performs an API request. 
  The api is quite simple and the only input it requires is
  a string.  It returns a JSON response.

  Returns an array of dictionaries since usually a search via
  this api returns multiple results
  """

  res = requests.get(base_url, params = {'q': address})
  if res.status_code != requests.codes.ok :
    raise PlaceiliveError("Error code {}".format(r.status_code))

  # A good request will return a JSON array of dictionaries.
  return res.json()

def get_lqi(address):
  """ 
  This function extracts the overall Life Quality Index 
  from the placeilive.com API response. 
  """

  result = _request_placeilive(address)
  lqi = []
  for entry in result:
    try:
      lqi.append(int(entry["lqi"]["value"]))
    except (ValueError, KeyError):
      pass

  if lqi:
    return lqi
  else:
    raise AddressNotFoundError("No lqi values found")


def get_category_lqi(address, category):
  """ 
  This function extracts the specific Life Quality Index 
  from the placeilive.com API response given a particular category.

  Valid values for the category are:
      "Daily Life"
      "Demographics"
      "Entertainment"
      "Health"
      "Safety"
      "Sports And Leisure"
      "Transportation"
  """
  result = _request_placeilive(address)
  lqi = []
  for entry in result:
    for cat in entry["lqi_category"]:
      if cat["type"] == category:
        # This try-catch is necessary since sometimes
        # value is 'N/A'. We just ignore it.
        try: 
          lqi.append(int(cat["value"]))
        except (ValueError, KeyError):
          pass

  if lqi:
    return lqi
  else:
    raise AddressNotFoundError("No category lqi values found")




print(get_lqi("Pankow"))
print(get_lqi("Kreuzberg"))
print(get_category_lqi("Pankow","Transportation"))
print(get_category_lqi("Pankow","Safety"))
print(get_lqi("Nonexistant"))

