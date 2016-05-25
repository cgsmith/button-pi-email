#!/usr/bin/env python
import RPi.GPIO as GPIO
import mandrill
import os
import requests
import time

apikey =  'your-api-key' #mandrill api key
fromemail = 'from@email.com' #from address
tomailbox = 'to@email.com' #email for sending mailbox open alert
toannounce = 'announce@email.com' #announcement email of external IP
subjectname = '[Subject in the email]'
buttonmsg = 'Hello,<br><br>The mailbox button was pressed'
fqn = os.uname()[1]
r = requests.get('http://wtfismyip.com/json')
startup = "Hello,<br><br>The controller (" + fqn + ") powered on just now.  Is this happening often? Here is the external IP for SSH access: " + r.json()['YourFuckingIPAddress'] #THATS THE NAME! I swear

print 'Powering controller on...'

trigger = int(time.time())
try:
  mandrill_client = mandrill.Mandrill(apikey)

  #send off the external IP for SSH in the future 
  message = {
  'from_email': fromemail,
  'to': [{'email':toannounce,'type':'to'}],
  'subject': subjectname + ' Controller Power On',
  'html': startup }

  result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')

except mandrill.Error, e:
  print 'A mandrill error occurred: %s - %s' %  (e.__class__, e)
  raise

GPIO.setmode(GPIO.BOARD) #setup GPIO board
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print 'GPIO set for 16'

try:
    print 'Trying to enter loop to check for button press'
    while True:
        time.sleep(0.05)
        if (GPIO.input(16) == 1):
            print 'Button pressed time is :'
            print trigger
            print time.time()
        if ((GPIO.input(16) == 1) & ((trigger + 3) < (int(time.time())))):
            trigger = int(time.time())
            try:
              print 'Time was less then trigger'
	      print 'Attempting to send email'
              mandrill_client = mandrill.Mandrill(apikey)

              #send off mailbox opened message 
              message = {
                'from_email': fromemail,
                'to': [{'email':tomailbox,'type':'to'}],
                'subject': subjectname,
                'html': buttonmsg 
              }

              result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
              print 'Email was sent'
            except mandrill.Error, e:
              print 'A mandrill error occurred: %s - %s' %  (e.__class__, e)
              raise

except KeyboardInterrupt:
    GPIO.cleanup()

