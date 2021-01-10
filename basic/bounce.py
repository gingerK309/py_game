import sys,math,pygame
from pygame.locals import *

pygame.display.set_caption('bounce ball')
blue = (0,50,255)
red = (255,102,102)
white =(255,255,255)
width=640
height=480
center_x =int(width/2)
center_y=int(height/2)
FPS = 180
clock = pygame.time.Clock()
amplitude=100
step=0
pygame.init()
screen = pygame.display.set_mode((width,height))
while True:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == K_ESCAPE:
            pygame.quit()
            sys.exit()
    screen.fill(white)
    step += 0.02
    yPos =-1 * math.sin(step) *amplitude
    pygame.draw.circle(screen,blue,(int(width*0.333),int(yPos)+center_y),30)
    yPos= -1* math.cos(step)*amplitude
    pygame.draw.circle(screen,red,(int(width*0.666),int(yPos)+center_y),30)
    pygame.display.update()
    clock.tick(FPS)