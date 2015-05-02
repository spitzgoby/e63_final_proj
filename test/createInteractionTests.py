#! testenv/bin/python
import json
import time
import requests

INTERACTION_USER_ID = 'user_id'
INTERACTION_TIME_STAMP = 'time_stamp'
INTERACTION_DURATION = 'duration'
INTERACTION_COORDS = 'coords'
COORDS_LATITUDE = 'latitude'
COORDS_LONGITUDE = 'longitude'

def createInteraction(user_id, time_stamp, duration, latitude, longitude):
  return {
    INTERACTION_USER_ID: str(user_id),
    INTERACTION_TIME_STAMP: str(time_stamp),
    INTERACTION_DURATION: str(duration),
    INTERACTION_COORDS: {
      COORDS_LATITUDE: str(latitude),
      COORDS_LONGITUDE: str(longitude),
    }
  }

def postInteraction(interaction):
  url = "http://localhost:5000/interactions/api/v1.0/report"
  headers = {'Content-type' : 'application/json'}
  return requests.post(url, data=json.dumps(interaction), headers=headers)

def testCreateSimpleInteraction():
  timeStamp = time.time()
  validInteraction = createInteraction(1, timeStamp, 100, 100, 100)
  response = postInteraction(validInteraction)
  assert(response.status_code == 201)

  response.interaction = response.json()['interaction']
  assert(int(response.interaction[INTERACTION_USER_ID]) == 1)
  assert(float(response.interaction[INTERACTION_TIME_STAMP]) == timeStamp)
  assert(float(response.interaction[INTERACTION_DURATION]) == 100)

def runTests():
  testCreateSimpleInteraction()