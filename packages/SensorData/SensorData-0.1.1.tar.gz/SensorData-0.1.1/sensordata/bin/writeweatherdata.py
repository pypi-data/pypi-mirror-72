
import requests 
import json 
import datetime
from sensordata.classes.database import Vandadatabase

api_key = "7c5b9307552f004743c60d8c72c449f1"
base_url = "http://api.openweathermap.org/data/2.5"
city_name = "Salzburg,AT" 

complete_url = base_url + "/weather?q=" + city_name + "&appid=" + api_key
  
# get json data
response = requests.get(complete_url) 
x = response.json() 

# Check the value of "cod" key  
# "401" wronp API Code
# "404" city is ot found
# "429" used premium service with free account

if x["cod"] != "401" and x["cod"] != "404" and x["cod"] != "429": 
  
  main = x["main"] 
  current_temperature = main["temp"] 
  current_temperature_inC = current_temperature - 273.15
  current_pressure = main["pressure"] 
  current_humidiy = main["humidity"] 
  
  #z = x["weather"] 
  #weather_description = z[0]["description"] 
  
  VandaDB = Vandadatabase()
  currentTSP = datetime.datetime.now()
	
  #insert Temperature
  VandaDB.write_measurement_data(
    sensor_id=3, 
    measured_variable_id=2,
    measurement_date=currentTSP,
    measured_value=current_temperature_inC,
    measurement_unit_id=2)
	
  #insert pressure	
  VandaDB.write_measurement_data(
    sensor_id=3, 
    measured_variable_id=3,
    measurement_date=currentTSP,
    measured_value=current_pressure,
    measurement_unit_id=3)
	
  #insert humidity	
  VandaDB.write_measurement_data(
    sensor_id=3, 
    measured_variable_id=1,
    measurement_date=currentTSP,
    measured_value=current_humidiy,
    measurement_unit_id=1)	
  
else: 
    print(x) 