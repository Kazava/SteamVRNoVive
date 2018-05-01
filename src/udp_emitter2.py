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
    host = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (ipaddress,8051)#('192.168.1.2', 8051)#('10.0.1.48', 8051)
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
                    serialData =  str(v.devices[d].get_serial())
                    serialDataBytes = bytearray(serialData.encode(encoding='utf_8', errors='strict'))

                    
                    data = v.devices[d].get_pose_matrix()
                    dataBytes = bytes(data)
#                     w=0;
#                     newDataArray = []
#                     for i in range(0,3):
#                         for j in range(0,2):
#                             val = data[i][j]
#                             newData = bytearray(struct.pack("f", val))  
#                             w = w + 1
                        
                    
                    
                    serialDataBytes = serialDataBytes + dataBytes
                    dataToSend = dataToSend + serialDataBytes
                    #trackingDataString = str(data)
                    #sendDataString = '%s' % serialData
                    #sendDataString += ", %s" % trackingDataString
                    
                    #data2 = v.devices[d].get_pose_euler()
                    
                   # sendDataArray = bytes(sendDataString , 'utf-8')
                    #print(sendDataArray)
                    #sent = sock.sendto(struct.pack('B'*len(sendDataArray), *sendDataArray),server_address)
                    
                    #sent = sock.sendto(struct.pack('B'*len(serialDataBytes), *serialDataBytes),server_address)
            sent = sock.sendto(struct.pack('B'*len(dataToSend), *dataToSend),server_address)
            sys.stdout.flush()
            sleep_time = interval-(time.time()-start)
            if sleep_time>0:
                    time.sleep(sleep_time)
                    #t = str(sendDataArray)
            #print(t, flush=True)
       
except Exception:
    print("PROBLEM in udp_emitter: " + str(Exception))
