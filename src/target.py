import time
import colors
from utils import ang_dis_to_coo
from scipy.spatial import distance
import math 
from utils import rand

class Target:
    angle = -1
    distance = -1
    # time = -1.0
    color = ()
    direction = 0 # -180 -> 180
    velocity = 0

    # initalization
    def __init__(self, angle, distance, direction, velocity, verified=None):
        self.angle = angle
        self.distance = distance
        self.time = time.time()
        # self.color = colors.red
        # self.color = color
        self.lat = -1
        self.lon = -1
        self.direction = direction
        self.velocity = velocity
        self.verified = verified or False
        self.sus = False
        self.approaching = False
        self.color = colors.red if self.sus else colors.blue

    def update(self, t=0.1/3600):
        self.color = colors.red if self.sus else colors.blue
        if rand.random() < 0.05:
            self.velocity += rand.randint(0,2)-1
            self.velocity = min(max(8, self.velocity), 29)

        x_center, y_center = ang_dis_to_coo(self.angle, self.distance, 700, 400)
        dis = self.velocity * t
        new_x, new_y = ang_dis_to_coo(self.direction, dis, x_center, y_center)
        # print(new_x, new_y)
        # if self.verified:
        new_y += 0.2
        
        self.distance = distance.euclidean((new_x, new_y), (700, 400))
        # if abs(700-new_x) < 1:
        self.angle = math.degrees(math.acos((700-new_x)/self.distance))
        if new_y > 400:
            self.angle = -self.angle
        
        if abs(abs(self.angle - self.direction) - 180) <= 20:
            self.approaching = True
        else:
            self.approaching = False
        
        self.sus = self.approaching and not self.verified
        # print('angle = ', self.angle)
        # elif abs(400-new_y) < 1:
        # self.angle = math.degrees(math.asin((400-new_y)/self.distance))
        # self.angle = math.degrees(math.acotan((400-new_y)/(700-new_x)))

        new_x, new_y
        
