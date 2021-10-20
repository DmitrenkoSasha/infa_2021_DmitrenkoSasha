import pygame
from pygame.draw import *
from random import randint, uniform
from math import sin, cos, pi


pygame.init()

FPS = 70
screen = pygame.display.set_mode((800, 600))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
LIME = (0, 128, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
MAROON = (128, 0, 0)
WHITE = (250, 228, 225)
COLORS = [RED, BLUE, YELLOW, GREEN, LIME, MAGENTA, CYAN, WHITE, MAROON]

k = 0  # кол-во попаданий
c = 0  # кол-во шариков в списке
x = 0
y = 0
color = 0
r = 0

pool_x = []
pool_y = []
pool_r = []
pool_color = []
pool_vx = []
pool_vy = []


def new_ball():
    """
    Добавляет новый шарик в список
    """
    global x, y, color, r
    x = randint(100, 700)
    y = randint(100, 500)
    r = randint(10, 100)
    color = COLORS[randint(0, 8)]


def draw_regular_polygon(surface, color_regpoly, vertex_count, radius, position):
    """
    Рисует один из правильных многоугольников
    position: координаты центра фигуры в скобках, например (200, 400)
    """
    n, r_regpoly = vertex_count, radius
    x_regpoly, y_regpoly = position
    pygame.draw.polygon(surface, color_regpoly, [
        (x_regpoly + r_regpoly * cos(2 * pi * i / n), y_regpoly + r_regpoly * sin(2 * pi * i / n))
        for i in range(n)
    ])


def check():
    """
    Проверяет, попал ли пользователь курсором в шарик
    :return: "Попал!" или "Мимо!"
    """
    global k
    flag = 0
    x_click = pygame.mouse.get_pos()[0]  # координата нажатия курсора по горизонтали
    y_click = pygame.mouse.get_pos()[1]  # координата нажатия курсора по вертикали
    for i in range(len(pool_x)):
        if (x_click - pool_x[i]) ** 2 + (y_click - pool_y[i]) ** 2 < pool_r[i] ** 2:
            k += 1
            flag = 1
            pool_x.pop(i)
            pool_y.pop(i)
            pool_r.pop(i)
            pool_color.pop(i)
            pool_vx.pop(i)
            pool_vy.pop(i)
            break
    if flag == 1:
        print("Попал!")
    else:
        print("Мимо!")


def move_x():
    """Сдвигает все шарики из списка по горизонтали """

    for i in range(len(pool_x)):
        if pool_x[i] - pool_r[i] <= 0:
            pool_vx[i] = uniform(1, 20)
        elif pool_x[i] + pool_r[i] >= 800:
            pool_vx[i] = -uniform(1, 20)
        vx = pool_vx[i]
        pool_x[i] = pool_x[i] + vx


def z():
    """Выдаёт случайно или 1, или -1. На это число,
    в случае столкновения шарика с вертикальными стенками, будет домножаться скорость по горизонтали"""
    exempli = randint(-1, 1)
    g = 0
    if exempli > 0:
        g = 1
    elif exempli <= 0:
        g = -1
    return g


def move_y():
    """Сдвигает все шарики из списка по вертикали """

    for i in range(len(pool_y)):
        if (pool_y[i] - pool_r[i] <= 0) or (pool_y[i] + pool_r[i] >= 600):
            pool_vx[i] = z()*pool_vx[i]
            pool_vy[i] = -pool_vy[i]
        vy = pool_vy[i]
        pool_y[i] = pool_y[i] + vy


def draw_balls():
    """Рисует шарики из списка"""
    for i in range(len(pool_x)):
        circle(screen, pool_color[i], (pool_x[i], pool_y[i]), pool_r[i])


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)

    amount_balls = 5  # Количество отображаемых шариков на экране
    while len(pool_x) < amount_balls:
        new_ball()
        pool_x.append(x)  # список х-координат центров шариков
        pool_y.append(y)
        pool_r.append(r)
        pool_color.append(color)
        pool_vx.append(uniform(-1, 1) * 20)
        pool_vy.append(uniform(-1, 1) * 20)

    move_x()
    move_y()
    draw_balls()
    draw_regular_polygon(screen, color, 4, 20,  (100, 100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Кол-во попаданий в шарики: ", k)
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
