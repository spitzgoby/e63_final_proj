from sys import stderr
import logging
import cassandra.cluster

logging.basicConfig(stream=stderr, level=logging.DEBUG)
session = cassandra.cluster.Cluster().connect()

session.execute('''CREATE KEYSPACE IF NOT EXISTS e63
                    WITH REPLICATION =
                    { 'class' : 'SimpleStrategy', 'replication_factor' : 1};
                ''')

session.execute('''CREATE TABLE IF NOT EXISTS e63.interactions (
                    user_id text,
                    time_stamp double,
                    duration double,
                    latitude double,
                    longitude double,
                    PRIMARY KEY (user_id, time_stamp));
                ''')

session.execute("COPY e63.interactions (user_id, time_stamp, duration, latitude, longitude) from '~/e63_final_proj/data/interactions.csv';")
session.execute("CREATE TABLE IF NOT EXISTS e63.cities (name varchar PRIMARY KEY, country varchar, latitude double, longitude double);")
session.execute("COPY e63.cities (name, latitude, longitude, country) from '~/e63_final_proj/data/cities.csv';")