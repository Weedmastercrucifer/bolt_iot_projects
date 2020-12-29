import requests    #for making HTTP requests
import json        #library for handling json data
import time        #module for sleep operation
from boltiot import Bolt     #importing Bolt from boltiot module
import conf        #configuration file
mybolt =Bolt(conf.bolt_api_key, conf.device_id)


def get_sensor_value_from_pin(pin):
        """Returns sensor value returns -999 if it fails"""
        try:
           response=mybolt.analogRead(pin)
           data=json.loads(response)
           if data["success"]!=1:
              print("Request Unsuccessful")
              print("Response is ->", data)
              return -999
           sensor_value=int(data["value"])
           return sensor_value
        except Exception as e:
               print("Something went wrong when returning sensor value")
               print(e)
               return -999


def send_telegram_message(message):
    """Sends message via Telegram"""
    url="https://api.telegram.org/" + conf.telegram_bot_id + "/sendMessage"
    data={
          "chat_id":conf.telegram_chat_id,
          "text":message
         }
    try:
       response= requests.request("POST",url,params=data)
       print("This is the Telegram url")
       print(url)
       print("This is the telegram response")
       print(response.text)
       telegram_data=json.loads(response.text)
       return telegram_data["ok"]
    except Exception as e:
           print("An error occurred while sending message")
           print(e)
           return False


while True:
          #Step 1
          sensor_value=get_sensor_value_from_pin("A0")
          print("The current sensor value is:", sensor_value)


          #Step 2
          if sensor_value==-999:
             print("Request was unsuccessful. Pausing")
             time.sleep(10)
             continue


          #Step 3
          if sensor_value>=conf.threshold:  #Set as 250
             print("Sensor value has exceeded threshold")
             message="ALERT!!! SENSOR VALUE HAS EXCEEDED "  + str(conf.threshold) + \
                     ". The current value is  " + str(sensor_value)
             telegram_status=send_telegram_message(message)
             print("The telegram status is :" , telegram_status)


          #Step 4
          time.sleep(10)
