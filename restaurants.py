
# coding: utf-8

# In[1]:


import httplib2 # http client library in python
import json # converting in-memory python objects to a serialized JSON representation
import sys
import codecs


# In[2]:


google_api_key = "AIzaSyD5De3ZKuZ74FRE-kEnPghTaYKA8fLeWX0"

# https://maps.googleapis.com/maps/api/geocode/json?address=+Geneva,+Switzerland&key=AIzaSyD5De3ZKuZ74FRE-kEnPghTaYKA8fLeWX0


foursquare_client_id = "ZZXHI411CVMMLR1BPQQCBDMT15515BAHT0DTL3XIOZTNB4VC"
foursquare_client_secret = "SZTXGKKLW2FH2G2VBNM2JERJ1VJG2KDY54L3QSWRWXHNRQUW"

# https://api.foursquare.com/v2/venues/search?client_id=ZZXHI411CVMMLR1BPQQCBDMT15515BAHT0DTL3XIOZTNB4VC&client_secret=SZTXGKKLW2FH2G2VBNM2JERJ1VJG2KDY54L3QSWRWXHNRQUW&v=20130815&ll=37.392971,-122.076044&query=Pizza
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)


# In[3]:

def getGeolocation(location):
    locationString = location.replace(' ', '+')
    geoUrl = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (
            locationString, google_api_key
          ))

    h = httplib2.Http()
    response, content = h.request(geoUrl, 'GET')

    result = json.loads(content)

    # get longitude and latitude
    ll = str(result['results'][0]['geometry']['location']['lat']) + ',' + str(result['results'][0]['geometry']['location']['lng'])
    return ll

def findARestaurant(mealType, location):
    h = httplib2.Http()

    ll = getGeolocation(location)

    restaurantsUrl = ("https://api.foursquare.com/v2/venues/search?client_id=ZZXHI411CVMMLR1BPQQCBDMT15515BAHT0DTL3XIOZTNB4VC&client_secret=SZTXGKKLW2FH2G2VBNM2JERJ1VJG2KDY54L3QSWRWXHNRQUW&v=20130815&ll=%s&limit=1&query=%s" %
                      (ll, mealType))


    response, content = h.request(restaurantsUrl, 'GET')

    result = json.loads(content)




    if result["meta"]["code"] == 200 and result['response']['venues']:
        restaurants = result['response']['venues']
        resultId = restaurants[0]['id']

        address = ', '.join(restaurants[0]['location']['formattedAddress'])
        name = restaurants[0]['name']

        print(name)
        print(address)

        imageUrl = ('https://api.foursquare.com/v2/venues/%s/photos?v=20130815&client_id=%s&client_secret=%s&limit=1' % (resultId, foursquare_client_id, foursquare_client_secret))

        response, content = h.request(imageUrl, 'GET')

        result = json.loads(content)

        image = 'http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct'

        photos = result['response']['photos']
        if photos['count'] > 0:
            prefix = photos['items'][0]['prefix']
            suffix = photos['items'][0]['suffix']
            image = prefix + 'original' + suffix
        return {"image":image, "name":name, "address":address}
    else:
        print("No Restaurants Found for %s in %s." % (mealType, location))
        return None


# In[4]:


