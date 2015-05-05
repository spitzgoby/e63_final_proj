import logging
import cassandra.cluster

session = cassandra.cluster.Cluster().connect('interactions')
session.execute('''CREATE TABLE IF NOT EXISTS interactions (
                    user_id text,
                    time_stamp double,
                    duration double,
                    latitude double,
                    longitude double,
                    PRIMARY KEY (user_id, time_stamp)
                  )''')

def add(interaction):
  query = '''INSERT INTO interactions
            (user_id, time_stamp, duration, latitude, longitude)
            VALUES ('{0}', {1}, {2}, {3}, {4})'''.format(
              interaction.user_id,
              interaction.time_stamp,
              interaction.duration,
              interaction.coords.latitude, 
              interaction.coords.longitude)
  logging.getLogger().debug("Query: " + query)          
  session.execute(query)
