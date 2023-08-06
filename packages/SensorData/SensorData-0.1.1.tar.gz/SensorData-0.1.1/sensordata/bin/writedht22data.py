# Module Imports
import sys
import datetime
import Adafruit_DHT
from sensordata.classes.database import Vandadatabase

# Sensordefinition
sensor = Adafruit_DHT.DHT22
pin = 4
#get Sensordata
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

#write data not null data to MariaDB 
if humidity is not None and temperature is not None:

    VandaDB = Vandadatabase()
    currentTSP = datetime.datetime.now()
	
	#insert Humidity data
    VandaDB.write_measurement_data(
      sensor_id=1, 
      measured_variable_id=1,
      measurement_date=currentTSP,
      measured_value=humidity,
      measurement_unit_id=1)
	  
	#insert Temperature data
    VandaDB.write_measurement_data(
      sensor_id=1, 
      measured_variable_id=2,
      measurement_date=currentTSP,
      measured_value=temperature,
      measurement_unit_id=2)
	  
else:
    print('Failed to get reading.')
    sys.exit(1)
	
	