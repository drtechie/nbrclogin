#!/usr/bin/env python2
#
#A simple script to login to NBRCSERVER
#Created by Dr.Mithun , MMST, IIT Kharagpur
#
import requests
import sys
from xml.dom import minidom
import ConfigParser
import time
#import win32con, win32api,os

URL = 'http://192.168.0.18:8090/httpclient.html'
LIVEURL = 'http://192.168.0.18:8090/live'

#LOGIN
def login():
	config = ConfigParser.ConfigParser()
	config.add_section('login')
	fname = open('.nbrcconfig.conf','r')
	config.readfp(fname)
	# login conf
	USERNAME = config.get('login','USERNAME')
	PASSWORD = config.get('login','PASSWORD')
	t = str(time.time()).split('.')[0]
	# This is the form data that the page sends when logging in
	login_data = {
        'username': USERNAME,
        'password': PASSWORD,
        'mode': '191',
        'producttype':0,
        'a':t
        }
	try:
                r=requests.post(URL, data=login_data)
	except requests.ConnectionError:
                print ('Network Unavailable. Retrying....')
                print ('Connected to NBRC WiFi ?')
                time.sleep(2)
                login()
	statusquery(r.text)
	message(r.text)
	
#LOGOUT
def logout():
	config = ConfigParser.ConfigParser()
	config.add_section('login')
	fname = open('.nbrcconfig.conf','r')
	config.readfp(fname)
	# login conf
	USERNAME = config.get('login','USERNAME')
	PASSWORD = config.get('login','PASSWORD')
	t = str(time.time()).split('.')[0]
	# This is the form data that the page sends when logging out
	login_data = {
        'username': USERNAME,
        'mode': '193',
        'producttype':0,
        'a':t
        }
	r=requests.post(URL, data=login_data)
	statusquery(r.text)
	message(r.text)

#KEEPALIVE
def keepalive():
	config = ConfigParser.ConfigParser()
	config.add_section('login')
	fname = open('.nbrcconfig.conf','r')
	config.readfp(fname)
	# login conf
	USERNAME = config.get('login','USERNAME')
	t = str(time.time()).split('.')[0]
	r=requests.get(LIVEURL+'?mode=192&username='+USERNAME+'&a='+t+'&producttype=0')
	checkalive = ack(r.text)
	if checkalive=='ack':
		#Send request every 160 sec to keep the connection alive
		print ('Connection ALIVE')
		time.sleep(160)
	elif checkalive=='login_again':
		print ('Connection LOST. Logging in again...')
		time.sleep(2)
		login()
    
#STATUS QUERY LIVE/LOGIN    
def statusquery(doc):
	from xml.dom.minidom import parseString
	dom = parseString(doc)
	#retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
	xmlTag = dom.getElementsByTagName('status')[0].toxml()
	#strip off the tag (<tag>data</tag>  --->   data):
	xmlData=xmlTag.replace('<status>','').replace('</status>','')
	xmlData=xmlData.replace('<![CDATA[','').replace(']]>','')
	print ("STATUS : " + xmlData+ "!!")

#SERVER MESSAGE QUERY 
def message(doc):
	from xml.dom.minidom import parseString
	dom = parseString(doc)
	#retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
	xmlTag = dom.getElementsByTagName('message')[0].toxml()
	#strip off the tag (<tag>data</tag>  --->   data):
	xmlData=xmlTag.replace('<message>','').replace('</message>','')
	xmlData=xmlData.replace('<![CDATA[','').replace(']]>','')
	print ("Server Message : " + xmlData+ "!!")	

#LIVE QUERY
def ack(doc):
	from xml.dom.minidom import parseString
	dom = parseString(doc)
	#retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
	xmlTag = dom.getElementsByTagName('ack')[0].toxml()
	#strip off the tag (<tag>data</tag>  --->   data):
	xmlData=xmlTag.replace('<ack>','').replace('</ack>','')
	xmlData=xmlData.replace('<![CDATA[','').replace(']]>','')
	return xmlData

#CREATE CONFIGURATION FILE IF NOT PRESENT
def makefile():
	username = raw_input('Please enter your username :')
	password = raw_input('Please enter your password :')
	file = open('.nbrcconfig.conf', 'w+')
	file.write('[login]\n')
	file.write('USERNAME='+username+'\n')
	file.write('PASSWORD='+password+'\n')
	#make the file hidden
	#win32api.SetFileAttributes('.nbrcconfig.conf',win32con.FILE_ATTRIBUTE_HIDDEN)
	file.close()
	print ('\n\nConfiguration file created. Run program again')
	print ('\nAdd ./path/to/nbrclogin& to .profile in your home folder')
	print ('For logging out run nbrclogout after editing /path/to/nbrclogin')
	print ('Created by Dr.Mithun, MMST, IIT Kharagpur')
	print ('Feedback? Mail to drmithunjames@gmail.com')
	try:
            input= raw_input('Press Enter to continue')
        except NameError:
                pass
	sys.exit()
	
#START
try:				#Check whether 'logout' is an argument
	 (str(sys.argv[1]))
except IndexError:
	try:			#Check whether configuration file is present
		filetry=open('.nbrcconfig.conf')
	except IOError:
                print 'A simple script to login to NBRCSERVER'
                print 'Written in Python, Compiled using PyInstaller'
		print '\n\nConfiguration file does not exist'
		print 'First run? Lets configure your username and password'
		print 'This will create a configuration file(.nbrcconfig.conf)\nin the current directory\n\n'
		print 'BE AWARE that the configuration file containing your credentials\nis kept HIDDEN but is still accessible(if someone views hidden files).'
		print 'You have been warned ! \n'
		makefile()
	else:
		login()
else:	
		if str(sys.argv[1])=='logout':
				logout()
				sys.exit()
while True:
	keepalive()
