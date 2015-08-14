import logging
import cassandra.cluster

KEYSPACE_NAME = 'e63'
TABLE_NAME = 'interactions'

session = cassandra.cluster.Cluster().connect()

# create the keyspace if it does not exist
session.execute('''CREATE KEYSPACE IF NOT EXISTS %s
                    WITH REPLICATION = 
                      { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
                ''' % (KEYSPACE_NAME))

# create the table if it does not exist
session.execute('''CREATE TABLE IF NOT EXISTS %s.%s (
                    user_id text,
                    time_stamp double,
                    duration double,
                    latitude double,
                    longitude double,
                    PRIMARY KEY (user_id, time_stamp)
                  )''' % (KEYSPACE_NAME, TABLE_NAME))

# prepare the CQL statement for inserting interactions into the database
prepared = session.prepare('''INSERT INTO e63.interactions
            (user_id, time_stamp, duration, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)''')

# inserts the interaction's values into the database
def insertInteraction(i):
  query = '''INSERT INTO interactions (user_id, time_stamp, duration, latitude, longitude)
              VALUES (\"%s\", %s, %s, %s, %s)''' \
              % (i.user_id, i.time_stamp, i.duration, i.coords.latitude, i.coords.longitude)
  logging.getLogger().debug("Query: " + query)
  session.execute(prepared, 
    (i.user_id, i.time_stamp, i.duration, i.coords.latitude, i.coords.longitude))
