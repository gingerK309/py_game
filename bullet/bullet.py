import sys
import pygame
from pygame.locals import *
import math
import random



fpsClock = pygame.time.Clock()
FPS = 60

def wait_for_key():
    waiting = True
    while waiting:
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = 0
                waiting = False
            if event.type == pygame.KEYUP:
                waiting = False

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_surface, text_rect)

acc=[0,0]
bullets=[]
width, height = 800, 480
white = (255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
flag = 1
screen=pygame.display.set_mode((width, height))
pygame.init()
pygame.font.init()
pygame.display.set_caption('바네사를 지켜라!')
LIGHTBLUE = (0,155,155,128) 

# 시작 화면 만들기
def start():
    screen.fill(LIGHTBLUE)
    draw_text('Save the Vanessa!',56, white,width/2, height*2/5)
    draw_text('attack: click / move: awsd',24, white,width/2, height*3/5)
    draw_text('press a any key...',32, white,width/2, height*3/4)
    pygame.display.flip()
    wait_for_key()
    if pygame.event.get()== pygame.QUIT:
        global flag
        global running
        flag = 0
        running = 0
        pygame.quit()
        sys.exit(0)

# 키 입력 체크
keys = [False, False, False, False]

# 플레이어 위치
playerpos=[100,220]

# 이미지 로딩
player = pygame.image.load("bullet/resources/images/dude.png")
grass = pygame.image.load("bullet/resources/images/grass.png")
castle = pygame.image.load("bullet/resources/images/castle.png")
bull = pygame.image.load("bullet/resources/images/bullet.png")
badguyimg1 = pygame.image.load("bullet/resources/images/badguy.png")
badguyimg=badguyimg1
healthbar = pygame.image.load("bullet/resources/images/healthbar.png")
health = pygame.image.load("bullet/resources/images/health.png")
gameover = pygame.image.load("bullet/resources/images/gameover.png")
youwin = pygame.image.load("bullet/resources/images/youwin.png")

# 오디오 로딩
hit = pygame.mixer.Sound("bullet/resources/audio/explode.wav")
enemy = pygame.mixer.Sound("bullet/resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("bullet/resources/audio/shoot.wav")
hit.set_volume(0.3)
enemy.set_volume(0.2)
shoot.set_volume(0.1)
pygame.mixer.music.load('bullet/resources/audio/bgm.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)


# 게임 구현
running = 1
count = 0
def game():
    global count
    exitcode = 0
    badtimer=100
    badtimer1=0
    badguys=[[width,100]]
    healthvalue= 194
    rstTime = 60
    starttick = pygame.time.get_ticks()
    global running
    pygame.mixer.init()
    while running:
        badtimer-=1
        # 화면 지우기
        screen.fill(0)
        # 이미지로 배경 채우기
        for x in range(int(width/grass.get_width()+1)):
            for y in range(int(height/grass.get_height()+1)):
                screen.blit(grass,(x*100,y*100))

        screen.blit(castle,(10,30))
        screen.blit(castle,(10,135))
        screen.blit(castle,(10,240))
        screen.blit(castle,(10,345))

        # 플레이어 회전
        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26))
        playerrot = pygame.transform.rotate(player, 360 - angle * 57.29) #57.29 = 180/3.14
        playerpos1 = (playerpos[0] - playerrot.get_rect().width / 2, playerpos[1] - playerrot.get_rect().height / 2)
        screen.blit(playerrot, playerpos1)
        
        # 총알 생성
        for bullet in bullets:
            index=0
            velx=math.cos(bullet[0])*10
            vely=math.sin(bullet[0])*10
            bullet[1]+=velx
            bullet[2]+=vely
            if bullet[1]<-64 or bullet[1]>width or bullet[2]<-64 or bullet[2]>height:
                bullets.pop(index)
            index+=1
            for projectile in bullets:
                bull1 = pygame.transform.rotate(bull, 360-projectile[0]*57.29)
                screen.blit(bull1, (projectile[1]+40, projectile[2]+5))
        
        # 적 생성
        if badtimer==0:
            badguys.append([width, random.randint(50,430)])
            badtimer=100-(badtimer1*2)
            if badtimer1>=35:
                badtimer1=35
            else:
                badtimer1+=3
        index=0
        for badguy in badguys:
            if badguy[0]<-64:
                badguys.pop(index)
            badguy[0]-=7
            # 성 피격시
            badrect=pygame.Rect(badguyimg.get_rect())
            badrect.top=badguy[1]
            badrect.left=badguy[0]
            if badrect.left<64:
                hit.play()
                healthvalue -= random.randint(5,20)
                badguys.pop(index)
            # 충돌 체크
            index1=0
            for bullet in bullets:
                bullrect=pygame.Rect(bull.get_rect())
                bullrect.left=bullet[1]
                bullrect.top=bullet[2]
                if badrect.colliderect(bullrect):
                    enemy.play()
                    acc[0]+=1
                    count += 10
                    badguys.pop(index)
                    bullets.pop(index1)
                index1+=1
            # 다음 적 생성
            index+=1
        for badguy in badguys:
            screen.blit(badguyimg, badguy)
        
        # 타이머 그리기
        font = pygame.font.Font(None, 32)
        elapsed_time = (pygame.time.get_ticks() - starttick)/1000
        survivedtext = font.render(f'Time: {int(rstTime-elapsed_time)}',True,(0,0,0))
        textRect = survivedtext.get_rect()
        textRect.topright=[width-5,5]
        screen.blit(survivedtext, textRect)
        draw_text(f'count: {count}',36,black,width/2,5)
        
        # 체력바 그리기
        screen.blit(healthbar, (5,5))
        for health1 in range(healthvalue):
            screen.blit(health, (health1+8,8))

        # 화면 업데이트
        pygame.display.update()
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            # 종료 버튼 눌렀을 때
            if event.type==pygame.QUIT:
                # 게임 종료 시
                pygame.quit()
                sys.exit(0)
            # 키 입력 시
            if event.type == pygame.KEYDOWN:
                if event.key==K_w:
                    keys[0]=True
                elif event.key==K_a:
                    keys[1]=True
                elif event.key==K_s:
                    keys[2]=True
                elif event.key==K_d:
                    keys[3]=True
            # 키 입력 끝남
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_w:
                    keys[0]=False
                elif event.key==pygame.K_a:
                    keys[1]=False
                elif event.key==pygame.K_s:
                    keys[2]=False
                elif event.key==pygame.K_d:
                    keys[3]=False
            if event.type == pygame.MOUSEBUTTONDOWN :
                shoot.play()
                position = pygame.mouse.get_pos()
                acc[1] += 1
                bullets.append ([math.atan2 (position [1]-(playerpos1 [1] +32), position [0]-(playerpos1 [0] +26)), playerpos1 [0] + 32, playerpos1 [1] +32])
        
        # 캐릭터 이동
        if keys[0]:
            playerpos[1]-=5
        elif keys[2]:
            playerpos[1]+=5
        if keys[1]:
            playerpos[0]-=5
        elif keys[3]:
            playerpos[0]+=5

        if playerpos[0]<80:
            playerpos[0] =80
        elif playerpos[0]>width-40:
            playerpos[0]=width-40
        if playerpos[1]<40:
            playerpos[1]=40
        if playerpos[1]>440:
            playerpos[1]=440

        # 게임 오버 체크
        if rstTime - elapsed_time<=0 and healthvalue>0:
            running=0
            exitcode=1
        if healthvalue<=0:
            running=0
            exitcode=0
        if rstTime - elapsed_time<=0 and healthvalue<=0:
            running = 0
            exitcode = 0
        if acc[1]!=0:
            accuracy=acc[0]*1.0/acc[1]*100
        else:
            accuracy=0
    
    # 결과 화면 출력
    if exitcode==0:
        draw_text(f'Accuarcy: {int(accuracy)}%',36,red,width/2,height*2/4)
        draw_text(f'Your score: {count}', 36, red, width/2, height*3/5)
        screen.blit(gameover, (0,0))
        pygame.mixer.music.stop()
        draw_text('if you want to restart, press a any key...',32,white,width/2, height*3/4)
        pygame.display.flip()
        if pygame.event.get() == pygame.QUIT:
            running = 0
            pygame.quit()
            sys.exit(0)
        else:
            wait_for_key()
            running = 1
            playerpos[0]=100
            playerpos[1]=height/2
            for i in range(4):
                keys[i] = False
            acc[0]=0
            acc[1]=0
            accuracy =0
            count=0
            pygame.mixer.music.play(-1, 0.0)
            start()
            
    else:
        draw_text(f'Accuarcy: {int(accuracy)}%',36,green,width/2,height*2/4)
        draw_text(f'Your score: {count}', 36, green, width/2, height*3/5)
        screen.blit(youwin, (0,0))
        pygame.mixer.music.stop()
        draw_text('if you want to restart, press a any key...',32,white,width/2, height*3/4)
        pygame.display.flip()
        if pygame.event.get() == pygame.QUIT:
            running = 0
            pygame.quit()
            sys.exit(0)
        else:
            wait_for_key()
            running = 1
            playerpos[0]=100
            playerpos[1]=height/2
            for i in range(4):
                keys[i] = False
            acc[0]=0
            acc[1]=0
            accuracy =0
            count=0
            pygame.mixer.music.play(-1, 0.0)
            start()
           
while running:
    start()
    if flag and running:
        game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
