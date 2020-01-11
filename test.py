import time
import json
import serial
from pprint import pprint
import random

if __name__ == "__main__":
	
	try :	
		ser  = serial.Serial("COM3", baudrate= 9600, 
			   timeout=2.5, 
			   parity=serial.PARITY_NONE, 
			   bytesize=serial.EIGHTBITS, 
			   stopbits=serial.STOPBITS_ONE
			)
	except Exception as e:
		print (e)
		exit(0)
	data = {}
	data["operation"] = "sequence"
	data["servo_count"] = 3
	data["frame_count"] = 2
	data["frame_speed"] = 300
	data["servo_iteration_speed"] = 5
	data["dimension"]   = 2
	data["loop"]        = 1
	data["frame"] 		= [[45,120,45], [120, 120, 90]]
	
	data=json.dumps(data)
	print (data)
	if ser.isOpen():
		ser.write(data.encode('ascii'))
		ser.flush()
		try:
			pass
			# incoming = ser.readline().decode("utf-8")
			# print (incoming)
		except Exception as e:
			print (e)
			pass
		ser.close()
	else:
		print ("opening error")
		