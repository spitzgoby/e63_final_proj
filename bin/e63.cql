-- Create E63 keyspace
CREATE KEYSPACE IF NOT EXISTS e63 WITH REPLICATION =
    { 'class' : 'SimpleStrategy', 'replication_factor' : 1};

-- Each interaction is uniquely identified by the id of the user and the time
-- when the interaction was created.
CREATE TABLE IF NOT EXISTS e63.interactions (
    user_id text,
    time_stamp double,
    duration double,
    latitude double,
    longitude double,
    PRIMARY KEY (user_id, time_stamp));

-- Copy interaction data from csv file created by convert_interactions.py
COPY e63.interactions 
    (user_id, time_stamp, duration, latitude, longitude)
    FROM 'data/interactions.csv';
-- Create table for city data
CREATE TABLE IF NOT EXISTS e63.cities (
    name varchar PRIMARY KEY,
    country varchar, 
    latitude double, 
    longitude double);
-- Copy cities from csv file created by convert_cities.py
COPY e63.cities 
    (name, latitude, longitude, country) 
    FROM 'data/cities.csv';