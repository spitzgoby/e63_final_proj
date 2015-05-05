#! finalenv/bin/python

import flask
import json
from interaction import Interaction

import argparse
import logging

from sys import stderr

service = flask.Flask(__name__)

#--------------#
# *** CRUD *** #
#--------------#

@service.route("/interactions/api/v1.0/report", methods=['POST'])
def create_interaction():
  """Validate the posted json object
  """
  request = flask.request
  if not request.json:
    print("Not json")
    print(request)
    flask.abort(400)
  if not Interaction.validate_interaction(request.json):
    flask.abort(400)
  interaction = Interaction(request.json)
  #interaction_db.add(interaction)
  return json.dumps(interaction, default = lambda obj: obj.__dict__), 201
  #return flask.jsonify({'interaction' : 'accepted'}), 201


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






