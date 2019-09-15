# HikBell
Doorbell running on Raspberry Pi 3B+ that is using:
* Hikvision camera for: image, sound notification and communication.
* Google Home for indoor notificatication.
* Pushbullet for mobile notification.

#Insallation

<code>sudo apt-get install update</code>

<code>sudo apt-get install python</code>

<code>sudo apt-get install wget</code>

<code>sudo apt-get install shutil</code>


<code>sudo apt-get install python3</code>

<code>sudo python3 -m pip install pychromecast</code>

#Auto start

<code>sudo nano /etc/rc.local</code>

<code>/usr/bin/sudo /usr/bin/python /home/pi/doorbell.py > /home/pi/doorbell.log 2>&1 &</code>

<code>/usr/bin/sudo /usr/bin/python3 /home/pi/GooglePyNotify.py > /home/pi/GooglePyNotify.log 2>&1 &</code>

#GooglePyNotify
Test: http://<ip>/Notify?<message>