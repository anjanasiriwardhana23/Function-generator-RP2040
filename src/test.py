from machine import Pin
import utime

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
WIDTH =128 
HEIGHT= 64
i2c=I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

button_pressed_count = 0 # global variable
button_pressed_count1 = 0 # global variable
button_pressed_count2 = 0 # global variable
pin_button = Pin(4, mode=Pin.IN, pull=Pin.PULL_UP)
pin_button1 = Pin(3, mode=Pin.IN, pull=Pin.PULL_UP)
pin_button2 = Pin(21, mode=Pin.IN, pull=Pin.PULL_UP)
button = Pin(18, Pin.IN, Pin.PULL_UP)   #Internal pull-up
button1 = Pin(19, Pin.IN, Pin.PULL_UP)   #Internal pull-up
button2 = Pin(20, Pin.IN, Pin.PULL_UP)   #Internal pull-up


from rotary_irq_rp2 import RotaryIRQ


# Enter the two GPIO pins you connected to data pins A and B
# Note the order of the pins isn't strict, swapping the pins
# will swap the direction of change.
#rotary = RotaryIRQ(6, 7)

# If you're using a Standalone Rotary Encoder instead of a module,
# you might need to enable the internal pull-ups on the Pico
rotary = RotaryIRQ(6, 7, pull_up=True)

current_val = 0  # Track the last known value of the encoder
led1 =Pin(25,Pin.OUT)
delay=.90
delay1=.10
led1.value(0)

def button_isr(pin):
    if pin_button.value() == 0:
      global button_pressed_count
      button_pressed_count += 1
    elif pin_button1.value() == 0:
      global button_pressed_count1
      button_pressed_count1 += 1
    elif pin_button2.value() == 0:
        if button.value() ==0 and button1.value() ==0 and button2.value() ==1:
            global button_pressed_count2
            button_pressed_count2 += 1 
           
def screen():
    oled.fill(0)
    oled.text("<< PREVIOUS", 0, 0)
    oled.text("Tutorial", 0, 40)
    oled.text("NEXT >>", 0, 55)
    oled.show()

def screen1():
    oled.fill(0)
    oled.text("<< PREVIOUS", 0, 0)
    oled.text("nice", 0, 40)
    oled.text("NEXT >>", 0, 55)
    oled.show()

while True:
    button_pressed_count_old = 0
    pin_button.irq(trigger=Pin.IRQ_FALLING,handler=button_isr)
    pin_button1.irq(trigger=Pin.IRQ_FALLING,handler=button_isr)
    pin_button2.irq(trigger=Pin.IRQ_FALLING,handler=button_isr)
    
    new_val = rotary.value()  # What is the encoder value right now?
    
    if current_val != new_val:  # The encoder value has changed!
        oled.fill(0)
        oled.text(str(new_val), 5, 30)
        oled.rect(10, 10, 107, 40, 1)
        oled.show()
        print('Encoder value:', new_val)  # Do something with the new value        
        current_val = new_val  # Track this change as the last know value
    elif button_pressed_count != button_pressed_count_old:
      screen()
      led1.value(1)
      utime.sleep(delay)
      led1.value(0)
      utime.sleep(delay)
      button_pressed_count= 0
    elif button_pressed_count2 != button_pressed_count_old:
      screen1()
      led1.value(1)
      utime.sleep(delay1)
      led1.value(0)
      utime.sleep(delay1)
      button_pressed_count2= 0

