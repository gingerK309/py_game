#encoding = utf-8
import math
#삼각함수는 각도 넣으면 숫자, 역삼각함수는 숫자 넣으면 각도
x1=2
y1=1
x2=5
y2=5
rAngle=math.atan2(y2-y1,x2-x1)
angle = rAngle*180/math.pi
print(int(angle))
