import sys
import pygame
import random

pygame.init() # 초기화
width =550
height=740
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("상자 피하기")
count = 0
clock = pygame.time.Clock() #FPS
score_font = pygame.font.Font(None,24)
message_font = pygame.font.Font(None,72)

bg = pygame.image.load('./rsc/bg.png') # 배경 이미지 로드
char = pygame.image.load('./rsc/char.png').convert_alpha() # 스프라이트 이미지 로드
hit = pygame.mixer.Sound('./rsc/hit.wav') # 효과음
hit.set_volume(0.3)
pygame.mixer.music.load('./rsc/bgm.wav') # 배경음
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

# 장애물
obs = pygame.image.load('./rsc/obstacle.png').convert_alpha() # 스프라이트 이미지 로드
obs_size= obs.get_rect().size # 이미지 크기 구함
obs_width = obs_size[0] # 장애물 가로 크기
obs_height = obs_size[1] # 장애물 세로 크기

obsArr=[]

class drop:
    def __init__(self):
        self.obs_x_pos = random.randint(0,width-obs_width)
        self.obs_y_pos = -2
    def speed(self):
        self.obs_y_pos += 5.5
    def draw(self):
        screen.blit(obs,(self.obs_x_pos,self.obs_y_pos))


# 폰트 정의
game_font = pygame.font.Font(None,40) # 폰트 객체 생성

#시작 화면 press any key 이벤트
def wait_for_key():
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                waiting = False
            if event.type == pygame.KEYUP:
                waiting = False

textcolor = (255,255,255)
yellow = (255,255,0)

#화면에 그릴 텍스트 생성 함수
def draw_text(text, size, color, x,y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_surface, text_rect)

# 시작 화면
def start():
    for x in range(int(width / bg.get_width() + 1)):
            for y in range(int(height / bg.get_height() + 1)):
                screen.blit(bg, (x * 250, y * 250)) # 배경 그리기
    draw_text('Suberunker',80, textcolor,width/2, height*2/5)
    draw_text('move: <-,->',36, textcolor,width/2, height*3/5)
    draw_text('press any key...',48,textcolor,width/2, height*3/4)
    pygame.display.flip()
    wait_for_key()
    if pygame.event.get()== pygame.QUIT:    
        global exitcode 
        exitcode = True  
        pygame.quit()
        sys.exit(0)
    
running = True
def game():
    char_size= char.get_rect().size # 이미지 크기 구함
    char_width = char_size[0] # 캐릭터 가로 크기
    char_height = char_size[1] # 캐릭터 세로 크기
    char_x_pos = width/2- char_width/2
    char_y_pos = height - char_height
    # 이동 좌표
    move_x = 0
    speed = 0.3
   
    global running
    while running: # 이벤트 루프
        fps = clock.tick(60) #초당 프레임 수 설정
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN: # 키다운 이벤트 확인
                if event.key == pygame.K_LEFT:
                    move_x -=speed
                if event.key == pygame.K_RIGHT:
                    move_x +=speed
            if event.type == pygame.KEYUP: # 키업하면 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    move_x=0

        char_rect = char.get_rect() # 캐릭터 충돌 처리를 위한 영역 설정
        char_rect.left = char_x_pos
        char_rect.top = char_y_pos

        if  char_x_pos<0: #가로 경계값
            char_x_pos = 0
        elif char_x_pos>width-char_width:
            char_x_pos = width-char_width
        else: char_x_pos +=move_x * fps

        for x in range(int(width / bg.get_width() + 1)):
            for y in range(int(height / bg.get_height() + 1)):
                screen.blit(bg, (x * 250, y * 250)) # 배경 그리기

        screen.blit(char,(char_x_pos,char_y_pos)) # 캐릭터 그리기

        global count
        if count % 40 == 0:
            obsArr.append(drop()) # 장애물 배열에 장애물 추가


        # 점수
        score=score_font.render(str(int(count/10)),True,(255,255,255))
        screen.blit(score,(10,10))

        for i,obstacle in enumerate(obsArr): # 장애물 그리기
            obstacle.speed()
            obstacle.draw()
            if obstacle.obs_y_pos > height:
                obsArr.pop(i)
            obs_rect = pygame.Rect(obs.get_rect())
            obs_rect.left = obstacle.obs_x_pos
            obs_rect.top = obstacle.obs_y_pos
            if char_rect.colliderect(obs_rect): # 충돌 감지
                hit.play()
                pygame.mixer.music.stop()
                running = False
                over = message_font.render('Game over',True,(255,255,255))
                over_size = char.get_rect().size
                over_width = over_size[0]
                over_height = over_size[1]
                screen.blit(over,(width/2-over_width*1.65,height/2-over_height/2))

        count += 1
        pygame.display.update() # 게임 화면 업데이트
start()
game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    pygame.display.update()
