CREATE KEYSPACE IF NOT EXISTS e63 WITH REPLICATION =
    { 'class' : 'SimpleStrategy', 'replication_factor' : 1};

CREATE TABLE IF NOT EXISTS e63.interactions (
    user_id text,
    time_stamp double,
    duration double,
    latitude double,
    longitude double,
    PRIMARY KEY (user_id, time_stamp));

COPY e63.interactions 
    (user_id, time_stamp, duration, latitude, longitude)
    FROM 'data/interactions.csv';
CREATE TABLE IF NOT EXISTS e63.cities (
    name varchar PRIMARY KEY,
    country varchar, 
    latitude double, 
    longitude double);
COPY e63.cities 
    (name, latitude, longitude, country) 
    FROM 'data/cities.csv';