'''
Created on 27 Oct 2017

@author: murray
'''
import sys
import socket
import threading
from bluetooth import *
from winerror import ERROR_CLIENT_SERVER_PARAMETERS_INVALID

class BluetoothRFCOMM:
    message = "This is the BluetoothRFCOMM class message"
    client_sock = ""
    #constructor
    def __init__(self):
        print( "BluetoothRFCOMM class created")
    
    
    def initBluetooth(self, uuid):
        try:
            server_sock= BluetoothSocket( RFCOMM )
        
            server_sock.bind(("",PORT_ANY))
            server_sock.listen(1)
            
            advertise_service( server_sock, "BluetoothServer",
                           service_id = uuid,
                           service_classes = [ uuid, SERIAL_PORT_CLASS ],
                           profiles = [ SERIAL_PORT_PROFILE ],)
            
            port = server_sock.getsockname()[1]
            print( "Waiting for connection on RFCOMM channel %d" % port)
            
            client_sock, client_info = server_sock.accept()

            self.client_sock = client_sock
            print( "Accepted connection from ", client_info)
            return client_sock
            #self.threadLock = threading.Lock()

            recieveThread = bluetoothRecieveThread(1,"Recieve Thread 1",client_sock)
            recieveThread.start()
            
            #stringMessage = "Test message from Python PC app"
            #self.sendData(msg=stringMessage)
            
        except (KeyboardInterrupt):
        
            print( "disconnected")
        
            self.client_sock.close()
            server_sock.close()
            print( "all done")
              
    def sendData(self,msg,client_sock):
        try:
            #self. threadLock.acquire()
            client_sock.send(msg) 
            #self.threadLock.release()
        except IOError:
            print( "sendData IO error: ")
        except Exception as e:
            print( "sendData ex error: " + str(e))
    
    def recieveData(self,client_sock):
        try:
            #self. threadLock.acquire()
            data = client_sock.recv(1024)
            if len(data) != 0: 
                        print ("received [%s]" % data)
                        return data
            return ""
            #self.threadLock.release()
        except IOError:
            print( "recieveData IO error: ")
        except Exception as e:
            print( "recieveData ex error: " + str(e))
    
class bluetoothRecieveThread(threading.Thread):
    recieveRun = False
    
    def __init__(self, threadID, name, client_socket):
        try:
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.client_socket = client_socket
            print( "bluetoothRecieveThread init created with ID= " + str(threadID) + " and name= " + name)
        except Exception as e:
            print( "bluetoothRecieveThread init ex error: " + str(e))
             
    def run(self):
  
        try:
            # Get lock to synchronize threads
            
            if not(bluetoothRecieveThread.recieveRun):
                
                bluetoothRecieveThread.recieveRun = True
                while(bluetoothRecieveThread.recieveRun):
                    #BluetoothRFCOMM.threadLock.acquire()
                    data = self.client_socket.recv(1024)
                    #BluetoothRFCOMM.threadLock.release()
                    if len(data) != 0: 
                        print ("received [%s]" % data)
                    
            else:
                    print ("not looking for recieved data")
           
        except IOError:
            print( "bluetoothRecieveThread run IO error: ")
        except Exception as e:
            print( "bluetoothRecieveThread run ex error: " + str(e))

