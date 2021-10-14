import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 2
screen = pygame.display.set_mode((1200, 600))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    """
    рисует новый шарик
    """
    global x, y, r
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


def click():
    """
    :return: Пишет "Click!", а на следующей строке координаты шарика
    """
    print('Click!')
    print(x, y, r)
    print(type(event.pos))
    print(event.pos[0])



def check(x_click, y_click):
    """
    Проверяет, попал ли пользователь курсором в шарик
    :param x_click: координата нажатия курсора по горизонтали
    :param y_click: координата нажатия курсора по горизонтали
    :return:
    """
    x_click = event.pos([0])  # Из кортежа с двумя элементами event.pos() вытаскиваем первый, соотв. горизонтали
    y_click = event.pos([1])  # Из кортежа с двумя элементами event.pos() вытаскиваем второй, соотв. вертикали
    if (x_click-x)**2 + (y_click-y)**2 < r**2:
        k+=1


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click()

    new_ball()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
