#!/usr/bin/python
from flask_cors import CORS
from flask import Flask, Response
from updateData import *
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

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
	data = getData()
	createCSV(data)
	createPHP(data)
	print 'Updated: ' + str(datetime.datetime.now())
	                 
scheduler = BackgroundScheduler()
scheduler.add_job(func=updateData, trigger="interval", seconds=UPDATE_TIME)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())                 


app.run(debug=True,use_reloader=False)
