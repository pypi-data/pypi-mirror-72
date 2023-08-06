# Module Imports
import sys
import datetime
from gpiozero import CPUTemperature
from sensordata.classes.database import Vandadatabase

cpu = CPUTemperature()
cputemp = cpu.temperature

#write data not null data to MariaDB 
if cputemp is not None:

    VandaDB = Vandadatabase()
    currentTSP = datetime.datetime.now()
	
	#insert CPU Temperature
    VandaDB.write_measurement_data(
      sensor_id=2, 
      measured_variable_id=2,
      measurement_date=currentTSP,
      measured_value=cputemp,
      measurement_unit_id=2)
	  
else:
    print('Failed to get reading.')
    sys.exit(1)
