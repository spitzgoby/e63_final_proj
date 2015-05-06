import logging
import cassandra.cluster

KEYSPACE_NAME = 'e63'
TABLE_NAME = 'interactions'

session = cassandra.cluster.Cluster().connect()

session.execute('''CREATE KEYSPACE IF NOT EXISTS {0} 
                    WITH REPLICATION = { 'class': 'SimpleStrategy',
                                          'replication_factor': 1 };
                '''.format(KEYSPACE_NAME))

session.execute('''CREATE TABLE IF NOT EXISTS {0}.{1} (
                    user_id uuid,
                    time_stamp double,
                    duration double,
                    latitude double,
                    longitude double,
                    PRIMARY KEY (user_id, time_stamp)
                  )'''.format(KEYSPACE_NAME, TABLE_NAME))

prepared = session.prepare('''INSERT INTO e63.interactions
            (user_id, time_stamp, duration, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)''')
def insertInteraction(i):
  query = '''INSERT INTO interactions
            (user_id, time_stamp, duration, latitude, longitude)
            VALUES ("{0}", {1}, {2}, {3}, {4})'''.format(
              i.user_id,
              i.time_stamp,
              i.duration,
              i.coords.latitude, 
              i.coords.longitude)
  logging.getLogger().debug("Query: " + query)
  session.execute(prepared, 
    (i.user_id, i.time_stamp, i.duration, i.coords.latitude, i.coords.longitude))
