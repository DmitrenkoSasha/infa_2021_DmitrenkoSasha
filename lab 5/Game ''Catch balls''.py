import pygame
from pygame.draw import *
from random import randint, uniform
from math import sin, cos, pi
from operator import itemgetter


pygame.init()

FPS = 70
screen = pygame.display.set_mode((800, 600))

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)  # Поверхность с отображением кол-ва очков

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
amount_regular_polygon = 1  # Количество отображаемых многоугольников на экране
live_time_poly = 0.7  # Время жизни многоугольников на экране в секундах
r_min = 30  # Миним. радиус шарика, мин. впис. радиус многоугольника
r_max = 100


def draw_score(score):
    """
    Draws score.
    :param score: Score
    :type score: float
    :return: None
    :rtype: None
    """
    textsurface = myfont.render('Your Score: ' + str(score), False, BLACK)
    screen.blit(textsurface, (20, 20))
    textsurface = myfont.render('Your Score: ' + str(score), False, WHITE)
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


def draw_list_polygons():
    """Рисует правильные многоугольники из списка. Отличается от функции draw_one_regular_polygon тем,
    что не сама прорисовывает каждый многоугольник, а просит об этом draw_one_regular_polygon"""
    for i in range(amount_regular_polygon):
        draw_one_regular_polygon(screen, pool_color_regpoly[i], pool_vertex_count[i], pool_r_regpoly[i],
                                 (pool_x_regpoly[i], pool_y_regpoly[i]))


pool_x_regpoly = []
pool_y_regpoly = []
pool_vertex_count = []
pool_r_regpoly = []
pool_color_regpoly = []


def check_ball():
    """
    Проверяет, попал ли пользователь курсором в шарики
    """
    global k_ball, points
    x_click = pygame.mouse.get_pos()[0]  # координата нажатия курсора по горизонтали
    y_click = pygame.mouse.get_pos()[1]  # по вертикали
    for i in range(amount_balls):
        if (x_click - pool_x[i]) ** 2 + (y_click - pool_y[i]) ** 2 < pool_r[i] ** 2:
            k_ball += 1
            points += (pool_vx[i]**2+pool_vy[i]**2)**(1/2)/pool_r[i]
            pool_x.pop(i)
            pool_y.pop(i)
            pool_r.pop(i)
            pool_color.pop(i)
            pool_vx.pop(i)
            pool_vy.pop(i)
            break  # Если мы убедились, что в i-ый шарик попали, то дальше можно не проверять


def check_poly():
    """
    Проверяет, попал ли пользователь курсором в многоугольник
    """
    global k_poly, points
    x_click = pygame.mouse.get_pos()[0]  # координата нажатия курсора по горизонтали
    y_click = pygame.mouse.get_pos()[1]  # по вертикали
    for i in range(amount_regular_polygon):
        r_vpis = pool_r_regpoly[i] * cos(pi / pool_vertex_count[i])
        if (x_click - pool_x_regpoly[i]) ** 2 + (y_click - pool_y_regpoly[i]) ** 2 < r_vpis ** 2:
            k_poly += 1
            points += 20/r_vpis
            break  # Если мы убедились, что в i-ый многоугольник попали, то дальше можно не проверять


def move_x():
    """Сдвигает все шарики из списка по горизонтали """

    for i in range(len(pool_x)):
        if pool_x[i] - pool_r[i] <= 0:
            pool_vx[i] = uniform(1, 15)
        elif pool_x[i] + pool_r[i] >= 800:
            pool_vx[i] = -uniform(1, 15)
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
    for i in range(amount_balls):
        circle(screen, pool_color[i], (pool_x[i], pool_y[i]), pool_r[i])


scores = []


def sort_results(text, score):
    """вносит результаты игрока в таблицу результатов и отсортировывает её
    :param text: имя игрока
    :param score: счёт игрока
    """
    table = open ('table.txt', 'w')
    with open ('scores.txt', 'a') as output:
      print(text, '"', score, file = output)
    with open ('scores.txt', 'r') as f:
      for string in range (0, 1000, 1):
        stroka = f.readline()
        if stroka != '':
            pairs = stroka.split('" ')
            scores.append(pairs)
            a = scores[string][1]
            a.rstrip('\n')
            a = int (a)
            scores[string][1] = a
    new_list = sorted(scores, key=itemgetter(1))
    new_list.reverse()
    print('Results table', file = table)
    for i in range (0, len(new_list), 1):
      new_list[i][1] = str (new_list[i][1])
      print(''.join(new_list[i]), file = table)
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

    if c/FPS >= live_time_poly:  # Условие обновления многоугольников на экране
        c = 0
        for j in range(amount_regular_polygon):  # Изменяем каждый элемент списков на нужный параметр каждой фигуры
            new_parameters()
            pool_x_regpoly[j] = x
            pool_y_regpoly[j] = y
            pool_vertex_count[j] = randint(3, 7)
            pool_r_regpoly[j] = r
            pool_color_regpoly[j] = color

    move_x()  # Двигает шарики по горизонтали
    move_y()
    draw_balls()
    draw_list_polygons()

    draw_score(round(points*100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(name, ":")
            print("Кол-во попаданий в шарики: ", k_ball)
            print("Кол-во попаданий в многоугольники: ", k_poly)
            sort_results(name, int(round(points*100)))

            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_ball()
            check_poly()

    pygame.display.update()
    screen.fill(BLACK)

'''output = open('Рейтинг игроков .txt', 'a')

s = str(k_ball)
name = str(name)
output.write(name)
output.write(s)
output.write('\n')
output.close()'''

pygame.quit()
