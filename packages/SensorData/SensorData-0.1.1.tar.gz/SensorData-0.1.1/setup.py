from distutils.core import setup

setup(
    name='SensorData',
    version='0.1.1',
	author='Georg Stocker',
	author_email='georg.stocker@gmail.com',
    packages=['sensordata','sensordata.test','sensordata.classes','sensordata.bin'],
	scripts=['bin/writecpudata.py','bin/writedht22data.py'],
	url='http://pypi.python.org/pypi/SensorData/',
    license='LICENSE.txt',
	description='Storing sensordata in DB',
    long_description=open('README.txt').read(),
	install_requires=[
		'Adafruit_DHT >= 1.4.0',
		'mariadb >= 0.9.59',
		'gpiozero >= 1.5.1'],
)