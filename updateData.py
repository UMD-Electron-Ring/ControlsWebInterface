import requests
import datetime

UPDATE_TIME = 5 # seconds
SERVER = 'http://127.0.0.1:8000/'
magnets = ['H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','H11','H12','H13','H14','H15','H16','H17']
header = ('Magnet','Input Voltage','Output Voltage','Output Current')

def getData():
	data = []
	#data.append(header)
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
	pdata = '<div class="table"></div>'
	for row in data:
		pdata += '<div class="table">'
		for j,item in enumerate(row):
			if j == 0:
				pdata += '<div class="row header">'
				pdata += '<div class="cell">'
				pdata += str(item)
				pdata += '</div>'
				pdata += '</div>'
			else:
				pdata += '<div class="row">'
				pdata += '<div class="cell">'
				# implement future color checks w/ style="background:green"
				pdata += str(item)
				pdata += '</div>'
				pdata += '</div>'				
		pdata += '</div>'
	
	with open('data/data.php', 'w') as f:
		f.write(header+'\n')
		f.write('echo \''+pdata+'\'; \n')
		f.write(footer+'\n')
		
def createPHP2(data):
	header='<?php'
	footer = '?>'
	for i,row in enumerate(data):
		for j,item in enumerate(row):
			if j != 0:
				with open('data/'+magnets[i]+'-'+str(j)+'.php', 'w') as f:
					f.write(header+'\n')
					f.write('echo \''+str(item)+'\'; \n')
					f.write(footer+'\n')
				
	
	
	
	
	
	
	
	
	
	
	


	
