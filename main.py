import pygame
import  pickle
from random import randint, choice

pygame.init()

WIDTH, HEIGHT = 1000, 400
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('*Dino from Google Chrome*')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
nick = "Jaggy"

font = pygame.font.SysFont('arial', 50)
def print_text(x, y,message = 'Nick', font_color = (80,95,134)):
    font_type = pygame.font.SysFont('arial', 30)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x,y))
    if message == 'Nick':
        return False
    else: return True

def scoresSave():
    global scoresBest
    if scores > scoresBest:
        f = open('scores.dat', 'wb')
        pickle.dump(scores,f)
        f.close()
        scoresBest = scores

def scoresLoad():
    global scoresBest
    try:
        f = open('scores.dat', 'rb')
        scoresBest = pickle.load(f)
        f.close()
    except:
        pass
# -------------------------------
imgSprites = pygame.image.load('sprites.png').convert_alpha()
imgBG = imgSprites.subsurface(2, 104, 2400, 26)
imgDinoStand = [imgSprites.subsurface(1514,2,88,94),
                imgSprites.subsurface(1602,2,88,94)]
imgDinoSit = [imgSprites.subsurface(1866,36,118,60),
              imgSprites.subsurface(1984,36,118,60)]
imgDinoLose = [imgSprites.subsurface(1690,2,88,94)]
imgCactus = [ imgSprites.subsurface(446,2,34,70),
              imgSprites.subsurface(480,2,68,70),
              imgSprites.subsurface(512,2,102,70),
              imgSprites.subsurface(512,2,68,70),
              imgSprites.subsurface(652,2,50,100),
              imgSprites.subsurface(752,2,98,100),
              imgSprites.subsurface(850,2,102,100)]
imgPter = [imgSprites.subsurface(260,0,92,82),
           imgSprites.subsurface(352,0,92,82)]
imgRestart = imgSprites.subsurface(2,2,72,64)

sndJump = pygame.mixer.Sound('jump.wav')
sndLevelup = pygame.mixer.Sound('levelup.wav')
sndGameOver = pygame.mixer.Sound('gameover.wav')

fontScores = pygame.font.Font(None, 30)
#-------------------------------
py, sy = 380, 0
isStand = False
speed = 10
frame = 0
scores = 0
scoresBest = 0
bgs = [pygame.Rect(0, HEIGHT - 50, 2400, 26)]#земля
objects = []
timer = 0
level = 0
time = 0
# ----------------------------
class Items:
    def __init__(self):
        objects.append(self)

        if randint(0, 4) == 0 and scores > 500:
            self.image = imgPter                    # птеродактель
            self.speed = 3
            py = HEIGHT - 30 - randint(0, 2) * 50
        else:
            self.image = [choice(imgCactus)]        # кактусы
            self.speed = 0
            py = HEIGHT - 20

        self.rect = self.image[0].get_rect(bottomleft = (WIDTH, py))
        self.frame = 0

    def update(self):
        global  speed, timer, sy, time
        self.rect.x -= speed + self.speed
        self.frame = (self.frame + 0.1) % len(self.image)

        if self.rect.colliderect(dinoRect) and speed != 0:  #столкновение
            speed = 0
            timer = 60
            sy = -10    # Подпрыгивает
            sndGameOver.play()
            time = 0
        if self.rect.right < 0: objects.remove(self)
        # self.rect.right < 0 and objects.remove(self)  # фича
        # if self.rect.right < 500: objects.remove(self) #демонстрация удаления объекта

    def draw(self):
        screen.blit(self.image[int(self.frame)],self.rect)

scoresLoad()
need_input = False
input_rect = pygame.Rect(250,200,140,40)
input_text = ''
play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    if need_input and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            need_input = False
            nick = str(input_text)
            print(nick)
            input_text = ''
        elif event.key == pygame.K_BACKSPACE:
            input_text = input_text[:-1]
        else:
            if len(input_text) < 10:
                input_text += event.unicode

    keys = pygame.key.get_pressed()
    b1, b2, b3 = pygame.mouse.get_pressed()
    pressJump = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP] or b1
    pressSit = keys[pygame.K_LCTRL] or keys[pygame.K_s] or keys[pygame.K_DOWN] or b3

    if (pressJump or pressSit) and speed == 0 and timer == 0:
        scoresSave()    # запись рекорда
        py, sy = 380, 0
        isStand = False
        speed = 10
        frame = 0
        scores = 0
        objects = []

    if pressJump and isStand and speed > 0:         # условие прыжка
        sy = -22
        sndJump.play()

    if isStand: frame = (frame + speed / 35) % 2   # скорость движения ног
    py += sy
    sy = (sy + 1) * 0.97

    isStand = False
    if py > HEIGHT - 20:
        py, sy, isStand = HEIGHT - 20, 0, True

    if speed == 0: dinoImage = imgDinoLose[0]
    elif pressSit: dinoImage = imgDinoSit[int(frame)]
    else: dinoImage = imgDinoStand[int(frame)]

    dw, dh = dinoImage.get_width(), dinoImage.get_height()
    dinoRect = pygame.Rect(150, py - dh, dw, dh)

    for i in range(len(bgs)-1, -1, -1):
        bg = bgs[i]
        bg.x -= speed
        if bg.right < 0: bgs.pop(i)
        # bg.right and bgs.pop(i)

    if bgs[-1].right < WIDTH:
        bgs.append(pygame.Rect(bgs[-1].right, HEIGHT - 50, 2400, 26))

    for obj in objects: obj.update()

    if timer > 0: timer -= 1
    elif speed > 0:                 #объекты создаются только при движении
        timer = randint(100, 150)
        Items()

    scores += speed /50             #подсчёт очков

    if scores // 100 > level:       # подсчёт level
        level = scores // 100
        sndLevelup.play()

    if speed > 0:
        speed = 10 + scores // 100  #увеличиваем скорость каждые 100 очков

    time = (time + 0.01) % 512              # время дня и ночи
    d = abs(time - 256)
    screen.fill((d,d,d))                    # плавная смена дня и ночи
    # screen.fill('white')                  # стираем экран
    for bg in bgs: screen.blit(imgBG, bg)   # отрисовываем землю
    for obj in objects: obj.draw()          # отрисовываем кактусы и птерадактеля
    screen.blit(dinoImage, dinoRect)        # отрисовываем динозавра

    text = fontScores.render('Имя: ' + nick + '        Очки: ' + str(int(scores)), True, 'gray40')   # True - режим размытия
    screen.blit(text,(WIDTH - 300,10))      # отображение имени и очков

    text = fontScores.render('Рекорд: ' + str(int(scoresBest)), True, 'orange')   # True - режим размытия
    screen.blit(text,(50,10))               # отображение очков

    if speed == 0 and timer == 0:
        if print_text(WIDTH // 2, HEIGHT // 2,'FFFF'):
            rect = imgRestart.get_rect(center = (WIDTH // 2, HEIGHT // 2))
        screen.blit(imgRestart, rect)

    if keys[pygame.K_ESCAPE]:
        need_input = True
    print_text(260,200, input_text)

    pygame.display.update()
    clock.tick(FPS)

scoresSave()
pygame.quit()
