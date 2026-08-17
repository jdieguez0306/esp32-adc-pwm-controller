from machine import Pin, ADC, PWM, RTC, Timer
import time

# Part 1 setting RTC with User input

rtc = RTC() # Global initialization of RTC

def get_user_input():
    # Get the current date and time from user inputs
    year = int(input("Year? "))
    month = int(input("Month? "))
    day = int(input("Day? "))
    weekday = int(input("Weekday? "))
    hour = int(input("Hour? "))
    minute = int(input("Minute? "))
    second = int(input("Second? "))
    microsecond = int(input("Microsecond? "))

    # Initialize the RTC clock using the user inputs
    rtc.datetime((year, month, day, weekday, hour, minute, second, microsecond))


# Use a timer to print out the updated date every thirty seconds
def print_curr_time(timer):
    date_time = rtc.datetime()
    print("Date: {:02d}/{:02d}/{:04d}".format(date_time[1], date_time[2], date_time[0]))
    print("Time: {:02d}:{:02d}:{:02d}:{:06d}".format(date_time[4], date_time[5], date_time[6], date_time[7]))


# Part 2: ADC pin and Reading the value
potent = ADC(Pin(32))         # Initialize pin used for potentiometer (ADC CH1)
potent.atten(ADC.ATTN_11DB)   # Sets an 11DB attenuation to read 3.3V 
potent.width(ADC.WIDTH_12BIT) # Sets a 12 bit resolution for ADC


#Part 3 PWM LED initialization
red_led = PWM(Pin(25))  # Initialize pin for LED
red_led.freq(10)        # Initial frequency
red_led.duty(512)       # Initial Duty Cycle

ignore_switch_press = False
mode = 0                # Initialize starting mode just in an idle state
                        # mode = 1 (Frequency Cycle)
                        # mode = 2 (Duty Cycle)

# Initialize the switch press button (on board GPIO38)
sp_button = Pin(38, Pin.IN, Pin.PULL_UP)

# Set Timer for Debouncer
debounce_timer = Timer(2)

# Debounce Callback
def debounce_callback(timer):
    # Global variables
    global ignore_switch_press
    
    ignore_switch_press  = False
    
# Switch Press CallBack interrupt
def switch_press_callback(pin):
    
    # Global variables
    global ignore_switch_press, mode
    
    if ignore_switch_press:
        return
    ignore_switch_press = True
    
    # Change the mode from frequency control to duty cycle control
    control = sp_button.value()   # Check to see if switch press button is pressed (Pulled low)
    if control == 0:
        if mode == 0:
            mode = 1
            # Debug
            print("Frequency Control")
        elif mode == 1:
            mode = 2
            # Debug
            print("Duty Cycle Control")
        elif mode == 2:
            mode = 1
            # Debug
            print("Frequency Control")
            
    # Set debounce timer for interrupt using debounce callback   
    debounce_timer.init(period = 250, mode = Timer.ONE_SHOT, callback = debounce_callback)
    
sp_button.irq(handler = switch_press_callback, trigger = Pin.IRQ_FALLING | Pin.IRQ_RISING)

# Go from ADC value of potent value to frequency value
def adc_to_freq(potent_val):
    
    # Keeps potent value in the range form 0 - 4095
    potent_val = max(0, min(4095, potent_val))
    
    return int(1 + (potent_val/4095) * (20 - 1))

# Go from ADC value of potent value to duty cycle
def adc_to_duty(potent_val):
    
    # Keeps potent value in the range from 0 - 4095
    potent_val = max(0, min(4095, potent_val))
    
    return int((potent_val / 4095) * 1023)

# periodic timer that calls a function to read the value of ADC
def read_potent_val(timer):
    
    value = potent.read()  # returns raw ADC value based on resolution bits (0-4095 for 12 bits)
    update_led(value)
    
# Update the Led based on the potentiometer value
def update_led(value):
    
    # Global variable to determine which mode (idle, frequency, or duty cycle)
    global mode
    
    # Get Frequency for LED
    if mode == 1:
        curr_frequency = adc_to_freq(value)
        red_led.freq(curr_frequency)
    # Get Duty Cycle for LED   
    elif mode == 2:
        curr_duty = adc_to_duty(value)
        red_led.duty(curr_duty)


def main():
    # Get the current time from User to set up RTC
    get_user_input()
    
    # Set Up Timer for  RTC
    rtc_timer = Timer(0)
    rtc_timer.init(period= 30000, mode= Timer.PERIODIC, callback = print_curr_time)
    
    # Set up Timer to read potentiometer every 100 ms
    adc_timer = Timer(1)
    adc_timer.init(period = 100, mode = Timer.PERIODIC, callback = read_potent_val)

main()


    
