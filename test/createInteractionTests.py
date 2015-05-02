#! ../test/bin/python
import urllib2

INTERACTION_USER_ID = 'user_id'
INTERACTION_POST_ID = 'post_id'
INTERACTION_DURATION = 'duration'
INTERACTION_COORDS = 'coords'
COORDS_LATITUDE = 'latitude'
COORDS_LONGITUDE = 'longitude'

def createInteraction(user_id, post_id, duration, latitude, longitude):
  return {
    INTERACTION_USER_ID: str(user_id),
    INTERACTION_POST_ID: str(post_id),
    INTERACTION_DURATION: str(duration),
    INTERACTION_COORDS: {
      COORDS_LATITUDE: str(latitude),
      COORDS_LONGITUDE: str(longitude),
    }
  }

def testCreateSimpleInteraction():
  validInteraction = createInteraction(1, 1, 100, 100, 100)
