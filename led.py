import RPi.GPIO as IO          

import time                            

IO.setwarnings(False)          

IO.setmode (IO.BCM)      

IO.setup(19,IO.OUT)         

p = IO.PWM(19,100)        
p.start(0)  

while 1:                              

    for x in range (30):               
        p.ChangeDutyCycle(x)           
        time.sleep(0.2)
	print x                
      
    for x in range (30):               
        p.ChangeDutyCycle(30-x)        
        time.sleep(0.2)                
	print 30-x

