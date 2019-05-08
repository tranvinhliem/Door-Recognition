import cv2
import numpy as np
import os
import time
import RPi.GPIO as GPIO
from datetime import datetime
import sys
sys.path.append('/home/pi/lcd')
import lcddriver
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


os.system('sudo modprobe bcm2835-v4l2')
flg = True
lock = 27
button = 17
buz = 18
mag = 22
lcd = lcddriver.lcd()

#SYSTEM STARTS
def main():
	recognizer = cv2.face.LBPHFaceRecognizer_create() 
	def boostTrainer():
		recognizer.read('/home/pi/Door/trainer/trainer.yml') 

	t1=threading.Thread(target=boostTrainer,args=())

	start = time.time()
	t1.start()
	t1.join()
	end = time.time()

	print('[INFO] Looking for data') 
	print('[INFO] Reading data') 
	print('[INFO] Time taken in seconds :', end - start)
	cascademodel = "haarcascade_frontalface_default.xml" 
	faceCascade = cv2.CascadeClassifier(cascademodel);
	font = cv2.FONT_HERSHEY_SIMPLEX
	#Initial the level security for check several time of face
	countface=0
	#Initial counter to execute when recognized
	global counter
	counter=0
	#Initial count to execute when can't not recognition
	global clock
	clock=0
	#Iniciate id counter
	id = 0
	# Names related to ids:
	names = ['None', 'Liem']
	# Initialize and start realtime video capture
	cam = cv2.VideoCapture(0) 
	cam.set(3, 640) # set video widht 
	cam.set(4, 480) # set video height
	# Define min window size to be recognized as a face
	minW = 0.1*cam.get(3) 
	minH = 0.1*cam.get(4) 
	print('Start Recognition') 
	lcd.lcd_display_string('Recognition',1)
	lcd.lcd_display_string('Wait for \'Tick\'',2)
	time.sleep(2)
	lcd.lcd_clear()
	while True:
		ret, img =cam.read()
		#img = cv2.flip(img, -1) # Flip vertically
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor = 1.2,
			minNeighbors = 5,
			minSize = (int(minW), int(minH)),
			)
		def send_mail(img):
			detector ='/home/pi/Door/detector'
			filename = 'intruder.jpg'
			cv2.imwrite('detector/intruder.jpg',img)
			user = 'dooralertraspberry@gmail.com'
    			password = 'a58evwck'
   			receiver = 'rintran1307@gmail.com'
    			message = 'Hey! Someone is at home!!!'

    			msg = MIMEMultipart()
    			msg['From'] = user
    			msg['To'] = receiver
    			msg['Subject'] = "REPORTING!"
    			msg.attach(MIMEText(message))

   			 # Attachment
    			file = detector + '/intruder.jpg'
    			attachment = open(file, "rb")

    			part = MIMEBase('application', 'octet-stream')
    			part.set_payload(attachment.read())
    			encoders.encode_base64(part)
    			part.add_header('Content-Disposition', "attachment; filename=%s" % filename)
    			msg.attach(part)

  		  	mail_server = smtplib.SMTP('smtp.gmail.com', 587)
    			mail_server.ehlo()
    			mail_server.starttls()
    			mail_server.ehlo()
    			mail_server.login(user, password)
    			mail_server.sendmail(user, receiver, msg.as_string())
    			mail_server.close()
		for(x,y,w,h) in faces:

		# Check confidence
 			cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
			send_mail(img)
			id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
			confidence =round(100 -confidence)

			if (confidence > 30):
				id = names[id]
				confidence = "{0}%".format(confidence)
				cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255),2)
				cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1,(255,255,0),1)
				print ('Face Recognized')
				print('ID',id)
				print('Confidence',confidence)
				lcd.lcd_display_string('Front of camera',1)
				time.sleep(2)
				countface+=1
				if(countface==3):

					lcd.lcd_clear()
					GPIO.setmode(GPIO.BCM)
					GPIO.setup(lock, GPIO.OUT)
					GPIO.output(lock, GPIO.LOW)
					GPIO.setup(mag, GPIO.IN, GPIO.PUD_UP)

					GPIO.setup(buz, GPIO.OUT)
					GPIO.output(buz, GPIO.HIGH)
					time.sleep(2)
					GPIO.output(buz, GPIO.LOW)
					lcd.lcd_display_string('Face Recognized!',1)
					os.system('echo \"Someone access the Door\" | mail -s \"REPORTING\" rintran1307@gmail.com')
					time.sleep(2)

					lcd.lcd_display_string('Hello! Welcome !',1)
					lcd.lcd_display_string('Open the door',2)
					time.sleep(2)
					lcd.lcd_clear()
					while True:
							GPIO.setup(mag, GPIO.IN, GPIO.PUD_UP)
							if(GPIO.input(mag)==0):
								lcd.lcd_display_string('CLOSED',1)
								time.sleep(3)
								GPIO.setup(lock, GPIO.OUT)
								GPIO.output(lock, GPIO.HIGH)
								GPIO.cleanup()
								history = '/home/pi/Door/history'
								file_name = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
								cv2.imwrite('history/%s.%s.%s.jpg' %(file_name,str(id),str(confidence)),img)
								
								counter +=1
								break

							lcd.lcd_display_string('Door is opened',1)
							lcd.lcd_display_string('Check door again',2)
							time.sleep(2)
							lcd.lcd_clear()
							GPIO.setmode(GPIO.BCM)
							GPIO.setup(buz, GPIO.OUT)
        						GPIO.output(buz, GPIO.HIGH)
        						time.sleep(2)
        						GPIO.output(buz, GPIO.LOW)

				break

			else:
                   		id = "Unknown"
                   		confidence = " {0}%".format(confidence)
                   		countface=0
				cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255),2)
                   		cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1,(255,255,0), 1)
                   		lcd.lcd_display_string("Unrecognized",1)
                   		lcd.lcd_display_string("Please try again",2)
                   		time.sleep(2)
                   		lcd.lcd_clear()
				clock +=1

		if(clock == 3):
			lcd.lcd_display_string('Please Try Again',1)
			break
		if(counter == 1):
			break
		cv2.imshow('camera',img)
		k = cv2.waitKey(10) & 0xff 
		if k == 27 :   #Press 'ESC' for exit program
			break
	cam.release()
	cv2.destroyAllWindows()
#GPIO.cleanup()
while True:
				print('Wait')
				d= time.strftime("%d %b %Y")
				t= time.strftime("%H:%M:%S")
				lcd.lcd_display_string(d,1)
				lcd.lcd_display_string(t,2)
				time.sleep(3)
				lcd.lcd_display_string('Hi There! ^^',1)
				lcd.lcd_display_string('Press the button',2)
				time.sleep(2)
				lcd.lcd_clear()

				GPIO.setmode(GPIO.BCM)
				GPIO.setup(button, GPIO.IN,GPIO.PUD_UP)
				#GPIO.add_event_detect(button, GPIO.FALLING, callback=main, bouncetime=150)

				if (GPIO.input(button)==0):
					GPIO.setmode(GPIO.BCM)
					GPIO.setup(buz,GPIO.OUT)
					GPIO.output(buz,GPIO.HIGH)
					time.sleep(2)
					GPIO.output(buz,GPIO.LOW)
					print('Start Recognition')
					lcd.lcd_display_string('Wait a moment',1)
					lcd.lcd_display_string('Look at camera',2)
					time.sleep(1)
					lcd.lcd_clear()

					main()

				time.sleep(0.5)
