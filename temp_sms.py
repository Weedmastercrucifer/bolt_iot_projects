import conf,json,time #conf contains details of phone numbers api keys etc.
from boltiot import Sms,Bolt
minimum_limit=300
maximum_limit=600
mybolt=Bolt(conf.API_KEY,conf.DEVICE_ID)
sms= Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)
while True: 
     print("Reading sensor value")
     response=mybolt.analogRead('A0')
     data=json.loads(response) 
     print("Sensor value is: " +str(data['value'])) 
     try: 
        sensor_value=int(data['value'])
        if sensor_value>maximum_limit or sensor_value<minimum_limit: 
             print("making request to Twilio to send a sms")
             response=sms.send_sms("The current Temperature sensor value is " +str(sensor_value)) 
             print("Response received from Twilio is :" +str(response)) 
             print("Status of SMS at Twilio is : " +str(response.status)) 
     except Exception as e:
            print("Error occurred below are the details")
            print(e) 
     time.sleep(10)
