import triad_openvr
import time
import sys
import bitarray

try:
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
            txt = ""
            buttonpress = ""
            for each in v.devices["tracker_1"].get_pose_euler():
                deviceIndexNum = v.devices["tracker_1"].index
                txt += ", %.4f" % each
                state = v.get_state(deviceIndexNum)
                trigger = state[1]
                if(trigger.rAxis[1].x):
                    buttonpress = "1"
                else:
                    buttonpress = "0"
                
                txt += "," + buttonpress + " "
            print("\r" + txt, end="")
            #txt2 = ""
            for each in v.devices["tracker_2"].get_pose_euler():
                deviceIndexNum2 = v.devices["tracker_2"].index
                txt += ", %.4f" % each
                state2 = v.get_state(deviceIndexNum2)
                trigger2 = state2[1]
                buttons = 0
                if(trigger2.rAxis[1].x):
                    buttons |= (1<< 0)
                buttonValue = trigger2.ulButtonPressed 
                if(buttonValue == 4294967296):
                    buttons |= (1<< 1)
                if(buttonValue == 2):
                    buttons |= (1<< 2)                              
                if(buttonValue == 4):
                    buttons |= (1<< 3)

                    
                
                    
                    
                txt += ", %.4f" % each
                txt += " "
            print("\r" + txt, end="")
            sleep_time = interval-(time.time()-start)
            if sleep_time>0:
                time.sleep(sleep_time)
            #buttonpress = ""
            #for i in range(15):
                
            #    state = v.get_state(i)
            #    trigger = state[1]#.rAxis[1].x
            #    if(trigger.rAxis[1].x):
            #        buttonpress = buttonpress + "1"
            #    else:
            #        buttonpress = buttonpress + "0"
            #print(buttonpress)

except:
    print("PROBLEM")