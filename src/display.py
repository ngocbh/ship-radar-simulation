import colors
import pygame
import math
import time
from risk_assessment_model import vessel as vessel_dict, assess_risk
from utils import ang_dis_to_coo
from vessel import Vessel

""" This module draws the radar screen """
dis_thresh = 600
vessel = Vessel(vessel_dict)

def draw_arrow(screen, colour, start, end, arrow_size=10):
    pygame.draw.line(screen,colour,start,end,arrow_size//2)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pygame.draw.polygon(screen, colour, 
    ((end[0]+arrow_size*math.sin(math.radians(rotation)), end[1]+arrow_size*math.cos(math.radians(rotation))), 
    (end[0]+arrow_size*math.sin(math.radians(rotation-120)), end[1]+arrow_size*math.cos(math.radians(rotation-120))), 
    (end[0]+arrow_size*math.sin(math.radians(rotation+120)), end[1]+arrow_size*math.cos(math.radians(rotation+120)))))

def draw_target(radarDisplay, target, x, y, fontRenderer):
    pygame.draw.circle(radarDisplay, target.color, (x, y), 10)
    rel_x = math.cos(math.radians(target.direction)) * target.velocity
    rel_y = math.sin(math.radians(target.direction)) * target.velocity
    draw_arrow(radarDisplay, target.color, (x, y), (x-rel_x, y-rel_y), arrow_size=8)
    text = fontRenderer.render("{} knots".format(target.velocity), 1, colors.green)
    radarDisplay.blit(text,(x+10,y))

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def get_risk(targets):
    no_sus_ships = 0
    for an in list(targets):
        if targets[an].sus:
            no_sus_ships += 1
    vessel_score = assess_risk(vessel_dict) 
    return sigmoid(0.7 * (vessel_score - 0.5) + no_sus_ships ) * 100, no_sus_ships

def draw(radarDisplay, targets, angle, distance, fontRenderer):
     # draw initial screen
    radarDisplay.fill(colors.black)

    pygame.draw.circle(radarDisplay, colors.green, (700,400), 600, 1)

    pygame.draw.circle(radarDisplay, colors.green, (700,400), 500, 1)

    pygame.draw.circle(radarDisplay, colors.green, (700,400), 400, 1)

    pygame.draw.circle(radarDisplay, colors.green, (700,400), 300, 1)

    pygame.draw.circle(radarDisplay, colors.green, (700,400), 200, 1)

    pygame.draw.circle(radarDisplay, colors.green, (700,400), 100, 1)

    pygame.draw.circle(radarDisplay, colors.white, (700,400), 5)

    radarDisplay.fill(colors.black, [0, 785, 1400, 20])

    # horizental line
    pygame.draw.line(radarDisplay, colors.green, (30, 400), (1370, 400), 1)
    # pygame.draw.line(radarDisplay, colors.green, (30, 750), (1370, 750), 1)

    # 45 degree line
    # pygame.draw.line(radarDisplay, colors.green, (1100, 800),(205, 285-400), 1)

    # 90 degree line
    pygame.draw.line(radarDisplay, colors.green, (700, 800), (700, 0), 1)

    # 135 degree line
    # pygame.draw.line(radarDisplay, colors.green, (700, 780), (1195, 285), 1)

    

    # write the 0 degree
    # text = fontRenderer.render("0", 1, colors.green)
    # radarDisplay.blit(text,(10,400))

    # write the 45 degree
    # text = fontRenderer.render("45", 1, colors.green)
    # radarDisplay.blit(text,(180,260))

    # write the 90 degree
    # text = fontRenderer.render("90", 1, colors.green)
    # radarDisplay.blit(text,(690,10))

    # write the 135 degree
    # text = fontRenderer.render("135", 1, colors.green)
    # radarDisplay.blit(text,(1205,270))

    # write the 180 degree
    # text = fontRenderer.render("180", 1, colors.green)
    # radarDisplay.blit(text,(1365,400))

    # draw the moving line
    a = math.sin(math.radians(angle)) * 700.0
    b = math.cos(math.radians(angle)) * 700.0
    pygame.draw.line(radarDisplay, colors.green, (700, 400), (700 - int(b), 400 - int(a)), 3)

    # draw stastics board
    pygame.draw.rect(radarDisplay, colors.blue, [20, 20, 225, 170], 2)

    # write the current angle
    text = fontRenderer.render("Angle : " + str(angle), 1, colors.white)
    radarDisplay.blit(text,(40,40))

    # write the distance
    if distance == -1:
        text = fontRenderer.render("Distance : Out Of Range" , 1, colors.white)
    else:
        text = fontRenderer.render("Distance : " + str(distance) + " cm" , 1, colors.white)
    radarDisplay.blit(text,(40,70))

    text = fontRenderer.render(f"Ship name: {vessel.name}", 1, colors.white)
    radarDisplay.blit(text,(40,100))

    risk_score, num_sus_ships = get_risk(targets)

    text = fontRenderer.render("No. sus ships : {}".format(num_sus_ships), 1, colors.white if num_sus_ships == 0 else colors.red)
    radarDisplay.blit(text,(40,130))

    text = fontRenderer.render("Risk : {:.0f}%".format(risk_score), 1, colors.white if risk_score < 70 else colors.red)
    radarDisplay.blit(text,(40,160))

    # draw stastics board
    pygame.draw.rect(radarDisplay, colors.blue, [1210, 20, 170, 140], 2)

    text = fontRenderer.render("Lon : {}".format(vessel.lon), 1, colors.white)
    radarDisplay.blit(text,(1230,40))

    text = fontRenderer.render("Lat : {}".format(vessel.lat), 1, colors.white)
    radarDisplay.blit(text,(1230,80))

    text = fontRenderer.render("Velocity: {} knots".format(vessel.velocity), 1, colors.white)
    radarDisplay.blit(text,(1230,120))

    vessel.lon += 0.00013945
    # draw targets
    # angle
    for an in list(targets):
        # calculate the coordinates and the remoteness of the target
        # x = 700 - math.cos(math.radians(target.angle)) * target.distance
        # y = 400 - math.sin(math.radians(target.angle)) * target.distance
        if targets[an].distance > dis_thresh:
            del targets[an]
            continue
        # if an > angle-1 and an < angle+5:
        x, y = ang_dis_to_coo(targets[an].angle, targets[an].distance, 700, 400)
        draw_target(radarDisplay, targets[an], x, y, fontRenderer)
        targets[an].update(t=0.01)
        # targets[an].time = time.time()

        # else:
            # # fading
            # diffTime = time.time() - targets[an].time
            # if diffTime >= 0.0 and diffTime <= 0.5:
            #     targets[an].color = colors.red1L
            # elif diffTime > 0.5 and diffTime <= 1:
            #     targets[an].color = colors.red2L
            # elif diffTime > 1.0 and diffTime <= 1.5:
            #     targets[an].color = colors.red3L
            # elif diffTime > 1.5 and diffTime <= 2.0:
            #     targets[an].color = colors.red4L
            # elif diffTime > 2.0 and diffTime <= 2.5:
            #     targets[an].color = colors.red5L
            # elif diffTime > 2.5 and diffTime <= 3.0:
            #     targets[an].color = colors.red6L
        # elif diffTime > 3.0:
        #     del targets[an]
            
    # update the screen
    pygame.display.update()
    
