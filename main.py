from machine import Pin
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from rotary_irq_rp2 import RotaryIRQ
import utime
import AD9833


#OLED display config
WIDTH =128 
HEIGHT= 64
i2c=I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

#AD9833 config
ad9833 = AD9833.AD9833(sdo = 11, clk = 10, cs = 9,  fmclk = 25)

#set I/P and O/P
ok = Pin(4, mode=Pin.IN, pull=Pin.PULL_UP)
ok1 = Pin(5, mode=Pin.IN, pull=Pin.PULL_UP) #encorder push
menu = Pin(3, mode=Pin.IN, pull=Pin.PULL_UP)
home = Pin(2, mode=Pin.IN, pull=Pin.PULL_UP)
A0 = Pin(18, mode=Pin.IN, pull=Pin.PULL_UP)
A1 = Pin(19, mode=Pin.IN, pull=Pin.PULL_UP)
A2 = Pin(20, mode=Pin.IN, pull=Pin.PULL_UP)
GS = Pin(21, mode=Pin.IN, pull=Pin.PULL_UP)
rotary = RotaryIRQ(7, 6, pull_up=True) #r encorder

green =Pin(25,Pin.OUT)
red =Pin(24,Pin.OUT)

#variables
home_count =0
menu_count =0
switch_count =0
switch_count =0
freq_count = 0
current_val = 0 
smode ='SIN'
range ='Hz'
global sfreq
sfreq = 1000
sphase = 0
new_val =0
X = 0
Y = 0
Z = 0
C = 0
count1 = 0
count2 =0
frequency =0
starting=1
#off all led's
green.value(0)
red.value(0)

#delay
delay=.3
delay1=.05

def phase(sphase,new_val, current_val,Z):       
        current_val = 0
        oled.fill(0)
        oled.text("Phase in Deg:-", 10, 10)
        oled.text("PHASE", 47, 55)
        oled.text(">>OK ", 10, 45)
        oled.text(">> ", 110, 30)
        oled.text("<< ", 0, 30)
        oled.text(str(Z), 55, 30)
        oled.show() 
        while True:                
            if ok.value()==0 or ok1.value()==0:
                oled.fill(0)
                sphase = Z
                green.value(1)
                utime.sleep(delay1)
                green.value(0)
                utime.sleep(delay1)
                menu_count=0
                home_count=0
                switch_count=0
                return sphase
                                        
            new_val = rotary.value()
            if current_val != new_val:
                if Z >=360:
                    Z=0
                
                if current_val > new_val:
                    current_val = new_val
                    Z -=30
                    if Z < 0:
                        Z=0
                    print('Zvalue=' ,Z)
                        
                        
                if current_val < new_val:
                    current_val = new_val
                    Z +=30
                    print("Z value=",Z)
                    
                oled.fill(0)
                oled.text("Phase in Deg:-", 10, 10)
                oled.text("PHASE", 47, 55)
                oled.text(">>OK ", 10, 45)
                oled.text(">> ", 110, 30)
                oled.text("<< ", 0, 30)
                oled.text(str(Z), 55, 30)
                oled.show()      
                print('Encoder value:', Z)
                current_val = new_val    

def modes(smode,new_val, current_val,Y,C):
        smode='SIN' 
        current_val = 0
        oled.fill(0)
        oled.text("Waveform:-", 10, 10)
        oled.text("MODE", 50, 55)
        oled.text(">>OK ", 10, 45)
        oled.text(">> ", 110, 30)
        oled.text("<< ", 0, 30)
        oled.text(str(smode), 55, 30)
        oled.show()
        C=55
        while True:                
            if ok.value()==0 or ok1.value()==0:
                oled.fill(0)
                if Y ==360:
                    Y=0
                    smode='SIN'
                green.value(1)
                utime.sleep(delay1)
                green.value(0)
                utime.sleep(delay1)
                menu_count=0
                home_count=0
                switch_count=0
                return smode
        
                
                
            new_val = rotary.value()
            if current_val != new_val:
                if Y >=3:
                    Y=0
                    smode='SIN'
                    C=55
                if Y ==2:
                    smode='TRIANGLE'
                    C=32
                if Y ==1:
                    smode='SQUARE'
                    C=42
                
                if current_val > new_val:
                    current_val = new_val
                    Y -=1
                    if Y < 1:
                        Y=1
                    print('Yvalue=' ,Y)
                        
                        
                if current_val < new_val:
                    current_val = new_val
                    Y +=1
                    print("Y value=",Y)
                    
                oled.fill(0)
                oled.text("Waveform:-", 10, 10)
                oled.text("MODE", 50, 55)
                oled.text(">>OK ", 10, 45)
                oled.text(">> ", 110, 30)
                oled.text("<< ", 0, 30)
                oled.text(str(smode), C, 30)
                oled.show()      
                print('Encoder value:', Y)
                current_val = new_val  

