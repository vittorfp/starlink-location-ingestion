import datetime
import json
import time
from pathlib import Path

import influxdb

DB = 'starlink'
FMT = "%Y-%m-%dT%H:%M:%S"
data_path = Path.cwd() / "api-spacex-backend" / "starlink_historical_data.json"

with open(data_path, "r") as f:
    contents = json.load(f)


def format_time(string):
    return int(time.mktime(datetime.datetime.strptime(string, FMT).timetuple()) * 1e6)


data = [
    f"location,id={point['id']} longitude={point['longitude']} "
    f"{format_time(point['spaceTrack']['CREATION_DATE'])}"
    for point in contents
    if point['longitude'] is not None
]

data.extend([
    f"location,id={point['id']} latitude={point['latitude']} "
    f"{format_time(point['spaceTrack']['CREATION_DATE'])}"
    for point in contents
    if point['latitude'] is not None
])

try:

    client = influxdb.InfluxDBClient(host='localhost', port=8086)
    client.create_database(DB)
    client.write_points(data, database=DB, time_precision='u', batch_size=1000000, protocol='line')

except influxdb.exceptions.InfluxDBClientError as e:
    print(json.loads(str(e)[4:])["error"])
