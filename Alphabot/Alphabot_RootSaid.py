#code for alphabot kit with Raspberry Pi consisting of features like-
#remote control from an android application(Rootsaid); real-time camera feed, RGB lights.
import RPi.GPIO as GPIO
import time
import socket
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import cv2
import numpy
import picamera
from picamera.array import PiRGBArray
from picamera import PiCamera


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


redPin = 24
gndPin = 23
greenPin = 5
bluePin = 18
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)

pR = GPIO.PWM(redPin, 256)
pG = GPIO.PWM(greenPin,256)
pB = GPIO.PWM(bluePin, 256)

    
pR.start(0)
pG.start(0)
pB.start(0)

Alpha = AlphaBot()
UDP_IP = "0.0.0.0"
UDP_PORT = 5050

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
stream = camera.capture_continuous(rawCapture,format="bgr", use_video_port=True)


#while True:
# capture frames from the camera
for frame in stream:

	image = frame.array

	# show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)


	# if the `q` key was pressed, break from the loop and close display window
	if key == ord("q"):
		cv2.destroyAllWindows()
		break

	data,rcv =sock.recvfrom(1024)
	raw = data.decode('ASCII')

	print(raw)
	if  raw =='stop':

		Alpha.stop()
		pR.ChangeDutyCycle(0)
		pG.ChangeDutyCycle(0)
		pB.ChangeDutyCycle(0)

	elif raw=='left':
		Alpha.left()
		pR.ChangeDutyCycle(0)
		pG.ChangeDutyCycle(0)
		pB.ChangeDutyCycle(100)


	elif raw=='right':
		Alpha.right()
		pR.ChangeDutyCycle(0)
		pG.ChangeDutyCycle(0)
		pB.ChangeDutyCycle(100)


	elif raw == 'forward':

		Alpha.forward()
		pR.ChangeDutyCycle(0)
		pG.ChangeDutyCycle(100)
		pB.ChangeDutyCycle(0)


	elif raw == 'backward':
		Alpha.backward()
		pR.ChangeDutyCycle(100)
		pG.ChangeDutyCycle(0)
		pB.ChangeDutyCycle(0)
			

	else:
		Alpha.stop()
		pR.ChangeDutyCycle(0)
		pG.ChangeDutyCycle(0)
		pB.ChangeDutyCycle(0)