def freqq(sfreq,new_val, current_val,X):   
    while True:
        oled.fill(0)
        oled.text("FREQUENCY", 30, 55)
        oled.text("B1 to +/- 1", 10, 22)
        oled.text("B2 to +/- 0.05", 10, 32)
        oled.text("Press:- ", 10, 10)
        oled.text(">>OK ", 10, 45)
        oled.show()         
                
        if ok.value()==0 or ok1.value()==0:
            oled.fill(0)
            if X < 0:
                X=0
            sfreq = X *1000
            green.value(1)
            utime.sleep(delay1)
            green.value(0)
            utime.sleep(delay1)
            menu_count=0
            home_count=0
            switch_count=0
            return sfreq
        
        if A0.value() ==1 and A1.value() ==0 and A2.value() ==0: #B1
            current_val = 0          
            oled.fill(0)
            oled.text("Value in KHz:- ", 10, 10)
            oled.text("FREQUENCY", 30, 55)
            oled.text("<<FREQ ", 10, 45)
            oled.text(">> ", 110, 30)
            oled.text("<< ", 0, 30)
            oled.text(str(X), 55, 30)
            oled.show()      
            print('Encoder value:', X)
            
            while True: #+-1
                if ok1.value()==0:
                    if X < 0:
                        X=0 
                    utime.sleep(delay)
                    break                
                
                new_val = rotary.value()
                if current_val != new_val:                    
                    if current_val > new_val:
                        current_val = new_val
                        X -=1
                        if X < 0:
                            X=0
                        print('Xvalue=' ,X)
                                                
                    if current_val < new_val:
                        current_val = new_val
                        X +=1
                        print("X value=",X)
                    
                    if X <= 0:
                        X=0
                    X = round(X,2)    
                    oled.fill(0)
                    oled.text("Value in KHz:- ", 10, 10)
                    oled.text("FREQUENCY", 30, 55)
                    oled.text("<<FREQ ", 10, 45)
                    oled.text(">> ", 110, 30)
                    oled.text("<< ", 0, 30)
                    oled.text(str(X), 55, 30)
                    oled.show()      
                    print('Encoder value:', X)
                    current_val = new_val
                
        if A0.value() ==0 and A1.value() ==0 and A2.value() ==0: #B2
            current_val = 0        
            oled.fill(0)
            oled.text("Value in KHz:- ", 10, 10)
            oled.text("FREQUENCY", 30, 55)
            oled.text("<<FREQ ", 10, 45)
            oled.text(">> ", 110, 30)
            oled.text("<< ", 0, 30)
            oled.text(str(X), 50, 30)
            oled.show()      
            print('Encoder value:', X)
            while True: #+-0.05
                if ok1.value()==0:
                    utime.sleep(delay)
                    break
                
                new_val = rotary.value()
                if current_val != new_val:
                    if X < 0:
                        X=0  
                    if current_val > new_val:
                        current_val = new_val
                        X -=0.05
                        if X < 0:
                            X=0
                        print("X value=",X)                        
                        
                    if current_val < new_val:
                        current_val = new_val
                        X +=0.05
                        print("X value=",X)
                    
                    X = round(X,2)
                    oled.fill(0)
                    oled.text("Value in KHz:- ", 10, 10)
                    oled.text("FREQUENCY", 30, 55)
                    oled.text("<<FREQ ", 10, 45)
                    oled.text(">> ", 110, 30)
                    oled.text("<< ", 0, 30)
                    oled.text(str(X), 50, 30)
                    oled.show() 
                    print('Encoder value:', new_val)
                    current_val = new_val                
                                 
#interrupt function
def button_isr(pin):
    if home.value() == 0:
      global home_count
      home_count += 1
    elif menu.value() == 0:
      global menu_count
      menu_count += 1
    elif GS.value() == 0:
        if A0.value() ==0 and A1.value() ==1 and A2.value() ==0: #switch
            global switch_count
            switch_count += 1          
