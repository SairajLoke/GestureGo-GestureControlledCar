from pypluto import pluto
import time
#A sample program to test the drone API
drone=pluto()
drone.connect()
#r p t y
drone.trim(0,-10,0,0)
# drone.takeoff()

drone.disarm()
drone.arm()  #remember to arm while using throttle speed anfd not take off
time.sleep(2)
    # drone.takeoff()
# drone.throttle_speed(300,3)
drone.set_all_speed(0,0,300,0,2)
time.sleep(2)
drone.disarm()

# drone.keyboard_control()







