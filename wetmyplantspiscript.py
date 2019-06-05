import requests
import datetime
import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():

        payload = {'Email': 'carter.knutson@oit.edu'}
        r= requests.get('https://wetmyplants.azurewebsites.net/piapi/getuserplants', data=payload)
        plantlist = r.text
        plantlist = plantlist.split('"')
        open('plantIDs.txt', 'w').close()
        with open('/home/pi/plantIDs.txt', 'w') as f:
            for p in plantlist:
                if ":" in p:
                    f.write("%s\n" % p)

        plants = open('plantIDs.txt').readlines()
                            

        for p in plants:
                             
                            os.system ('cd miflora')
                            os.system (' /home/pi/miflora/demo.py --backend gatttool poll' + p + '> /home/pi/flowercare.txt')

                            f = open( '/home/pi/flowercare.txt', 'r' )
                            file = f.read()
                            data = file.split("\n")
                            water = data[4].split(": ")
                            water = water[1]
                            light = data[5].split(": ")
                            light = light[1]
                            payload = {'Id': plantID, 'CurrentLight': light, 'CurrentWater': water}
                            r = requests.post('https://wetmyplants.azurewebsites.net/piapi/updateplant', data=payload)

shed.Start()
