import pygame
pygame.init()
pygame.mixer.music.load('./bgm.mp3')
pygame.mixer.music.play(-1)
display_width=800
display_height=700
finish= False
screen = pygame.display.set_mode((display_width,display_height))
box = True
box_x=20
box_y=20
x=(display_width*0.2)
y=(display_height*0.08)

bg = pygame.image.load('./background.png')
def play(x,y):
    screen.blit(bg,(x,y))

clock = pygame.time.Clock()
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish=True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            box = not box
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: box_y -=3
    if pressed[pygame.K_DOWN]: box_y +=3
    if pressed[pygame.K_LEFT]: box_x -=3
    if pressed[pygame.K_RIGHT]: box_x +=3
    if box: color=(255,0,0)
    else: color =(255,255,0)
    screen.fill((255, 255, 255))
    play(x,y)
    pygame.draw.rect(screen,color,pygame.Rect(box_x,box_y,60,60))
    pygame.display.update()
    clock.tick(60)
