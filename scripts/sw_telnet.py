#! /usr/bin/env python

# Script para enviar un comando via Telnet a un switch HP

import os, sys, time, select, traceback, smtplib, datetime, argparse, re, telnetlib 

telnet_timeout = 1 

def connect(ipaddress, username, password):
	try:
		#print "Connecting..."
		tn = telnetlib.Telnet(ipaddress)
        	#print "Connecting OK!"
        	try:
        		#print "Authentication..."
			tn.read_until("Username:", telnet_timeout)
			tn.write(username + "\r")
			tn.read_until("Password:", telnet_timeout)
			tn.write(password + "\r")
			tn.write("\r\n")
			output=tn.read_until(">", telnet_timeout)
			#print "Authentication OK!"
			return tn
        	except Exception, e:
			print "ERROR: Incorrect user/password"
			print "Exception: %s" % str(e)
			tn.close()
    	except Exception, e:
        	print "Error connecting to " + ipaddress
        	print "Exception: %s" % str(e) 

def disconnect(tn):
	try:
        	tn.write("\r\n")
        	tn.write("quit\r\n")
		#print "Disconnecting OK"
	except Exception, e:
        	print "Error: connection error or model not supported"
        	print "Exception: %s" % str(e)
    	return True 

def getName(tn):
	name = None
	try:
		output=tn.read_until(">", telnet_timeout)
	except Exception, e:
		print "Error: connection error or model not supported"
		print "Exception: %s" % str(e)
	r = re.compile('<(.*?)>')
	m = r.search(output)
	if m:
		name = m.group(1)
	return name 

def send_command(ipaddress, username, password, cmd):
	tn = connect(ipaddress, username, password)
	prompt = "<%s>" % getName(tn)
	try:
		tn.write("screen-length disable" + "\n")  # Desactiva la paginacion de la terminal y envia la respuesta sin dar espacio.
		tn.write("\r\n")
		time.sleep(0.2) # espera a que tome el comando
                output = tn.read_very_eager()
		cmds_list = cmd.split(",")
		for cmd in cmds_list:
			if ('display' in cmd) or ('dis' in cmd):
				tn.write(cmd + "\r\n")
				time.sleep(0.2) #espera a que tome el comando
				output = tn.read_very_eager()
				print output
			else:
				tn.write(cmd + "\n")
				time.sleep(0.2) #espera a que tome el comando
	except Exception, e:
        	print "Error: connection error or model not supported"
        	print "Exception: %s" % str(e)
	disconnect(tn)
			
def main():
	__author__ = 'jcramirez'
	parser = argparse.ArgumentParser(description='This is a script to send a cli cmd via telnet to a server')
	parser.add_argument('-s','--server', help='Server where the commad will be send',required=True)
	parser.add_argument('-u','--user',help='Valid user in the server', required=True)
	parser.add_argument('-p','--password',help='Valid password for the user', required=True)
	parser.add_argument('-c','--cmd',help='Command to be summited', required=True)
	args = parser.parse_args()
	
	# # show input values ##
	#print ("Server: %s" % args.server )
	#print ("User: %s" % args.user )
	#print ("Password: %s" % args.password)
	#print ("Command: %s" % args.cmd)
	
	send_command(args.server, args.user, args.password,args.cmd)
   
#*****************************************************
#		MAIN 
#*****************************************************
if __name__ == "__main__":
    main ()
