#! finalenv/bin/python

import flask

service = flask.Flask(__name__)

@service.route("/")
def hello():
  return "Hello world!"

if __name__ == '__main__':
  service.run(debug=True)