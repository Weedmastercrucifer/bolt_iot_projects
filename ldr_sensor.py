import conf,email_conf,json,time #conf and email_conf contains details of phone numbers api keys etc.
from boltiot import Sms,Bolt,Email
minimum_limit=400
maximum_limit=900
mybolt=Bolt(conf.API_KEY,conf.DEVICE_ID)
sms= Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER) 
mailer=Email(email_conf.MAILGUN_API_KEY, email_conf.SANDBOX_URL,  email_conf.SENDER_MAIL, email_conf.RECIPIENT_MAIL)

while True: 
     print("Reading sensor value")
     response=mybolt.analogRead('A0')
     data=json.loads(response) 
     print("Sensor value is: " +str(data['value'])) 
     try: 
        sensor_value=int(data['value'])
        if sensor_value>maximum_limit or sensor_value<minimum_limit: 
             print("making request to Twilio to send a sms")
             response=sms.send_sms("The current Light intensity sensor value is " +str(sensor_value)) 
             print("Response received from Twilio is :" +str(response)) 
             print("Status of SMS at Twilio is : " +str(response.status))
             print("Making mail request to mailgun")
             respons_e=mailer.send_email("Alert" ," The current light intensity sensor value is " +str(sensor_value))
             response_text=json.loads(respons_e.text)
             print("RESPONSE received is: " +str(response_text['message'])) 
     except Exception as e:
            print("Error occurred below are the details")
            print(e) 
     time.sleep(60)
