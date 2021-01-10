import os
import pygame

pygame.init()

width = 800
height = 700
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Pang Game!")

clock = pygame.time.Clock()

current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
rsc_path = os.path.join(current_path,'rsc') # rsc 폴더 위치 반환

# 배경
background = pygame.image.load(os.path.join(rsc_path,'background.png'))

# 배경음, 효과음
shoot = pygame.mixer.Sound(os.path.join(rsc_path,'char.wav'))
hit = pygame.mixer.Sound(os.path.join(rsc_path,'hit.wav'))
shoot.set_volume(0.3)
hit.set_volume(0.3)
pygame.mixer.music.load(os.path.join(rsc_path,'bgm.ogg'))
pygame.mixer.music.play(-1)

# 스테이지
stage = pygame.image.load(os.path.join(rsc_path,'stage.png'))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# 캐릭터
char = pygame.image.load(os.path.join(rsc_path,'char2.png'))
char_size = char.get_rect().size
char_width = char_size[0]
char_height = char_size[1]
char_x_pos= width/2 - char_width/2
char_y_pos = height- char_height-stage_height

# 캐릭터 이동 방향
move_x_left = 0
move_x_right= 0
speed = 4

# 무기
weapon = pygame.image.load(os.path.join(rsc_path,'weapon.png'))
weapon_size =weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기 무한 발사
weapons = []
w_speed = 10

# 공
ball_imgs = [
    pygame.image.load(os.path.join(rsc_path,'balloon1.png')),
    pygame.image.load(os.path.join(rsc_path,'balloon2.png')),
    pygame.image.load(os.path.join(rsc_path,'balloon3.png')),
    pygame.image.load(os.path.join(rsc_path,'balloon4.png'))
]

# 무기/ 공 파괴
w_destroy = -1
b_destroy = -1


# 공 크기에 따른 처음 속도
ball_speed_y=[-20,-18,-16,-15]

# 쪼개지는 공들
balls =[]

balls.append({ # 최초 발생 공
    "pos_x":50, # 공 x 좌표
    "pos_y":50, # 공 y 좌표
    "img_idx":0, # 공 이미지 index
    "to_x": 3, # 공 x축 이동 방향
    "to_y": -6, # 공 y축 이동 방향
    "init_spd_y": ball_speed_y[0] # y 최초 속도
})


# 폰트
game_font = pygame.font.Font(None,48)
total_time = 100
start_ticks = pygame.time.get_ticks() # 시작 시간

# 게임 종료 메시지
game_result = 'Game over...'


running = True
while running:
    fps = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # 캐릭터 왼쪽 이동
                move_x_left -= speed
            elif event.key == pygame.K_RIGHT: # 캐릭터 오른쪽 이동
                move_x_right += speed
            elif event.key == pygame.K_SPACE: # 무기 발사
                shoot.play()
                weapon_x_pos = char_x_pos + char_width/2 - weapon_width/2
                weapon_y_pos = char_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_x_left = 0
            elif event.key == pygame.K_RIGHT:
                move_x_right = 0

    char_x_pos += move_x_left + move_x_right # 캐릭터 위치 정의

    if char_x_pos <0:
        char_x_pos=0
    elif char_x_pos> width - char_width:
        char_x_pos = width - char_width

    weapons = [[w[0],w[1]-w_speed] for w in weapons] # 무기 위치 위로
    weapons = [[w[0],w[1]] for w in weapons if w[1]>0] # 천장에 닿으면 무기 없앰
    
    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_imgs[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if ball_pos_x < 0 or ball_pos_x > width -ball_width:
            ball_val["to_x"] = ball_val["to_x"]*-1 # 가로벽에 닿았을 때 공 위치 변경
        if ball_pos_y >= height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"] # 스테이지에 닿았을 때 공 위치 변경
        else: ball_val["to_y"] += 0.5 # 증가하는 위치 값 줄임

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 충돌 처리

    char_rect = char.get_rect() # 캐릭터 rect 정보 업데이트
    char_rect.left =char_x_pos
    char_rect.top = char_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        # 공 rect 정보 업데이트
        ball_rect = ball_imgs[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x # 공 rect 정보 업데이트
        ball_rect.top = ball_pos_y

        if char_rect.colliderect(ball_rect): # 공 & 캐릭터 충돌 처리
            running = False
            break
            
            
        # 공 & 무기 충돌 처리
        for w_idx , w_val in enumerate(weapons):
            weapon_pos_x  = w_val[0]
            weapon_pos_y = w_val[1]
            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            if weapon_rect.colliderect(ball_rect): # 충돌 체크
                hit.play()
                w_destroy = w_idx # 무기 파괴 값 설정
                b_destroy = ball_idx # 공 파괴 값 설정

                if ball_img_idx < 3: # 가장 작은 공이 아니라면 다음 단계 공으로 나눈다
                    
                    # 현재 공 크기의 정보
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나뉜 공 정보
                    division_ball_rect = ball_imgs[ball_img_idx + 1].get_rect()
                    division_ball_width = division_ball_rect.size[0]
                    division_ball_height = division_ball_rect.size[1]

                    # 왼쪽
                    balls.append({ # 최초 발생 공
                        "pos_x":ball_pos_x + ball_width/2 - division_ball_width/2,
                        "pos_y":ball_pos_y + ball_height/2 - division_ball_height/2,
                        "img_idx":ball_img_idx + 1,
                        "to_x": -3,
                        "to_y": -8,
                        "init_spd_y": ball_speed_y[ball_img_idx+1]})

                    # 오른쪽
                    balls.append({  # 최초 발생 공
                        "pos_x": ball_pos_x + ball_width / 2 - division_ball_width / 2,
                        "pos_y": ball_pos_y + ball_height / 2 - division_ball_height / 2,
                        "img_idx": ball_img_idx + 1,
                        "to_x": 3,
                        "to_y": -8,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})
                break
        else: # 계속 게임을 진행
            continue # 안쪽 for문 탈출 조건 충족 X
        break # 안쪽 for문 탈출 후 바깥 쪽 for문도 탈출
    
    # 충돌된 공이나 무기 없애기
    if b_destroy > -1:
        del balls[b_destroy]
        b_destroy = -1

    if w_destroy > -1:
        del weapons[w_destroy]
        w_destroy = -1

    # 게임 클리어
    if len(balls) == 0 :
       game_result = 'Mission complete!'
       running = False


    screen.blit(background,(0,0))
    for weapon_x_pos,weapon_y_pos in weapons: # 무기 그리기
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))

    for idx,val in enumerate(balls): # 공 그리기
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_imgs[ball_img_idx],(ball_pos_x,ball_pos_y))

    screen.blit(stage,(0,height-stage_height))
    screen.blit(char,(char_x_pos,char_y_pos))

    # 타이머
    elapsed_time = (pygame.time.get_ticks() - start_ticks ) /1000
    timer = game_font.render(f'Time: {int(total_time-elapsed_time)}',True,(0,0,0))
    screen.blit(timer,[10,10])

    # 시간 초과
    if total_time - elapsed_time <= 0:
        game_result = 'Time over...'
        running = False

    pygame.display.update()

msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(width / 2), int(height / 2)))
screen.blit(msg, msg_rect)
pygame.mixer.music.stop()
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit(0)