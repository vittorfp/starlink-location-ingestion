# Starlink data ingestion

In this exercise I'll be loading some Starlink location data into InfluxDB and making some queries.
InfluxDB was chosen as a database because we are dealing with time series, and this database is optimized for this finality. 

### Initial setup

In order to run properly, the system needs to have some software installed:

- git 
- docker-compose

#### Start InfluxDB on Docker

````shell
git clone https://github.com/influxdata/sandbox.git
sudo sandbox/sandbox up
````

### Load data

Simply run (from the root folder of this repository):
````shell
git clone https://github.com/BlueOnionLabs/api-spacex-backend.git
python load_data.py
````
Now the data was loaded to the database.

### Query to get the last known location in a given time

You can run this query on the influx client Chronograph (that was already started too and can be accessed at [http://localhost:8888/](http://localhost:8888/))

````sql
SELECT 
    last("longitude") AS "last_longitude", 
    last("latitude") AS "last_latitude" 
FROM 
    "starlink"."autogen"."location"
WHERE 
    time < :desired_timestamp:
GROUP BY "id"
FILL(null) 
````
`:desired_timestamp:` in the format `yyyy-mm-ddTHH:MM:SS.000Z`
