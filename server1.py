import os
import socket
import pickle
import signal 
from datetime import datetime

def SigHandler(a,vb):
	print("Exiting..")
	exit(0)	

signal.signal(signal.SIGINT,SigHandler)

ips = [
    {
        'ip':"localhost",
        'port':1632
    }
]


def backup_data(my_arr):
    print("[+] Backing data to server2..")
    s2_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2_details = ips.copy().pop()
    print("[+] Connecting to backup server ",s2_details["ip"],":",s2_details["port"])
    s2_sock.connect((s2_details["ip"],s2_details["port"]))
    f_name = my_arr[1]
    print(f_name)
    s2_sock.send(f_name.encode())
    content = ""
    tmp_read = s2_sock.recv(1024).decode()
    while "<<EOC>>" not in tmp_read:
        content = content+tmp_read
        tmp_read = s2_sock.recv(1024).decode()

    print(content)
    content = my_arr[-1]
    content = content +"<<EOC>>"
    s2_sock.send(content.encode())

    if s2_sock.recv(1024) ==b'OK':
        print("[+] Succesfully Saved")
    else:
        print("[!] Failed")


log=[]

try:

    files = list(os.walk('server1'))

    os.chdir('server1')

    if not os.path.exists("server.log"):

        print("Log file doesn't exist")

        with open("server.log","wb") as fp:

            log.append("0000,,,")

            pickle.dump(log,fp)

    with open("server.log","rb") as fp:

        log = pickle.load(fp)

except EOFError:

    print("+[!] File exist or Log file is empty")


s1_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s1_sock.bind(("",1635))

print("[+] Server is online now...")

s1_sock.listen(2)

while True:

    # Client Request
    c_conn,addr = s1_sock.accept()

    #Retriving filename sent from client
    f_name = c_conn.recv(1024).decode()

    #Reading content of the file
    content = b""
    if os.path.exists(''+f_name):
        with open(f_name,"rb") as fd:
            content = fd.read()
    content=content+b"<<EOC>>" #Appending End of Content for  the file content

    print("Content is :",f_name,":",content)

    c_conn.send(content)#Sending file content to server

    content =""
    length = len(content)

    #Reading content to be written to file sent from client
    tmp_read = c_conn.recv(1024).decode()
    content = content + tmp_read
    while "<<EOC>>" not in tmp_read:
        tmp_read = c_conn.recv(1024).decode()
        content = content + tmp_read
    print("Writing conent:",content)
    content = content.replace("<<EOC>>","") #removing End of content

    #writting content to the file
    with open(f_name,"a") as fd:
        length = length+fd.write(content)
    curr_time = datetime.now()

    #Backing up data to backup server
    curr_time = curr_time.strftime("%H%M")
    arr = []
    arr.append(curr_time)
    arr.append(f_name)
    arr.append(str(length))
    arr.append(content)
    log.append(",".join(arr))

    #Starting to backing up content
    try:
        backup_data(arr)
    except (ConnectionResetError,ConnectionRefusedError):
        print("[!] Server 2 is down.")

    c_conn.send(b"OK")

    print("[+] Completed All Transaction")


    



# print(a)

# fp.close()
