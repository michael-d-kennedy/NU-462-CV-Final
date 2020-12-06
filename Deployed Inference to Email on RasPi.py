import os
import pathlib
from pycoral.utils import edgetpu
from pycoral.utils import dataset
from pycoral.adapters import common
from pycoral.adapters import classify
from PIL import Image
from picamera import PiCamera
from os import system
from time import sleep
import random
from datetime import datetime
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'xxxxx' #change this to match your gmail account
GMAIL_PASSWORD = 'xxxxx'  #change this to match your gmail password
 
 
class Emailer:
    def sendmail(self, recipient, subject, content, openImage):
          
        #Create Headers
        emailData = MIMEMultipart()
        emailData['Subject'] = subject
        emailData['To'] = recipient
        emailData['From'] = GMAIL_USERNAME
        
        #Attach our text data  
        emailData.attach(MIMEText(content))
  
        #Create our Image Data from the defined image
        imageData = MIMEImage(open(openImage, 'rb').read(), 'jpg') 
        imageData.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
        emailData.attach(imageData)
  
        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
  
        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
  
        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, emailData.as_string())
        session.quit
  
sender = Emailer()


# Specify the TensorFlow model, labels, and image
script_dir = pathlib.Path(__file__).parent.absolute()
model_file = os.path.join(script_dir, 'model.tflite')
label_file = os.path.join(script_dir, 'labels.txt')

camera = PiCamera()
camera.resolution = (1944, 1944)
camera.framerate = 15
camera.brightness = 45
camera.contrast = 55
sleep(5)
CurrentDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
current_picture =  CurrentDateTime + '.jpg' #str(datetime.now()) + '.jpg'
camera.capture(current_picture)

image_file = os.path.join(script_dir, current_picture) #'Closed0940.jpg') #'Open0718.jpg')
#Crop the door latch
image_file_latch = Image.open(image_file).crop((1150, 500, 1374, 724))


# Initialize the TF interpreter
interpreter = edgetpu.make_interpreter(model_file)
interpreter.allocate_tensors()

# Resize the image
size = common.input_size(interpreter)
image = image_file_latch.convert('RGB').resize(size, Image.ANTIALIAS)
#image = Image.open(image_file).convert('RGB').resize(size, Image.ANTIALIAS)

# Run an inference
common.set_input(interpreter, image)
interpreter.invoke()
classes = classify.get_classes(interpreter, top_k=1)

# Print the result
labels = dataset.read_label_file(label_file)
for c in classes:
  print('%s: %.5f' % (labels.get(c.id, c.id), c.score))

gate_status = labels.get(c.id, c.id)
gate_cert = c.score

if gate_status == 'Open':
    openImage = image_file
    sendTo = 'xxxxx, xxxxx'
    emailSubject = ""
    emailContent = "OPEN GATE DETECTED with " + str(c.score*100.)[:4] + "% certainty on "  + CurrentDateTime   
    sender.sendmail(sendTo, emailSubject, emailContent, openImage)
    print("Email Sent")    

