import sys,pygame,math
from pygame.locals import *

pygame.display.set_caption('회전하기')
white=(255,255,255)
black=(0,0,0)

pygame.init()
width = 600
height= 600
screen = pygame.display.set_mode((width,height))

rot = pygame.image.load('turn.png')
def rotation(x1,y1,x2,y2):
    y=y1-y2
    x=x1-x2
    angle=math.atan2(x,y)
    angle = angle *(180/math.pi)
    angle =(angle+90)%360
    return angle

while True:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == K_ESCAPE:
            pygame.quit()
            sys.exit()

    screen.fill(white)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rot_x= int(width/2)
    rot_y= int(height/2)
    degree = rotation(rot_x,rot_y,mouse_x,mouse_y)
    turn_rot = pygame.transform.rotate(rot,degree)
    rot_pos = turn_rot.get_rect()
    rot_pos.center=(rot_x,rot_y)
    screen.blit(turn_rot,rot_pos)

    pygame.draw.line(screen,black,(mouse_x-10,mouse_y),(mouse_x+10,mouse_y))
    pygame.draw.line(screen, black, (mouse_x, mouse_y-10), (mouse_x, mouse_y+10))
    pygame.display.update()
