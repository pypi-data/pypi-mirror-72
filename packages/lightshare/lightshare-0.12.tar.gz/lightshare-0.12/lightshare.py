#!/usr/bin/env python3
import tkinter.filedialog
import os
import socket
import time
from pathlib import Path
from tkinter.filedialog import askopenfile
import sys

def print_(msg,isok,nt):
    """For printing coloured text.
    Takes three aruguments - msg,isok,nt
    For Red on Black - use isok=False; For Green on Black - use isok=True;
    If you are using Windows set nt=True, for others set nt=False; MacOs users, try it, if it doesn't work :( """
    if nt:
        if isok:
            os.system("color 0a")
            print(msg)
        else:
            os.system("color 0C")
            print(msg)
    else:
        if isok:
            os.system("setterm -term linux -back black -fore green && echo \""+str(msg)+"\"")
        else:
            os.system("setterm -term linux -back black -fore red && echo \""+str(msg)+"\"")

def send(file='',host='',port=''):
    """ For sending file. Takes 3 arguments - file, host, port;
    Please specify full path for the file argument, host is the receivers IP Address. You know what port is... plus it's optional."""
    if file=="":
        launch="d"
    else:
        launch="u"
    if os.name=="nt":
        nt=True
    else:
        nt=False
    if file=='':
        root = tkinter.Tk()
        root.wm_withdraw() 
        file_=tkinter.filedialog.askopenfilename()
        if file_=="None" or file_==(None,):
            print_("\n[-] No file selected. Exiting",False,nt)
        root.destroy()
    else:
        pass
    file=os.path.abspath(file_)
    if host=='':
        print_("\n\nEnter IP Displayed on recieving computer :",True,nt)
        host=input()
    else:
        pass
    if port=='':
        port=8075
    else:
        pass
    filesize=os.path.getsize(file)
    fname=Path(file).name
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print_("\n\n[...] Connecting to "+str(host)+" using "+str(port),True,nt)
    try:
        s.connect((host,port))
    except:
        print_("\n[-] Connection Failed...",False,nt)
        time.sleep(5)
        exit(0)
    print_("\n[+] Connected...\n\n",True,nt)
    temp_1=str(fname)+"<SEPERATOR>"+str(filesize)
    temp_b_form=bytes(temp_1,encoding='utf-8')
    s.send(temp_b_form)
    buffersize=524288
    print("\n\n\n")
    with open(file,"rb") as handle:
        x=0
        while True:
            print_("\n\n[...] Sending... ("+str(int((x/filesize)*100))+" %)",True,nt)
            bytes_=handle.read(buffersize)
            if not bytes_:
                break
            s.sendall(bytes_)
            x+=buffersize
    s.close()
    print_("\n\n\n[+] File Sent!",True,nt)
    if launch=='d':
        menu()
    else:
        return

def receive(auto="",port=''):
    """For receiving file. Takes 2 arguments - auto, port;
    You have no use for auto. For my sake and your's forget about it;
    As for port, don't change it unless you have changed the port at the sender."""
    if auto=="n":
        launch="d"
    else:
        launch="u"
    if os.name=="nt":
        nt=True
    else:
        nt=False
    host=[l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    if launch=="d":
        print_("IP Address: "+str(host),True,nt)
    if launch=="d":
        port=8075
        print_("\n\nPort: "+str(port)+"\n\n",True,nt)
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(5)
    if launch=="d":
        print_("[*] Listening as "+str(host)+" on "+str(port),True,nt)
    sender_socket,address=s.accept()
    if launch=="d":
        print_("[+] Got connected to "+str(address)+" ! :) \n\n",True,nt)
    received=sender_socket.recv(4096)
    received=received.decode("utf-8")
    filename,filesize=received.split("<SEPERATOR>")
    filename=os.path.basename(filename)
    filesize=int(filesize)
    BufferSize=262144
    temp=b""
    x=0
    while True:
        bytes_=sender_socket.recv(BufferSize)
        print_("\n\n[...] Receiving... ("+str(int((x/filesize)*100))+" %)",True,nt)
        if not bytes_:
            break 
        temp+=bytes_
        x+=len(bytes_)
    handle=open(filename,"wb")
    handle.write(temp)
    handle.close()
    sender_socket.close()
    s.close()
    if launch=="d":
        print_("\n\n\n[+] File Recieved successfully... Check current directory",True,nt)
        menu()
    else:
        return
 
def menu():
    if os.name=="nt":
        nt=True
    else:
        nt=False
    print('\n\n\n\n \t\tLightshare! V0.12')
    print("\n\n \t\t\tSocket based file transfer program. Made by Nannan. \n\n\n")
    print_("[1]  Receive \n[2]  Send \n[3]  Exit\n\t Enter Option:\n",True,nt)
    ch=int(input())
    if ch<=0 or ch>3:
        print_("\n Enter Proper Option \n\n",False,nt)
        return menu()
    else:
        if ch==2:
            return send()
        elif ch==1:
            return receive(auto="n")
        else:
            return exit(1)    

if __name__=="__main__":
    menu()
