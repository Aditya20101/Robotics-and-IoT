
# Python3 script to interface basic Blynk rest API with Raspberry PI

import RPi.GPIO as GPIO
import time


import requests

token="<Enter your token here>"

class AlphaBot(object):
	
	def __init__(self,in1=12,in2=13,ena=6,in3=20,in4=21,enb=26):
		self.IN1 = in1
		self.IN2 = in2
		self.IN3 = in3
		self.IN4 = in4
		self.ENA = ena
		self.ENB = enb

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.IN1,GPIO.OUT)
		GPIO.setup(self.IN2,GPIO.OUT)
		GPIO.setup(self.IN3,GPIO.OUT)
		GPIO.setup(self.IN4,GPIO.OUT)
		GPIO.setup(self.ENA,GPIO.OUT)
		GPIO.setup(self.ENB,GPIO.OUT)
		#self.forward()
		self.PWMA = GPIO.PWM(self.ENA,500)
		self.PWMB = GPIO.PWM(self.ENB,500)
		self.PWMA.start(100)
		self.PWMB.start(100)

	def forward(self):
		GPIO.output(self.IN1,GPIO.HIGH)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.HIGH)

	def stop(self):
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.LOW)

	def backward(self):
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.HIGH)
		GPIO.output(self.IN3,GPIO.HIGH)
		GPIO.output(self.IN4,GPIO.LOW)

	def left(self):
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.HIGH)

	def right(self):
		GPIO.output(self.IN1,GPIO.HIGH)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.LOW)
		
	def setPWMA(self,value):
		self.PWMA.ChangeDutyCycle(value)

	def setPWMB(self,value):
		self.PWMB.ChangeDutyCycle(value)	
		
	def setMotor(self, left, right):
		if((right >= 0) and (right <= 100)):
			GPIO.output(self.IN1,GPIO.HIGH)
			GPIO.output(self.IN2,GPIO.LOW)
			self.PWMA.ChangeDutyCycle(right)
		elif((right < 0) and (right >= -100)):
			GPIO.output(self.IN1,GPIO.LOW)
			GPIO.output(self.IN2,GPIO.HIGH)
			self.PWMA.ChangeDutyCycle(0 - right)
		if((left >= 0) and (left <= 100)):
			GPIO.output(self.IN3,GPIO.HIGH)
			GPIO.output(self.IN4,GPIO.LOW)
			self.PWMB.ChangeDutyCycle(left)
		elif((left < 0) and (left >= -100)):
			GPIO.output(self.IN3,GPIO.LOW)
			GPIO.output(self.IN4,GPIO.HIGH)
			self.PWMB.ChangeDutyCycle(0 - left)

Alpha = AlphaBot()




def write(token,pin,value):
	api_url = "https://blynk.cloud/external/api/update?token="+token+"&"+pin+"="+value
	response = requests.get(api_url)
	if "200" in str(response):
		print("Value successfully updated")
	else:
		print("Could not find the device token or wrong pin format")

def read(token,pin):
	api_url = "https://blynk.cloud/external/api/get?token="+token+"&"+pin
	response = requests.get(api_url)
	return response.content.decode()

# Example: write the virtual PIN v1 to set it to 100:
#write(token,"v1","150")

# Example: read a virtual PIN and print it on shell


while True:
	

	leftB=int(read(token,"v4"))
	
	rightB=int(read(token,"v5"))
	

	forwardB=int(read(token,"v6"))
	

	backwardB=int(read(token,"v7"))
	

	stopB = int(read(token,"v8"))
	  
	if  stopB ==255:
		Alpha.stop()
	
	elif leftB ==255:
		Alpha.left()
		
		
	elif rightB==255:
		Alpha.right()
		
		
	elif forwardB==255:
		Alpha.forward()
		
		
	elif backwardB==255:
		Alpha.backward()	
		
	else:
		Alpha.stop()
		
	print(f"left-{leftB}  right-{rightB}  forward-{forwardB}  backward-{backwardB}  stop-{stopB}")

