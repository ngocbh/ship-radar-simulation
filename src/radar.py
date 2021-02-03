import FakeRPi.GPIO as GPIO
import pygame
import math
import time
import colors
import sys
import cv2
from target import *
from display import *
from ultrasonicsensor import ultrasonicRead

# The range is set to 50 cm, to change it 
# change the range condition in the ultrasonicsensor module
# change the range condition in this module
# change scale in e and f in draw function in display module

print('Radar Start')

# initialize the program
x = pygame.init()

pygame.font.init()

defaultFont = pygame.font.get_default_font()

fontRenderer = pygame.font.Font(defaultFont, 16)

radarDisplay = pygame.display.set_mode((1400, 800), pygame.RESIZABLE )
# radarDisplay = pygame.display.set_mode((1920, 1080), vsync=1)

pygame.display.set_caption('Radar Screen')

# setup the servo and ultrasonic
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

servoPin = 12
GPIO.setup(servoPin, GPIO.OUT)
servo = GPIO.PWM(servoPin, 50)
servo.start(7)

TRIG = 16
ECHO = 18
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# targets list
targets = {
    20:Target(20, 200, 150, 13, True), 
    35:Target(35, 150, 0, 22, True), 
    50:Target(50, 250, -137, 30, True), 
    60:Target(60, 300, 90, 23, True), 
    # 80:Target(80, 80, 125, 24, True), 
    # 110:Target(110, 300, -60, 17, True), 
    # 140:Target(140, 200, -30, 29, True), 
    160:Target(160, 150, -15, 19, True)
}

try:
    while True:
        # rotate from 0 to 360
        for angle in range(0, 360):
            distance = ultrasonicRead(GPIO, TRIG, ECHO)
            # change the condition if the range is changed
            # if distance != -1 and distance <= 50:
                # targets[angle] = Target(angle, distance)
                
            draw(radarDisplay, targets, angle, distance, fontRenderer)

            # angle = 360 - angle
            # dc = 1.0 / 18.0 * angle + 2
            # servo.ChangeDutyCycle(dc)

            time.sleep(0.01) # 0.01*360=3.6s

        # # rotate from 0 to 180
        # for angle in range(0, 180):
            
        #     distance = ultrasonicRead(GPIO, TRIG, ECHO)
            
        #     # change the condition if the range is changed
        #     # if distance != -1 and distance <= 50:
        #         # targets[angle] = Target(angle, distance)
                
        #     draw(radarDisplay, targets, angle, distance, fontRenderer)

        #     angle = 180 - angle
        #     dc = 1.0 / 18.0 * angle + 2
        #     servo.ChangeDutyCycle(dc)

        #     time.sleep(0.001)
            

        # # rotate from 180 to 0
        # for angle in range(180, 0, -1):
            
        #     distance = ultrasonicRead(GPIO, TRIG, ECHO)
            
        #     # change the condition if the range is changed
        #     # if distance != -1 and distance <= 50:
        #     #     targets[angle] = Target(angle, distance)
            
        #     draw(radarDisplay, targets, angle, distance, fontRenderer)

        #     angle = 180 - angle
        #     dc = 1.0 / 18.0 * angle + 2
        #     servo.ChangeDutyCycle(dc)

        #     time.sleep(0.001)
            
        # detect if close is pressed to stop the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            
except KeyboardInterrupt:
    print('Radar Exit')
    servo.stop()
    GPIO.cleanup()
    
# except Exception as e:
#     print(e)
#     print('Radar Exit')
#     servo.stop()
#     GPIO.cleanup()
    
    
pygame.quit()
sys.exit()
