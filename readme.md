E63 Final Project
=================

Introduction
------------
A final project for Harvard Extension School's CSCIE-63 Big Data Analytics course

Goal
-----
Demonstrate an end to end solution for mobile analytics utilizing tools discussed in class

Components
----------
* A REST service that receives and stores interaction objects from users' 
  mobile devices
* Cassandra DB installation that stores user data
* A Spark installation that can run user defined scripts against the collected
  data and provide insight into the data
* A website using D3 visualization tools to present the analysis graphically
* Installation scripts and instructions detailing implementation

Installation
------------
* Follow [DataStax's instructions](http://docs.datastax.com/en/cassandra/2.1/cassandra/install/installAMI.html) to create an EC2 instance with Cassandra and
connect over SSH
* Close this repo with: `git clone https://github.com/spitzgoby/e63_final_proj.git`
* Change into the new directory e63_final_proj
* Run the installation script with `./bin/install.sh`
* 