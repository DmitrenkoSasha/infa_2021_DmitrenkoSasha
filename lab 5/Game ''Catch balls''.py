import pygame
from pygame.draw import *
from random import randint, uniform
pygame.init()

FPS = 2
screen = pygame.display.set_mode((800, 600))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

k=0 #  кол-во попаданий
c=0 #   кол-во шариков в списке

pool_x = []
pool_y = []
pool_r = []
pool_color = []

def new_ball():
    """
    рисует новый шарик
    """
    global x, y, color, r
    x = randint(100, 700)
    y = randint(100, 500)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


def check():
    """
    Проверяет, попал ли пользователь курсором в шарик
    :return: "Попал!" или "Мимо!"
    """
    global k
    x_click = pygame.mouse.get_pos()[0]  #координата нажатия курсора по горизонтали
    y_click = pygame.mouse.get_pos()[1]  #координата нажатия курсора по вертикали
    if (x_click-x)**2 + (y_click-y)**2 < r**2:
        k+=1
        print("Попал!")
    else:
        print("Мимо!")

def move_x():
    """Сдвигает все шарики из списка по горизонтали """
    
    for i in range(len(pool_x)):
        vx = 1  #uniform(-1, 1) * 3   Будет каждый тик новую скорость каждому шару давать?
        pool_x[i] = pool_x[i] + vx
    print(pool_x)    
    

def move_y():
    """Сдвигает все шарики из списка по горизонтали """
    
    for i in range(len(pool_y)):
        vy = uniform(-1, 1) * 3   #Будет каждый тик новую скорость каждому шару давать?
        pool_y[i] = pool_y[i] + vy
    print(pool_y)

def draw():
    "Рисует шарики из списка"
    for i in range(len(pool_x)):
        circle(screen, pool_color[i], (pool_x[i], pool_y[i]), pool_r[i])


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check()
        
    new_ball()
    c+=1
    if c < 5:
        pool_x.append(x) #список х-координат центров шариков
        pool_y.append(y) 
        pool_r.append(r) 
        pool_color.append(color)
        
    move_x()
    move_y()
    draw()
    
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
