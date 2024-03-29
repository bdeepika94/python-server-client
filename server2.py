import os
import socket
import signal
import pickle
from datetime import datetime

def SigHandler(arg1,arg2):
	print("Exiting..")
	exit(0)	

signal.signal(signal.SIGINT,SigHandler)


try:
	os.chdir('server2')
except EOFError:
	print("+[!] File exist or Log file is empty")

s2_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2_sock.bind(("",1632))
s2_sock.listen(2)
while True:
	try:
		# Waiting for client connection
		c_conn,addr=s2_sock.accept()

		#waiting for filename
		f_name = c_conn.recv(1024).decode()

		#Retriving file content
		content = b""
		if os.path.exists(''+f_name):
			with open(f_name,"rb") as fd:
				content = fd.read()
		content = content+b"<<EOC>>"
		
		#sending File content
		c_conn.send(content)
		content =""
		length = len(content)

		#content to be added to file
		tmp_read = c_conn.recv(1024).decode()
		content = content + tmp_read
		while "<<EOC>>" not in tmp_read:
			tmp_read = c_conn.recv(1024).decode()
			content = content + tmp_read
		content = content.replace("<<EOC>>","")		# Removing end of content 

		#writing content to file
		with open(f_name,"a") as fd:
			length = length+fd.write(content)
		c_conn.send(b'OK')

	except (ConnectionResetError,ConnectionRefusedError):

		print("Connection Error")
	
