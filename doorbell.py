#coding=utf-8
#author: Fredrik Tell
from pushbullet import Pushbullet
import wget
import shutil
import time
from datetime import datetime
import RPi.GPIO as GPIO
import requests
import threading
import sys

pb_channel_name = "lerkil"
pb_api_key = "o.9NgIOV3yKFrMALNXKwFlPjlU2s2T02yd"
cameraImageUrl = "http://admin:mannaviken6@192.168.1.205/ISAPI/Streaming/channels/101/picture"
cameraTwoWayUrl = "http://admin:mannaviken5@192.168.1.205/ISAPI/System/TwoWayAudio/channels/1/audioData"
google_home_url = 'http://127.0.0.1/Notify?Doorbell'
message = "Visitor at the front door"
outputFolder = "/home/pi/picture.jpg"
GPIO_Pin = 5
GPIO_Steady = 2000

pb = Pushbullet(pb_api_key)
pb_channel = pb.get_channel(pb_channel_name)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_Pin, GPIO.IN)

#Send sound to Google Home
def GoogleHomeNotice():
    try:
        requests.get(google_home_url)
    except:
        print("ERROR - Can't send sound to Google Home")

#Send Pushbullet with image
def PushbulletNotice():
    #Get image from camera and replace the old one
    filename = wget.download(cameraImageUrl, out=outputFolder)
    shutil.move(filename, outputFolder)
    filename = outputFolder
    
    #Upload image to Pushbullet server
    with open(filename, "rb") as pic:
        file_data = pb.upload_file(pic, "picture.jpg")
        
    #Get current time
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y-%m-%d %H:%M")
    
    #Publish notification
    pb_channel.push_file(body=date_time, title=message, **file_data)
    
#Send sound to Hikvision IP camera
def DoorbellSpeakerNotice():
    headers = {'content-type': 'application/binary'}
    data = open('output.ulaw')
    requests.put(cameraTwoWayUrl, headers=headers, data=data)

#Button event
def Doorbell(channel):
    #Google Home notice
    GoogleHomeNoticeThread = threading.Thread(target=GoogleHomeNotice)
    GoogleHomeNoticeThread.start()
    
    #Pushbullet notice
    PushbulletNoticeThread = threading.Thread(target=PushbulletNotice) 
    PushbulletNoticeThread.start()
    
    #DoorbellSpeaker notice
    DoorbellSpeakerNoticeThread = threading.Thread(target=DoorbellSpeakerNotice) 
    DoorbellSpeakerNoticeThread.start()
    

GPIO.add_event_detect(GPIO_Pin, GPIO.FALLING, callback=Doorbell, bouncetime=GPIO_Steady)
print("Doorbell is started")
while True:
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print("Thanks for this time!")
        sys.exit()
