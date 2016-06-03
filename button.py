#!/usr/bin/env python
import RPi.GPIO as GPIO
from sparkpost import SparkPost
import os
import requests
import time

# All of your config should be in your ENV variables
fromAddress = os.environ.get('BTNPI_FROM_ADDRESS', None)
toAddress = os.environ.get('BTNPI_TO_ADDRESS', None)
toAnnounce = os.environ.get('BTNPI_TO_ANNOUNCE', None)
subject = os.environ.get('BTNPI_SUBJECT', None)
buttonMessage = os.environ.get('BTNPI_MESSAGE', None)
fqn = os.uname()[1]
r = requests.get('http://wtfismyip.com/json')
startup = "Hello,<br><br>The controller (" + fqn + ") powered on just now.  Is this happening often? Here is the " \
          "external IP for SSH access: " + r.json()['YourFuckingIPAddress']  # THATS THE NAME! I swear

print('Powering controller on...')

trigger = int(time.time())  # Time used to see how long it has been since last button press

try:
    # Connect up to SparkPost
    sparky = SparkPost()

    # Send off the external IP for SSH in the future
    response = sparky.transmissions.send(
        recipients=toAnnounce,
        html=startup,
        from_email=fromAddress,
        subject=subject + ' Controller Power On')

except e:
    print('A mailing error occurred: %s - %s' % (e.__class__, e))
    raise

# Setup the GPIO mode and PIN for 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
print('GPIO set for 16')

# Loop for a button press and try sending a message when the button is pressed
try:
    print 'Trying to enter loop to check for button press'
    while True:
        time.sleep(0.05)  # Maintain a safe distance from button presses
        if GPIO.input(16) == 1:  # it is pushed - just print it
            print('Button pressed time is :')
            print(trigger)
            print(time.time())
        if (GPIO.input(16) == 1) & ((trigger + 3) < (int(time.time()))):
            trigger = int(time.time())
            try:
                print('Time was less then trigger')
                print('Attempting to send email')
                sparky = SparkPost() # Connect up to SparkPost

                # Send off mailbox opened message
                response = sparky.transmissions.send(
                    recipients=[toAddress],
                    html=buttonMessage,
                    from_email=fromAddress,
                    subject=subject)

                print 'Email was sent'
            except e:
                print('A mailing error occurred: %s - %s' % (e.__class__, e))
                raise

except KeyboardInterrupt:
    GPIO.cleanup()
