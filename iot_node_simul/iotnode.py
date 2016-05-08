#!/usr/bin/env python 

import socket
import select
import time
import sys
import re 

TCP_IP = '127.0.0.1'
TCP_PORT = 10001
BUFFER_SIZE = 100

CAPS_MESSAGE = "<MSGTYPE:CAPS><MYID:Abhic2><CAPS:TYPE=SWITCH,ID=SW1>"
HELLO_MESSAGE = "<MSGTYPE:HELLO><Hello Gateway>"

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
s.connect((TCP_IP, TCP_PORT))
s.send(CAPS_MESSAGE)

inputs = [ s ]
outputs = [ ] 
excep = [ s ]

message_q = [ ]

while 1: 
    if  (len(inputs) == 0) and (len(outputs)==0) and  (len(excep)==0):
        print '\n------NOTHING TO DO. BYE------------'
        break
    print '\nWaiting for data...'
    readable,writable,exceptional = select.select(inputs,outputs,excep)
    for i in readable:
        if i is s:
            print '\nGot Message from Server' 
            data = i.recv(1024)
            if data:
                print '\nReceived data is %s from %s' % (data , i.getpeername())            
                match = re.match( r'<MSGTYPE:(.*)>(<.*>)', data, re.M|re.I)
                if match: 
                    print 'Message type is %s Message is %s' % (match.group(1),match.group(2))
                    if match.group(1) == 'HELLO':
                        outputs.append(i)
                        message_q.append(HELLO_MESSAGE) 
            else: 
                print '\nConnection closed by Server'
                i.close()
                if i in inputs: 
                    print 'Removing Socket from inputs list'
                    inputs.remove(i)
                if i in excep:
                    print 'Removing Socket from exceptions list'
                    excep.remove(i)
                if i in outputs:
                    print 'Removing Socket from outputs list'
                    excep.remove(i)
    for i in outputs:
        fd = outputs.pop()
        msg = message_q.pop()
        fd.send(msg)


