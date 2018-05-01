'''
Created on 27 Oct 2017

@author: murray
'''
import BluetoothRFCOMM
import triad_openvr
import struct
import time
import sys

#from bokeh.command.subcommands.file_output import FileOutputSubcommand

#initilise class

bComms = BluetoothRFCOMM.BluetoothRFCOMM()
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
client_sock = bComms.initBluetooth(uuid)
bComms.sendData("PC_Python_Init",client_sock)
#setup tracking
v = triad_openvr.triad_openvr()
v.print_discovered_objects()

button1Debounce = 0
button2Debounce = 0
button3Debounce = 0
button4Debounce = 0
buttonDebounceValue = 10

try:    
    while(True):
        sendDataString = "w"
        dataToSend = bytearray()
        for d in v.devices: 
            if "tracker" in d or "controller" in d:
                deviceIndexNum = v.devices[d].index
                state = v.get_state(deviceIndexNum)
                trigger = state[1]
                
                buttons = 0
                if(trigger.rAxis[1].x):
                    if(button1Debounce == buttonDebounceValue):
                        buttons |= (1<< 0)
                        button1Debounce = 0
                    button1Debounce = buttonDebounceValue + 1
                    
                buttonValue = trigger.ulButtonPressed 
                if(buttonValue == 4294967296):
                    if(button2Debounce == buttonDebounceValue):
                        buttons |= (1<< 1)
                        button2Debounce = 0
                    button2Debounce = buttonDebounceValue + 1
                    
                if(buttonValue == 2):
                    if(button3Debounce == buttonDebounceValue):
                        buttons |= (1<< 2)     
                        button3Debounce = 0
                    button3Debounce = buttonDebounceValue + 1
                                             
                if(buttonValue == 4):
                    if(button4Debounce == buttonDebounceValue):
                        buttons |= (1<< 3)
                        button4Debounce = 0
                    button4Debounce = buttonDebounceValue + 1

                serialData =  str(buttons) + str(v.devices[d].get_serial())
                serialDataBytes = bytearray(serialData.encode(encoding='utf_8', errors='strict'))
                data = v.devices[d].get_pose_matrix()
                dataBytes = bytes(data)
                serialDataBytes = serialDataBytes + dataBytes
                dataToSend = dataToSend + serialDataBytes
        bComms.sendData(struct.pack('B'*len(dataToSend), *dataToSend),client_sock)
        #print(dataToSend)
        sys.stdout.flush()
        time.sleep(0.01)
#                     sleep_time = interval-(time.time()-start)
#                     if sleep_time>0:
#                             time.sleep(sleep_time)   
except:
    print("PROBLEM in send tracking data")
finally:
    print("Application finished")

