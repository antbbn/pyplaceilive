import requests

class PlaceILiveError(Exception):
  """Specific exception for placeilive.com API error"""
  pass

class AddressNotFoundError(Exception):
  """Specific exception for placeilive.com API error"""
  pass

class PlaceILiveRequest:
  base_url = 'https://api.placeilive.com/v1/houses/search'

  def __init__(self, address, base_url = None):
    """ This function performs an API request. 
    The api is quite simple and the only input it requires is
    a string.  It returns a JSON response.
    The second argument is there just in case something changes
    with the API (e.g. version).
  
    Returns an array of dictionaries since usually a search via
    this api returns multiple results
    """
  
    if base_url is not None:
      self.base_url = base_url

    res = requests.get(self.base_url, params = {'q': address})
    if res.status_code != requests.codes.ok :
      if res.status_code == 404:
        raise AddressNotFoundError("Address Not Found")
      else:
        raise PlaceILiveError("Error code {}".format(res.status_code))
  
    # A good request will return a JSON array of dictionaries.
    self.result = res.json()

  def get_lqi(self):
    """ 
    This function extracts the overall Life Quality Index 
    from the placeilive.com API response. 
    """
  
    lqi = []
    for entry in self.result:
      try:
        lqi.append(int(entry["lqi"]["value"]))
      except (ValueError, KeyError):
        pass
  
    if lqi:
      return lqi
    else:
      raise AddressNotFoundError("No lqi values found")


  def get_category_lqi(self,category):
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
    lqi = []
    for entry in self.result:
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



if __name__ == "__main__":
  query = "Pankow"
  pil = PlaceILiveRequest(query)

  # An example
  print(query,": ",pil.get_lqi())
  print(query,", Transportation: ", pil.get_category_lqi("Transportation"))

  query = "Nonexistant"
  try:
    pil = PlaceILiveRequest(query)
    print(query,": ", pil.get_lqi())
  except AddressNotFoundError as e:
    print("Address Not Found: ", e)

  query = "Dircksenstr. 47 10178 Berlin"
  try:
    pil = PlaceILiveRequest(query)
    print(query,": ",pil.get_lqi())
  except AddressNotFoundError as e:
    print("Address Not Found: ", e)

