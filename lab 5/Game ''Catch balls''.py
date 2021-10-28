import pygame
from pygame.draw import *
from random import randint, uniform
from math import sin, cos, pi
from operator import itemgetter

pygame.init()

FPS = 70
screen = pygame.display.set_mode((800, 600))

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

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

k_ball = 0  # кол-во попаданий в шарики
k_poly = 0  # кол-во попаданий в многоугольники
points = 0  # очки
c = 0  # счётчик времени жизни многоугольника
x = 0
y = 0
color = 0
r = 0
amount_regular_polygon = 2  # Количество отображаемых многоугольников на экране
live_time_poly = 0.7  # Время жизни многоугольников на экране в секундах
r_min = 30  # Миним. радиус шарика, мин. впис. радиус многоугольника
r_max = 100


def draw_score(score):
    """
    Пишет в левом верхнем углу экрана счёт игрока
    :param score: Score
    :type score: float
    :return: None
    :rtype: None
    """
    textsurface = myfont.render('Your Score: ' + str(score), False, WHITE)  # Поверхность с отображением кол-ва очков
    screen.blit(textsurface, (20, 20))


def new_parameters():
    """
    Создаёт новые парарметры, общие для всех фигур
    """
    global x, y, color, r
    x = randint(100, 700)
    y = randint(100, 500)
    r = randint(r_min, r_max)
    color = COLORS[randint(0, 8)]


pool_x = []
pool_y = []
pool_r = []
pool_color = []
pool_vx = []
pool_vy = []


def draw_one_regular_polygon(surface, color_regpoly, vertex_count, radius, position):
    """
    Рисует один правильный многоугольник.
    position: координаты центра фигуры в скобках, например (200, 400)
    """
    n, r_regpoly = vertex_count, radius
    x_regpoly, y_regpoly = position
    pygame.draw.polygon(surface, color_regpoly, [
        (x_regpoly + r_regpoly * cos(2 * pi * i / n), y_regpoly + r_regpoly * sin(2 * pi * i / n))
        for i in range(n)
    ])


def draw_list_polygons(list_x_regpoly, list_y_regpoly, list_vertex_count, list_color_regpoly, list_r_regpoly, amount):
    """Рисует правильные многоугольники из списка. Отличается от функции draw_one_regular_polygon тем,
    что не сама прорисовывает каждый многоугольник, а просит об этом draw_one_regular_polygon"""
    for a in range(amount):
        draw_one_regular_polygon(screen, list_color_regpoly[a], list_vertex_count[a], list_r_regpoly[a],
                                 (list_x_regpoly[a], list_y_regpoly[a]))


pool_x_regpoly = []
pool_y_regpoly = []
pool_vertex_count = []
pool_r_regpoly = []
pool_color_regpoly = []


def check_ball(list_x, list_y, list_vx, list_vy, list_r, list_color_ball, amount):
    """
    Проверяет, попал ли пользователь курсором в шарики

    list_x: список коорд. каждого центра шарика по гориз.
    list_y:  список коорд. кцентра шарика по вертикали
    list_vx: список скоростей каждого шарика по гориз.
    list_vy: список скоростей каждого шарика по вертик.
    list_r: список радиусов шариков
    list_color_ball: список с цветами каждого шарика
    amount: кол-во шариков
    """
    global k_ball, points
    x_click = pygame.mouse.get_pos()[0]  # координата нажатия курсора по горизонтали
    y_click = pygame.mouse.get_pos()[1]  # по вертикали
    for i in range(amount):
        if (x_click - list_x[i]) ** 2 + (y_click - list_y[i]) ** 2 < list_r[i] ** 2:
            k_ball += 1
            points += (list_vx[i] ** 2 + list_vy[i] ** 2) ** (1 / 2) / list_r[i]
            list_x.pop(i)
            list_y.pop(i)
            list_r.pop(i)
            list_color_ball.pop(i)
            list_vx.pop(i)
            list_vy.pop(i)
            break  # Если мы убедились, что в i-ый шарик попали, то дальше можно не проверять


def check_poly(list_x_regpoly, list_y_regpoly, list_vertex_count, list_r_regpoly, amount):
    """
    Проверяет, попал ли пользователь курсором в многоугольник

    list_x_regpoly: список коорд. каждого центра многоугольника по гориз.
    list_y_regpoly:  список коорд. центра многоугольника по вертикали
    list_vertex_count: список с количеством вершин каждого многоугольника
    list_r_regpoly: список радиусов многоугольников
    list_color_ball: список с цветами каждого многоугольника
    amount: кол-во многоугольников
    """
    global k_poly, points
    x_click = pygame.mouse.get_pos()[0]  # координата нажатия курсора по горизонтали
    y_click = pygame.mouse.get_pos()[1]  # по вертикали
    for i in range(amount):
        r_vpis = list_r_regpoly[i] * cos(pi / list_vertex_count[i])
        if (x_click - list_x_regpoly[i]) ** 2 + (y_click - list_y_regpoly[i]) ** 2 < r_vpis ** 2:
            k_poly += 1
            points += 20 / r_vpis
            break  # Если мы убедились, что в i-ый многоугольник попали, то дальше можно не проверять


