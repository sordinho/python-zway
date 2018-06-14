"""
Created on Apr 4, 2014
Updated on May 16, 2018

@author: Dario Bonino
@author: Luigi De Russis

Copyright (c) 2014-2018 Dario Bonino and Luigi De Russis

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License
"""

import rest
import time


def isUserAtHome():
	# the base url
	base_url = 'http://192.168.0.202:8083'

	# login credentials
	username = 'admin'
	password = 'ami-zwave'

	# get z-wave devices
	all_devices = rest.send(url=base_url + '/ZWaveAPI/Data/0', auth=(username, password))

	# clean up all_devices dictionary
	all_devices = all_devices['devices']
	# remove the Z-Way controller from the device list
	all_devices.pop('1')

	# "prototype" and base URL for getting/setting device properties
	device_url = base_url + '/ZWaveAPI/Run/devices[{}].instances[{}].commandClasses[{}]'

	# every device has an ID ==> dobbiamo trovare id del sensore di movimento dal sito
	# ogni sensore può avere diverse instances, ad esempio il 4 in 1 ne avra 4, sono le diverse cose che può fare
	# ogni istance ha una command class, che specifica le feature del device:

	# sensore di movimento
	motion_sensor_id = None  # id del nostro sensore
	sensor_binary = '48'  # (command class) per il movimento

	# search for devices to be "operated", in this case power outlets, temperature, and motion sensors
	for device_key in all_devices:
		# iterate over device instances
		for instance in all_devices[device_key]['instances']:
			# search for the SensorBinary (48) command class, e.g., for motion
			if sensor_binary in all_devices[device_key]['instances'][instance]['commandClasses']:
				# debug
				print('Device %s is a sensor binary' % device_key)
				# get motion
				url_to_call = device_url.format(device_key, instance, sensor_binary)
				# info from devices is in the response
				response = rest.send(url=url_to_call, auth=(username, password))
				val = response['data']['1']['level']['value']
				print('Motion: ' + str(val))
				return val

# per includere un dispositivo premere 3 volte veloce il tasto.
# se non posso includere, provare prima a escludere
# se ci sono 10 sensori di movimento collegati dobbiamo riconoscere il nostro => cerchiamo id del nostro sensore e facciamo check solo di quello
