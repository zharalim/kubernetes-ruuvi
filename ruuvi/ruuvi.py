from ruuvitag_sensor.ruuvi import RuuviTagSensor
from ruuvitag_sensor.ruuvi_rx import RuuviTagReactive

from influxdb import InfluxDBClient
from requests.exceptions import ConnectionError

import logging
import time
import signal
import sys
import os

influxdb_client = None
ruuvi_rx = None

def main():
  logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
  logging.info("Initializing...")
  
  global influxdb_client
  global ruuvi_rx

  #influxdb_host = os.environ['INFLUXDB_SERVICE_HOST']
  #influxdb_port = os.environ['INFLUXDB_SERVICE_PORT']

  # Use kubernetes dns
  influxdb_host = 'influxdb'
  influxdb_port = '8086'

  logging.info("Influxdb configured to " + influxdb_host + ":" + influxdb_port)
  influxdb_client = InfluxDBClient(host=influxdb_host, port=influxdb_port, database='ruuvi', timeout=10)
  signal.signal(signal.SIGINT, signal_handler)

  logging.info("Starting RuuviTag listeners...")

  ruuvi_rx = RuuviTagReactive()
  ruuvi_rx.get_subject().subscribe(send_data_to_influxdb)

  logging.info("Initialization done.")
  signal.pause()

def signal_handler(sig, frame):
  global ruuvi_rx

  logging.info('Shutting down...')
  if (ruuvi_rx):
    ruuvi_rx.stop()

  sys.exit(0)

def send_data_to_influxdb(sensor_data): 
  logging.info(sensor_data)

  json_body = [
    {
        "measurement": "ruuvi",
        "tags": {
            "sensor": sensor_data[0],
        },
        "fields": {
            "temperature": sensor_data[1]['temperature'],
            "humidity": sensor_data[1]['humidity'],
            "pressure": sensor_data[1]['pressure'],
            "battery": sensor_data[1]['battery']
        }
    }
  ]
  
  try:
    influxdb_client.write_points(json_body)
  except ConnectionError:
    logging.error("Connecting to influxdb failed")

if __name__ == '__main__':
    main()