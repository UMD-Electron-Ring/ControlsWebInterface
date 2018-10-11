#!/usr/bin/python
from flask_cors import CORS
from flask import Flask, Response
from updateData import *
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient # aws python iot sdk

# setup AWS IoT Certificate based connection
myMQTTClient = AWSIoTMQTTClient("arn:aws:iot:us-east-1:552138036221:thing/UMER_magnets")
myMQTTClient.configureEndpoint("a134g88szk3vbi-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("keys/root-CA.crt","keys/4986845d81-private.pem.key","keys/4986845d81-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
# Connect and publish
myMQTTClient.connect()
myMQTTClient.publish("UMER_magnets/data", "connected", 0)

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return '''
        <html><body>
        Hello. <a href="/getPlotCSV">Click me.</a>
        </body></html>
        '''

@app.route("/csv/")
def getPlotCSV():
    with open("data.csv") as fp:
         csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=data.csv"})
                 
@app.route("/php/<path>")
def getPlotPHP(path):
    with open("data/"+path+".php") as fp:
         php = fp.read()
    return Response(
        php,
        mimetype="text/php",
        headers={"Content-disposition":
                 "attachment; filename="+path+".php"})

def updateData():
# update webpage
	data = getData()
	createCSV(data)
	createPHP(data)
	print 'Updated: ' + str(datetime.datetime.now())

def logData():
# log data to aws iot
        data = getData()
        nowstr = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        payload = '{ "timestamp": "' + nowstr + '"'
        for magnet,dt in zip(magnets,data):
            payload += ', "'+magnet+'": '+str(dt[3])
        payload+= '}'
        myMQTTClient.publish("UMER_magnets/data", payload, 0)
        print 'published to IoT'
   
scheduler = BackgroundScheduler()
scheduler.add_job(func=updateData, trigger="interval", seconds=UPDATE_TIME)
scheduler.add_job(func=logData, trigger="interval", seconds=60);
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())                 


app.run(debug=True,use_reloader=False)
