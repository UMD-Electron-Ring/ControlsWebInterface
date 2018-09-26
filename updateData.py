import requests
import time
import datetime

UPDATE_TIME = 5 # seconds
SERVER = 'http://127.0.0.1:8000/'
magnets = ['H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','H11','H12','H13','H14','H15','H16','H17']
header = ('Magnet','Input Voltage','Output Voltage','Output Current')

def getData():
	data = []
	data.append(header)
	for magnet in magnets:
		r3 = requests.get(SERVER+'ReadCurrent/'+magnet)
		r2 = requests.get(SERVER+'ReadVoltage/'+magnet)
		r1 = requests.get(SERVER+'ReadInputVoltage/'+magnet)
		data.append((magnet,r1.json()[0],r2.json()[0],r3.json()[0]))
	return data
	
def createCSV(data):
	with open('data.csv', 'w') as f:
		for row in data:
			line = ''
			for entry in row:
			    line = line + str(entry) + ','
			line = line[:-1]
			f.write(line)
			f.write('\n')

def createPHP(data):
	header='<?php'
	footer = '?>'
	pdata = '<div class="table">'
	for i,row in enumerate(data):
		if i == 0:
			pdata += '<div class="row header">'
		else:
			pdata += '<div class="row">'
		for j,item in enumerate(row):
			pdata += '<div class="cell">'
			pdata += str(item)
			pdata += '</div>'
		pdata += '</div>'
	pdata += '</div>'
	
	with open('data.php', 'w') as f:
		f.write(header+'\n')
		f.write('echo \''+pdata+'\'; \n')
		f.write(footer+'\n')
		
	
while True:
	data = getData()
	createCSV(data)
	createPHP(data)
	print 'Updated: ' + str(datetime.datetime.now())
	time.sleep(UPDATE_TIME)
	
	
	
	
	
	
	
	
	
	
	


	
