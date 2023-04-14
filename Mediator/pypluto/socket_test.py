# https://techtutorialsx.com/2018/05/17/esp32-arduino-sending-data-with-socket-client/
# https://docs.ukfast.co.uk/operatingsystems/windows/windowsadministration/netstat.html


# laptop is the server
# netstat -anp | find ":8090" /c
#byte object for python3 

import socket 
import time 

HOST = '10.202.3.68'
PORT = 80

sock = socket.socket()

sock.connect((HOST,PORT))

message = "Hello Dada"
message = bytearray(message,'utf-8')

start = time.time()

print("hi")

sock.send(message)
 
data = ""       
 
while len(data) < len(message):
    data += str(sock.recv(1))
 
print(data)
 
sock.close()

# while True :
#     now = time.time()

#     elapse = now - start 
    
#     if( elapse < 5 ):
#         s.close()
#         time.sleep(1)
#         break
    


#     s.send(message)

#     time.sleep(1)
#     #see the echoing code if needed
    
    

# print("done")