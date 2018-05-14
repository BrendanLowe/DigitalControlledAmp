import RPi.GPIO as GPIO
import time

UDCPin = 12    # pin12
INCPin = 16

def setup():
  GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
  GPIO.setup(UDCPin, GPIO.OUT)   # Set LedPin's mode is output
  GPIO.output(UDCPin, GPIO.LOW) # Set LedPin high(+3.3V) to turn on led

  GPIO.setup(INCPin, GPIO.OUT)   # Set LedPin's mode is output
  GPIO.output(INCPin, GPIO.HIGH) # Set LedPin high(+3.3V) to turn on led


def blink():
  while True:
    GPIO.output(INCPin, GPIO.HIGH)  # led on
    print "On"
    time.sleep(1)
    GPIO.output(INCPin, GPIO.LOW) # led off
    print "Off"
    time.sleep(1)
def destroy():
  GPIO.output(UDCPin, GPIO.LOW)   # led off
  GPIO.output(INCPin, GPIO.LOW)   # led off
  GPIO.cleanup()                  # Release resource
if __name__ == '__main__':     # Program start from here
  setup()
  try:
    blink()
  except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    destroy()
