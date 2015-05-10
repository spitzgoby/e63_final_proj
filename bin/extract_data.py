#
# This script extracts and coallates the trajectory data from the GeoLife GPS 
# dataset provided by Microsoft (link: http://bit.ly/1KKSzms). The data is 
# written to user_interactions.csv in the same directory. 
#
# To use this script
# 1. Download the Geolife Trajectories zip file from http://bit.ly/1KKSzms
# 2. Unzip the file and place this script in the Geolife Trajectories 1.3
#    directory you just created
# 3. Run the script using the command: 
#       python extract_data.py
# 4. The script may take a few minutes to execute. 
# 5. Check the new user_interactions.csv file in the same directory
#
# Sample Output:
# user_id,latitude,longitude,date,time
# 000,39.984702,116.318417,2008-10-23,02:53:04
# 000,39.984683,116.31845,2008-10-23,02:53:10
# 000,39.984686,116.318417,2008-10-23,02:53:15
# 000,39.984688,116.318385,2008-10-23,02:53:20
# 000,39.984655,116.318263,2008-10-23,02:53:25
# 000,39.984611,116.318026,2008-10-23,02:53:30
# 000,39.984608,116.317761,2008-10-23,02:53:35
#

from os import listdir

def listdir_noh(path):
  return [item for item in listdir(path) if not item[0] == '.']

def extractInteraction(user_id, line):
  tokens = line.split(',')
  latitude = tokens[0]
  longitude = tokens[1]
  date = tokens[5] 
  time = tokens[6].rstrip()
  return ','.join([user_id,latitude,longitude,date,time])

def buildFilePaths():
  paths = []
  for user in listdir_noh('./Data'):
    for path in listdir_noh('./Data/' + user + '/Trajectory'):
      if not path[0] == '.': # ignore hidden files
        paths.append((user, path)) 
  return paths

def readInteractions():
  interactions = []
  for user, path in buildFilePaths():
      with open('./Data/' + user + '/Trajectory/' + path) as inFile:
        print 'Reading trajectories for user {0}, file {1}'.format(user, path)
        interactions.extend([extractInteraction(user, i) for i in inFile.readlines()[6:]])
  return interactions

def writeInteractions(interactions):
  with open('user_interactions.csv', mode='w') as outFile:
    print 'Writing trajectories to file, this may take a few minutes...'
    outFile.write('\n'.join(interactions))

def run():
  interactions = readInteractions()
  writeInteractions(interactions)

if __name__ == '__main__':
  run()

