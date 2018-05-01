import triad_openvr
import time
import sys
import struct
import socket
import csv

try:
    #ipaddress = '10.0.15.81'
    #import configs from csv
    try:
        with open('C:\XYZRealityConfig\Config.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)
                rowStr = row[0]
                if('IPADDRESS' in rowStr):
                    ipaddress = rowStr.split('=', 1)[1]
    except:
        print('CSV error: ')
    
    #port = 51423
    host = 'localhost'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    #server_address = (ipaddress,8052)#('192.168.1.2', 8051)#('10.0.1.48', 8051)
    server_address = (host,8052)#('192.168.1.2', 8051)#('10.0.1.48', 8051)
    v = triad_openvr.triad_openvr()
    v.print_discovered_objects()
    
    if len(sys.argv) == 1:
        interval = 1/250
    elif len(sys.argv) == 2:
        interval = 1/float(sys.argv[0])
    else:
        print("Invalid number of arguments")
        interval = False
 
    if interval:
        
        while(True):
            start = time.time()
            dataToSend = bytearray()
            for d in v.devices: #d in range(len(v.devices)):
                if "tracker" in d or "controller" in d:
                #if "tracker" in d:
                    deviceIndexNum = v.devices[d].index
                    state = v.get_state(deviceIndexNum)
                    trigger = state[1]
                    
                    buttons = 0
                    if(trigger.rAxis[1].x):
                        buttons |= (1<< 0)
                    buttonValue = trigger.ulButtonPressed 
                    if(buttonValue == 4294967296):
                        buttons |= (1<< 1)
                    if(buttonValue == 2):
                        buttons |= (1<< 2)                              
                    if(buttonValue == 4):
                        buttons |= (1<< 3)

                    serialData =  str(buttons) + str(v.devices[d].get_serial())
                    serialDataBytes = bytearray(serialData.encode(encoding='utf_8', errors='strict'))

                    
                    data = v.devices[d].get_pose_matrix()
                    
                    dataBytes = bytes(data)
                    serialDataBytes = serialDataBytes + dataBytes
                    dataToSend = dataToSend + serialDataBytes
            sent = sock.sendto(struct.pack('B'*len(dataToSend), *dataToSend),server_address)
            sys.stdout.flush()
            sleep_time = interval-(time.time()-start)
            if sleep_time>0:
                    time.sleep(sleep_time)
                    #t = str(sendDataArray)
            #print(t, flush=True)
       
except Exception:
    print("PROBLEM in udp_emitter: " + str(Exception))