def move_x(list_x, list_vx, list_r, amount):
    """Сдвигает все шарики из списка по горизонтали
    amount: кол-во шариков
    list_x:  список коорд. по гориз. центров шариков
    list_vx: список скоростей каждого шарика по гориз.
    list_r: список радиусов шариков
    """

    for i in range(amount):
        if list_x[i] - list_r[i] <= 0:
            list_vx[i] = uniform(1, 15)
        elif list_x[i] + list_r[i] >= 800:
            list_vx[i] = -uniform(1, 15)
        vx = list_vx[i]
        list_x[i] = list_x[i] + vx


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


def move_y(list_y, list_vx, list_vy, list_r, amount):
    """Сдвигает все шарики из списка по вертикали
     amount: кол-во шариков
    list_y:  список коорд. по вертикали центров шариков
    list_vx: список скоростей каждого шарика по гориз.
    list_vy: список скоростей каждого шарика по вертик.
    list_r: список радиусов шариков
    """

    for i in range(amount):
        if (list_y[i] - list_r[i] <= 0) or (list_y[i] + list_r[i] >= 600):
            list_vx[i] = z() * list_vx[i]
            list_vy[i] = -list_vy[i]
        vy = list_vy[i]
        list_y[i] = list_y[i] + vy


def draw_balls(amount, list_x, list_y, list_r, list_color_ball):
    """Рисует шарики, беря их данные из списков
    amount: кол-во шариков
    list_x: список коорд. каждого центра шарика по гориз.
    list_y:  список коорд. кцентра шарика по вертикали
    list_r: список радиусов шариков
    list_color_ball: список с цветами каждого шарика
    """
    for i in range(amount):
        circle(screen, list_color_ball[i], (list_x[i], list_y[i]), list_r[i])


scores = []  # Здесь будут данные в хронологическом порядке


def sort_results(text, score):
    """вносит результаты игрока в таблицу результатов 'scores.txt' и отсортировывает её,
    а затем записывает полученное в таблицу 'table.txt'
    :param text: имя игрока
    :param score: счёт игрока
    :return:  'scores.txt' & 'table.txt'
    """
    table = open('table.txt', 'w')  # Будет с сортированными данными
    with open('scores.txt', 'a') as output:  # Здесь данные в хронометрическом порядке
        print(text, '"', score, file=output)
    with open('scores.txt', 'r') as f:
        for string in range(0, 1000, 1):
            stroka = f.readline()
            if stroka != '':
                pairs = stroka.split('" ')
                scores.append(pairs)
                a = scores[string][1]
                a.rstrip('\n')
                a = int(a)
                scores[string][1] = a
    new_list = sorted(scores, key=itemgetter(1))
    new_list.reverse()
    print('Best players', file=table)
    for i in range(0, len(new_list), 1):
        new_list[i][1] = str(new_list[i][1])
        print(i+1, ')', ''.join(new_list[i]), file=table)
    table.close()


pygame.display.update()
clock = pygame.time.Clock()
finished = False

# Наполняем списки с параметрами многоугольников,
# чтобы вначале (при с/FPS < live_time_poly) draw_list_polygons() мог что-нибудь нарисовать
while len(pool_x_regpoly) < amount_regular_polygon:
    pool_x_regpoly.append(x)
    pool_y_regpoly.append(y)
    pool_vertex_count.append(randint(3, 7))
    pool_r_regpoly.append(r)
    pool_color_regpoly.append(color)

print("Введите своё имя: ")
name = input()

while not finished:
    clock.tick(FPS)
    c += 1  # С каждым тиком время жизни многоугольника увеличивается на 1 тик

    koef_v = 15  # Коэф. скорости шариков = макс. скорость при uniform = 1
    amount_balls = 5  # Количество отображаемых шариков на экране
    while len(pool_x) < amount_balls:  # Наполняем каждый список нужным количеством параметров каждого шарика
        new_parameters()
        pool_x.append(x)  # список х-координат центров шариков
        pool_y.append(y)
        pool_r.append(r)
        pool_color.append(color)
        pool_vx.append(uniform(-1, 1) * koef_v)
        pool_vy.append(uniform(-1, 1) * koef_v)

    if c / FPS >= live_time_poly:  # Условие обновления многоугольников на экране
        c = 0
        for j in range(amount_regular_polygon):  # Изменяем каждый элемент списков на нужный параметр каждой фигуры
            new_parameters()
            pool_x_regpoly[j] = x
            pool_y_regpoly[j] = y
            pool_vertex_count[j] = randint(3, 7)
            pool_r_regpoly[j] = r
            pool_color_regpoly[j] = color

    move_x(pool_x, pool_vx, pool_r, amount_balls)  # Двигает шарики по горизонтали
    move_y(pool_y, pool_vx, pool_vy, pool_r, amount_balls)
    draw_balls(amount_balls, pool_x, pool_y, pool_r, pool_color)
    draw_list_polygons(pool_x_regpoly, pool_y_regpoly, pool_vertex_count, pool_color_regpoly, pool_r_regpoly,
                       amount_regular_polygon)

    draw_score(round(points * 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(name, ":")
            print("Кол-во попаданий в шарики: ", k_ball)
            print("Кол-во попаданий в многоугольники: ", k_poly)
            sort_results(name, round(points * 100))

            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_ball(pool_x, pool_y, pool_vx, pool_vy, pool_r, pool_color, amount_balls)
            check_poly(pool_x_regpoly, pool_y_regpoly, pool_vertex_count, pool_r_regpoly, amount_regular_polygon)

    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
