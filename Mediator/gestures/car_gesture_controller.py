import time
from pypluto.pypluto import pluto
#above line req for controlling pluto drone ( not the car)

import socket 

class CarGestureController():
    def __init__(self,HOST='10.202.1.109' , PORT=80 ): 
        self._is_landing = False

        # print(self.CarSocket)

        
        self.Carsocket = socket.socket()
        self.Carsocket.connect((HOST,PORT))

        self.gest_land_stop = 3
        self.message = "N" #for No cmd

        
                

    def gesture_control(self, gesture_buffer):
        gesture_id = gesture_buffer.get_gesture()
        
        if gesture_id == 3 :
            print("GESTURE id is 3 :  ", gesture_id)
            # self._is_landing = not self._is_landing # for pluto drone
            print("is landing") #for pluto drone
            
            

        if not self._is_landing:

            if gesture_id == 0:  # Forward
                self.message = "S"
                
            elif gesture_id == 1:  # STOP
                self.message = "S"

            if gesture_id == 5:  # Back
                self.message = "S"
                

            elif gesture_id == 2:  # UP
                self.message = "F"

            elif gesture_id == 4:  # DOWN
                
                self.message = "B"

            
            elif gesture_id == 3:  # LAND  for pluto drone
                
                self._is_landing = True
                print("\nLanding ")

                self.message = "X" 
                print("land cmd now")
                time.sleep(2)
                

            elif gesture_id == 6: # LEFT
                self.message = "L" 

            elif gesture_id == 7: # RIGHT
                self.message = "R"

            elif gesture_id == -1:#undetected????
                self.message = "N"

            
            
            print(self.message)

            try :
                self.message = bytearray(self.message,'utf-8')
                self.Carsocket.send(self.message)
            except :
                pass
            