try:
    while True:
        count_old = 0
        home.irq(trigger=Pin.IRQ_FALLING,handler=button_isr)  #interrupts
        menu.irq(trigger=Pin.IRQ_FALLING,handler=button_isr)
        GS.irq(trigger=Pin.IRQ_FALLING,handler=button_isr)
        new_val = rotary.value()
        if starting != count_old:
            oled.fill(0)
            oled.text("WELCOME", 35, 30)
            oled.show()
            utime.sleep(1)
            starting=0
            menu_count=1
                    
        if switch_count != count_old: #HOLD function
            while True:
                if menu_count!= count_old or ok1.value()==0:
                    switch_count=0
                    red.value(0)
                    green.value(1)
                    utime.sleep(delay1)
                    green.value(0)
                    utime.sleep(delay1)
                    menu_count=1
                    break
                ad9833.set_frequency(0,0)
                ad9833.set_mode('OFF')
                ad9833.set_phase(0, 0, rads = False)
                oled.fill(0)
                oled.text("HOLD", 80, 10)
                oled.show()
                red.value(1)

        if home_count!= count_old:
            while True:
                 if menu_count!= count_old or ok1.value()==0 :
                    home_count=0
                    green.value(1)
                    utime.sleep(delay1)
                    green.value(0)
                    utime.sleep(delay1)
                    switch_count=0
                    menu_count=1
                    break
                 oled.fill(0)
                 oled.text("Powered by", 10, 10)
                 oled.text("RP2040", 75, 20)
                 oled.text("+ Micropython", 10, 30)
                 oled.text("+ UI V1.0", 10, 40)
                 oled.text("+ ANKS", 10, 50)
                 oled.show()        
            
        if menu_count != count_old: 
                 oled.fill(0)
                 sfreq = round(sfreq,1)
                 oled.text("FREQUENCY-", 0, 10)
                 oled.text(str(sfreq), 47, 27)
                 oled.text(str(range), 110, 27)
                 oled.text("+ MODE-", 0, 45)
                 oled.text(str(smode), 60, 45)
                 oled.text("+ PHASE-", 0, 55)
                 oled.text(str(sphase), 70, 55)
                 oled.text("Deg", 100, 55)
                 oled.show()
                 print(sfreq)
                 while True:
                        if home_count!= count_old :
                            menu_count=0
                            break
                        if switch_count != count_old:
                            menu_count=0
                            break
                        
                        if A0.value() ==1 and A1.value() ==1 and A2.value() ==0: #Offset
                            sphase= phase(sphase,new_val, current_val,Z)
                            oled.fill(0)
                            oled.text("FREQUENCY-", 0, 10)
                            oled.text(str(sfreq), 47, 27)
                            oled.text(str(range), 110, 27)
                            oled.text("+ MODE-", 0, 45)
                            oled.text(str(smode), 60, 45)
                            oled.text("+ PHASE-", 0, 55)
                            oled.text(str(sphase), 70, 55)
                            oled.text("Deg", 100, 55)
                            oled.show()
                            print(str(sphase))
                        if A0.value() ==0 and A1.value() ==0 and A2.value() ==1: #mode  
                            smode= modes(smode,new_val, current_val,Y,C)
                            oled.fill(0)
                            oled.text("FREQUENCY-", 0, 10)
                            oled.text(str(sfreq), 47, 27)
                            oled.text(str(range), 110, 27)
                            oled.text("+ MODE-", 0, 45)
                            oled.text(str(smode), 60, 45)
                            oled.text("+ PHASE-", 0, 55)
                            oled.text(str(sphase), 70, 55)
                            oled.text("Deg", 100, 55)
                            oled.show()
                            print(str(smode))

                        if A0.value() ==0 and A1.value() ==1 and A2.value() ==1: #freq
                             sfreq = freqq(sfreq,new_val, current_val,X)
                             sfreq = round(sfreq,1)
                             utime.sleep(delay1)
                             oled.fill(0)
                             oled.text("FREQUENCY-", 0, 10)
                             oled.text(str(sfreq), 47, 27)
                             oled.text(str(range), 110, 27)
                             oled.text("+ MODE-", 0, 45)
                             oled.text(str(smode), 60, 45)
                             oled.text("+ PHASE-", 0, 55)
                             oled.text(str(sphase), 70, 55)
                             oled.text("Deg", 100, 55)
                             oled.show()
                             print(sfreq)

                        ad9833.set_frequency(sfreq,0)
                        ad9833.set_mode(str(smode))
                        ad9833.set_phase(sphase, 0, rads = False)

except KeyboardInterrupt:
    oled.fill(0)
    ad9833.set_frequency(0,0)
    ad9833.set_mode('OFF')
    ad9833.set_phase(0, 0, rads = False)
    oled.show()
    green.value(0)
    red.value(0)