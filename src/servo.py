import RPi.GPIO as GPIO
from time import sleep

def open_servo():
    # initialize servo
    servopin = 32
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servopin,GPIO.OUT) # GPIO.setup(ledpin,GPIO.OUT)
    pi_pwm = GPIO.PWM(servopin,1000)
    pi_pwm.start(0)
    print("[SERVO] Initilized, opening door.")

    # open and close the servo
    for duty in range(0,101,1):
        pi_pwm.ChangeDutyCycle(duty)
        sleep(0.01)

    print("[SERVO] Door opened, waiting 5 seconds then closing.")
    sleep(5)

    for duty in range(100,-1,-1):
            pi_pwm.ChangeDutyCycle(duty)
            sleep(0.01)

if __name__ == "__main__":
    servopin = 32
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servopin,GPIO.OUT) # GPIO.setup(ledpin,GPIO.OUT)
    pi_pwm = GPIO.PWM(servopin,1000)
    pi_pwm.start(0)

    # currently have it to rotate some degree to the right and left. 
    # for open, turn right; for close, turn left
    while True:
        for duty in range(0,101,1):
            pi_pwm.ChangeDutyCycle(duty)
            sleep(0.01)
        sleep(0.5)

        for duty in range(100,-1,-1):
            pi_pwm.ChangeDutyCycle(duty)
            sleep(0.01)
        sleep(0.5)
