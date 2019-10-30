#!/usr/bin/env python3

import socket
import signal

ips = [
    {
        'ip':"localhost",
        'port':1632
    },
    {
        'ip':"localhost",
        'port':1635
    }
]

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
a = ips.pop()
ip = a['ip']
port = a["port"]
content=''

while True:
    try:
        # Connect to server
        s.connect((ip,port))

        #Asking user for file name
        f_name = input("Enter File name : ")
        s.send(f_name.encode())

        #Fetching file content
        content = ""
        tmp_read = s.recv(1024).decode()
        while "<<EOC>>" not in tmp_read:
            content = content+tmp_read
            tmp_read = s.recv(1024).decode()
        print("[Info] Content in you file: ")
        print(content)

        #Asking user for content
        content = input("Enter content : \n")
        content = content +"<<EOC>>"
        s.send(content.encode())

        # Waiting for successfull write
        if s.recv(1024) ==b'OK':
            print("[+] Succesfully Saved")
        else:
            print("[!] Failed")
        break
    except (ConnectionResetError,ConnectionRefusedError):
        print("Server is closed")
        s.close()
        if(len(ips)>0):
            a = ips.pop()
            ip = a['ip']
            port = a['port']
            print("Trying to send to :",ip,":",port)
            s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            print("No More IPS")
            break
    finally:
        print("Finally Block")
print("I dying my self!!!")
