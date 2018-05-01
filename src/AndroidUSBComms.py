'''
Created on 23 Oct 2017

@author: murray
'''
import sys
import socket
from bluetooth import *

# s = socket.socket()
# host = socket.gethostname()
# port = 59900
# s.binf((host,port))
# 
# s.listen(5)
# while True:
#     c, addr = s.accept()
#     print ('Got connection', addr)
#     c.send('Thank you for connecting')
#     c.close

#-------------------------- s = socket.socket()         # Create a socket object
#-------------------------- host = socket.gethostname() # Get local machine name
#---------------- port = 12345                # Reserve a port for your service.
#------------------------------------------------------------------------------ 
#------------------------------------------------------- s.connect((host, port))
#------------------------------------------------------------ print s.recv(1024)
#----------------------------------------------------------------------- s.close

# serverMACAddress = '9c:ae:d3:74:5d:07'
# port = 3
# s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# s.connect((serverMACAddress, port))
# while 1:
#     text = "Thank you for connecting"
#     if text == "quit":
#         break
#     s.send(text)
# s.close()

try:
    server_sock= BluetoothSocket( RFCOMM )
    #server_sock= socket.socket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
    
    port = server_sock.getsockname()[1]
    #print("Waiting for connection on RFCOMM channel %d" % port)
    #client_sock, client_info = server_sock.accept()
     
     
     
    
    
    x = 0
    while x<3:
        print( "Waiting for connection on RFCOMM channel %d" % port)
 
        client_sock, client_info = server_sock.accept()
        print( "Accepted connection from ", client_info)
        x = 1
 
        while x == 1:
                try:
                    data = client_sock.recv(1024)
                    if len(data) == 0: break
                    print ("received [%s]" % data)

                    if data == 'temp':
                            data = str("temp")
                    elif data == 'a':
                            data = 'A A A!'
                    elif data == 'b':
                            data = 'B B B'
                    else:
                            data = 'WTF!'
                            x = 5
                    client_sock.send(data)
                    print( "sending [%s]" % data)

                except IOError:
                        pass


except (KeyboardInterrupt):

    print( "disconnected")

    client_sock.close()
    server_sock.close()
    print( "all done")

    #break
