import mariadb
import sys
import json
import os

#from sensordata.classes.database import Vandadatabase

class Vandadatabase:

  def __init__(self):
    try:
	  #read config file
      self.script_dir = os.path.dirname(__file__)
      self.file_path = os.path.join(self.script_dir, '../res/config.json')
      with open(self.file_path, 'r') as json_data_file:
        self.data = json.load(json_data_file)
      #connect to database
      self.conn = mariadb.connect(
			user=self.data['mariadb']['user'],
			password=self.data['mariadb']['password'],
			host=self.data['mariadb']['host'],
			port=self.data['mariadb']['port']
      )	  
    except mariadb.Error as e:
      print(f"Error connecting to MariaDB Platform: {e}")
      sys.exit(1)

  def write_measurement_data(
    self, 
	sensor_id, 
    measured_variable_id,
    measurement_date,
    measured_value,
    measurement_unit_id):
    self.measurement_data = self.Measurement_data(self.conn)
    self.measurement_data.insert(sensor_id, measured_variable_id, measurement_date, measured_value, measurement_unit_id)

  class Measurement_data:
    def __init__(self,connection):
      self.mariadbcon = connection	

    def insert(
      self, 
      sensor_id, 
      measured_variable_id,
      measurement_date,
      measured_value,
      measurement_unit_id):
      cur = self.mariadbcon.cursor()
      cur.execute("INSERT INTO test.measurement_data(sensor_id, measured_variable_id, measurement_date, measured_value, measurement_unit_id) VALUES (?, ?, ?,?,?)"
        ,(sensor_id, measured_variable_id, measurement_date, measured_value, measurement_unit_id))

