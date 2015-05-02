#! finalenv/bin/python

import flask

service = flask.Flask(__name__)


#--------------#
# *** CRUD *** #
#--------------#


'''
interaction format
{
  user_id: "1",
  post_id: "1",
  coords: {
    latitude: 00.00,
    longitude: 00.00,
  }
  interaction_duration: "10000",
}
'''
interactions = []

INTERACTION_USER_ID = 'user_id'
INTERACTION_TIME_STAMP = 'time_stamp'
INTERACTION_DURATION = 'duration'
INTERACTION_COORDS = 'coords'
COORDS_LATITUDE = 'latitude'
COORDS_LONGITUDE = 'longitude'

def validate_interaction(interaction):
  """Return true if the json represents a valid interaction object
  """
  # Attempt to parse the objects, exceptions represent invalid objects
  try:
    int(interaction[INTERACTION_USER_ID])
    print("User id validated")
    float(interaction[INTERACTION_TIME_STAMP])
    print("Timestamp validated")
    int(interaction[INTERACTION_DURATION])
    print("Duration validated")
    float(interaction[INTERACTION_COORDS][COORDS_LATITUDE])
    print("Latitude validated")
    float(interaction[INTERACTION_COORDS][COORDS_LONGITUDE])
    print("Longitude validated")
    print("Coords validated")
  except (KeyError, ValueError):
    return False
  return True

@service.route("/interactions/api/v1.0/report", methods=['POST'])
def create_interaction():
  """
  """
  request = flask.request
  if not request.json:
    print("Not json")
    print(request)
    flask.abort(400)
  if not validate_interaction(request.json):
    flask.abort(400)
  interaction = {
    INTERACTION_USER_ID: request.json[INTERACTION_USER_ID],
    INTERACTION_TIME_STAMP: request.json[INTERACTION_TIME_STAMP],
    INTERACTION_DURATION: request.json[INTERACTION_DURATION],
    INTERACTION_COORDS: {
      COORDS_LATITUDE: request.json[INTERACTION_COORDS][COORDS_LATITUDE],
      COORDS_LONGITUDE: request.json[INTERACTION_COORDS][COORDS_LONGITUDE],
    }
  }
  interactions.append(interaction)
  return flask.jsonify({'interaction' : interaction}), 201


#------------------------#
# *** ERROR HANDLING *** #
#------------------------#


if __name__ == '__main__':
  service.run(debug=True)