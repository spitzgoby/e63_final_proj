#! finalenv/bin/python

import flask

import argparse
import logging

from sys import stderr


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

INTERACTION_USER_ID = 'user_id'
INTERACTION_TIME_STAMP = 'time_stamp'
INTERACTION_DURATION = 'duration'
INTERACTION_COORDS = 'coords'
COORDS_LATITUDE = 'latitude'
COORDS_LONGITUDE = 'longitude'


def validate_interaction(interaction):
  """Return true if the json represents a valid interaction object

  Parameters:
  interaction - The json object to be validated
  """
  # Attempt to parse the objects, exceptions represent invalid objects
  logging.debug("Validating posted json data, %s" % (interaction))
  try:
    int(interaction[INTERACTION_USER_ID])
    logging.debug("User id validated")
    float(interaction[INTERACTION_TIME_STAMP])
    logging.debug("Timestamp validated")
    int(interaction[INTERACTION_DURATION])
    logging.debug("Duration validated")
    float(interaction[INTERACTION_COORDS][COORDS_LATITUDE])
    logging.debug("Latitude validated")
    float(interaction[INTERACTION_COORDS][COORDS_LONGITUDE])
    logging.debug("Longitude validated")
    logging.debug("Coords validated")
  except (KeyError, ValueError):
    return False
  return True

@service.route("/interactions/api/v1.0/report", methods=['POST'])
def create_interaction():
  """Validate the posted json object
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
  return flask.jsonify({'interaction' : interaction}), 201


#------------------------#
# *** ERROR HANDLING *** #
#------------------------#



#---------------#
# *** SETUP *** #
#---------------#

def parseArgs():
  '''Parse command line arguments
  '''
  parser = argparse.ArgumentParser(
    description='''
      The Interaction Service collections interaction reports from mobile devices
      and stores them for later analysis.
    ''')
  parser.add_argument('-d', '--debug', action='store_true', 
    help='Run service in debugging mode')
  parser.add_argument('-p', '--port', type=int, default=5000, 
    help='Run service on selected port (default is 5000)')

  return parser.parse_args()

def setupLogging(debugMode):
  '''Set logging environment variables
  '''
  if (debugMode):
    level = logging.DEBUG
  else:
    level = logging.INFO
  logging.basicConfig(stream=stderr, level=level)
  logging.debug("Logging configuration set")


#--------------#
# *** MAIN *** #
#--------------#

if __name__ == '__main__':
  args = parseArgs()
  setupLogging(args.debug)
  service.run(debug=args.debug, port=args.port, host='0.0.0.0')






