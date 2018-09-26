#!/usr/bin/python
from flask_cors import CORS
from flask import Flask, Response
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
                 
@app.route("/php/")
def getPlotPHP():
    with open("data.php") as fp:
         php = fp.read()
    return Response(
        php,
        mimetype="text/php",
        headers={"Content-disposition":
                 "attachment; filename=data.php"})


app.run(debug=True)
