#
# This script converts the data extracted by extract_data.py into a json file
# whose objects conform to the interaction service specification. The data is
# written to interactions.json in the same directory.
#
# To use this script
# 1. Follow the steps listed in extract_data.py
# 2. Run the script using the command:
#     python convert_interactions.py
# 3. The script will take several minutes to execute
# 4. Check the new interactions.json file in the same directory
#

from datetime import datetime
import calendar
import uuid

def parseDate(d, t): 
  return datetime.strptime(' '.join([d, t]), '%Y-%m-%d %H:%M:%S')

uuid_map = {}
def uuidForUserNum(num):
  if not num in uuid_map:
    uuid_map[num] = uuid.uuid4()
  return uuid_map[num]


def parseLine(line):
  tokens = line.split(',')
  user_id = str(uuidForUserNum(tokens[0]))
  return {
    'user_id': user_id,
    'latitude': tokens[1],
    'longitude': tokens[2],
    'date': parseDate(tokens[3], tokens[4].rstrip())
  }

def timeDelta(start, end):
  return (end['date'] - start['date']).total_seconds() * 1000

def timeStamp(interaction):
  return calendar.timegm(interaction['date'].timetuple())


def createInteraction(start, end):
  return {
    'user_id': start['user_id'],
    'time_stamp': timeStamp(start),
    'duration': timeDelta(start, end),
    'latitude': start['latitude'],
    'longitude': start['longitude'],
  }

def createInteractions(path):
  MAX_INTERACTION_DELTA = 5 * 60 * 1000 # 5 minutes
  start, prev, cur = None, None, None
  interactions = []
  counter = 0
  with open(path) as infile:
    for line in infile:
      if start == None:
        start = parseLine(line)
        prev = start
      else:
        cur = parseLine(line)
        if timeDelta(start, cur) > MAX_INTERACTION_DELTA or \
          start['user_id'] != cur['user_id']:
          if start['user_id'] == cur['user_id']:
            counter += 1
          else:
            counter = 1
          interactions.append(createInteraction(start, prev))
          print 'user: {0} interaction: {1} created'.format(start['user_id'], counter)
          start, cur, prev = None, None, None
        else:
          prev = cur 
  if cur != None:
    interactions.append(createInteraction(start, cur))
  return interactions


def run():
  with open('interactions.csv', 'w') as outfile:
    for interaction in createInteractions('user_interactions.csv'):
      outfile.write('{0},{1},{2},{3},{4}\n'.format(
        interaction['user_id'],
        interaction['time_stamp'],
        interaction['duration'],
        interaction['latitude'],
        interaction['longitude'],))
   # json.dump(createInteractions('user_interactions.csv'), outfile)
    

if __name__ == '__main__':
  run()