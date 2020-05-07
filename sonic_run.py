#import library
import RPi.GPIO as GPIO
import time
import pyttsx3
#import pyttsx

# set GPIO to  BCM
GPIO.setmode(GPIO.BCM)

# define GPIO port number
GPIO_TRIGGER = 2
GPIO_ECHO = 3
GPIO_TRIGGER2 = 4
GPIO_ECHO2 = 5

# define GPIO port (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)

def distance():
    # set Trig to true
    GPIO.output(GPIO_TRIGGER, True)
    GPIO.output(GPIO_TRIGGER2, True)
    # the set up 10 us 
    time.sleep(0.00001)
    GPIO.output( GPIO_TRIGGER, False)
    GPIO.output( GPIO_TRIGGER2, False)
    start_time = time.time()
    stop_time = time.time()
    start_time2 = time.time()
    stop_time2 = time.time()

    # record the strt time 1
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()
        start_time2 = time.time()

    # record the stop time 2
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()
        stop_time2 = time.time()

    # time difference 
    time_diff = stop_time - start_time
    time_diff2 = stop_time2 - start_time2
    if time_diff2 < time_diff:
        time_diff = time_diff2
    #print ("stop_time is %d", stop_time)
    #print ("start_time is %d", start_time) 
    # convert time to distance
    distance = (time_diff * 34300) / 2

    return distance


if __name__ == '__main__':
    try:
        engine = pyttsx3.init()
        while True:
            dis = distance()
            print("Measured Distance = {:.2f} cm".format(dis))
            #time.sleep(1)
            string = str(dis).split('.')[0] + '.' + str(dis).split('.')[1][:2]
            string = 'Measured Distance is ' + string + ' centimeter.'
            if dis < 10:
                string = string + 'Warning.'
            engine.say(string)
            engine.runAndWait()
            time.sleep(2) 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        engine.stop()
        GPIO.cleanup()
