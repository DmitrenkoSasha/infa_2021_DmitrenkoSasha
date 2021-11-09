import pygame
import math
# import sys, os
from random import choice, randint
from operator import itemgetter


RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
LIMEGREEN = (50, 205, 50)
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, LIMEGREEN, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

class Gun:  # Необходимо создать надкласс пушка, и два подкласса пушка1,2 Они будут смотреть друг на друга и стрелять.
    # Вторая будет стрелять автоматически (рандомно)
    def __init__(self, x=60, y=450):
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.color1 = GREY
        self.color2 = LIMEGREEN
        self.lenght = 80
        self.width = 10
        self.x = x
        self.y = y
        self.vx = 3
        self.vy = 3
        self.motion_x = 'STOP'
        self.motion_y = 'STOP'

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        new_ball = Ball(self.x, self.y)
        new_ball.r += 5
        self.angle = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = - self.f2_power * math.sin(self.angle)
        self.f2_on = 0
        self.f2_power = 10

        return new_ball

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        try:
            self.angle = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))
        except ZeroDivisionError:
            print("Деление на ноль")
        if self.f2_on:
            self.color1 = RED
            self.color2 = RED
        else:
            self.color1 = GREY
            self.color2 = LIMEGREEN

    def draw(self):
        """Рисует пушку. Ствол смотрит на точку, куда наведён курсор."""
        pygame.draw.rect(screen, self.color2, (self.x - 60, self.y + 20, 120, 50))
        pygame.draw.rect(screen, self.color2, (self.x - 30, self.y, 60, 20))
        pygame.draw.circle(screen, self.color2, [self.x,  self.y], 5)
        pygame.draw.polygon(screen, self.color1, [[self.x, self.y], [self.x + self.width * math.sin(self.angle),
                                                                     self.y - math.cos(self.angle) * self.width],
                                                  [self.x + math.cos(self.angle) * self.lenght + self.width * math.sin(
                                                     self.angle),
                                                  self.y + math.sin(self.angle) * self.lenght - math.cos(
                                                      self.angle) * self.width],
                                                  [self.x + math.cos(self.angle) * self.lenght,
                                                  self.y + math.sin(self.angle) * self.lenght]])
        '''dog_surf = pygame.image.load("bomb.jpg")
        dog_rect = dog_surf.get_rect(bottomright=(100, 100))

        screen.blit(dog_surf, dog_rect)'''

    def power_up(self):
        if self.f2_on == 1:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def move_gun(self):
        """Движение пушки с залипанием клавиш"""
        if self.motion_x == 'LEFT':
            self.x -= self.vx
            if self.motion_y == 'UP':  # Именно вверх, так как 0 по OY сверху
                self.y -= self.vy
            elif self.motion_y == 'DOWN':
                self.y += self.vy
        elif self.motion_x == 'RIGHT':
            self.x += self.vx
            if self.motion_y == 'UP':  # Именно вверх, так как 0 по OY сверху
                self.y -= self.vy
            elif self.motion_y == 'DOWN':
                self.y += self.vy
        elif self.motion_y == 'DOWN':
            self.y += self.vy
        elif self.motion_y == 'UP':  # Именно вверх, так как 0 по OY сверху
            self.y -= self.vy

class Enemy_Gun:
    "Вражеская пушка, которая зависит пушки игрока. Эта пушка нуждается в координатах главной пушки, чтобы знать, куда стрелять"
    def __init__(self):
        self.f2_power = 30
        self.f2_on = 0
        self.x = randint(WIDTH//2, WIDTH)
        self.y = randint(0, HEIGHT)
        self.angle = 1
        self.color1 = BLACK
        self.color2 = GREY
        self.lenght = 40  # длина ствола
        self.width = 5  # толщина ствола
        self.fire_time = 5  # промежуток времени, через который пушка стреляет


    def fire2_end(self, x_our, y_our):
        """Выстрел мячом.

        Происходит при истечении промежутка времени fire_time.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        :x_our, y_our: координаты нашей пушки (точка, где начинается дуло)
        """
        new_ball = Ball(self.x, self.y)
        new_ball.r += 5
        self.angle = math.atan2((y_our - new_ball.y), (x_our - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = - self.f2_power * math.sin(self.angle)
        self.f2_on = 0

        return new_ball

    def draw(self, x_our, y_our):
        """Рисует пушку. Ствол смотрит на пушку игрока - нашу пушку"""
        self.angle = math.atan2((y_our - self.y), (x_our - self.x))
        pygame.draw.rect(screen, self.color2, (self.x - 30, self.y + 10, 60, 25))
        pygame.draw.rect(screen, self.color2, (self.x - 15, self.y, 30, 10))
        pygame.draw.circle(screen, self.color2, [self.x,  self.y], 5)
        pygame.draw.polygon(screen, self.color1, [[self.x, self.y], [self.x + self.width * math.sin(self.angle),
                                                                     self.y - math.cos(self.angle) * self.width],
                                                  [self.x + math.cos(self.angle) * self.lenght + self.width * math.sin(
                                                     self.angle),
                                                  self.y + math.sin(self.angle) * self.lenght - math.cos(
                                                      self.angle) * self.width],
                                                  [self.x + math.cos(self.angle) * self.lenght,
                                                  self.y + math.sin(self.angle) * self.lenght]])


class Ball:
    def __init__(self, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.livetime = 0.5

    def move(self, d_t):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).

        d_t: время, прошедшее между двумя тиками экрана.
        """
        self.x += self.vx
        self.y -= self.vy

        if self.y + self.r < 600:
            self.vy -= 9.81*d_t
        if self.x + self.r >= 800:
            self.vx = -0.8*self.vx
            self.x = 800 - self.r
        if self.x - self.r <= 0:
            self.vx = -0.8 * self.vx
            self.x = self.r
        if self.y + self.r >= 600:
            self.vy = -0.8 * self.vy
        if self.y + self.r <= 0:
            self.y = self.r
            self.vy = -0.8*self.vy
        if self.vy < 9.81*d_t and self.y + self.r >= 600:
            self.vx = 0
            self.vy = 0
            self.y = 600 - self.r

    def cut_livetime(self, d_t):
        """Уменьшает оставшееся время отображения на экране"""
        self.livetime -= d_t

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r)

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (obj.r+self.r)**2


class Target:
    def __init__(self):
        """ Инициализация новой цели. """
        self.points = 0
        self.live = 1
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(20, 50)
        self.vx = randint(10, 20)
        self.vy = randint(10, 20)
        self.color1 = RED
        self.color2 = BLACK
        self.color3 = YELLOW

    def move(self):
        pass

    def draw(self):
        pass


class Ball_target(Target):
    def __init__(self):
        """ Инициализация нового шарика-мишени """
        super(Ball_target, self).__init__()

    def hit(self, points=2):
        """Попадание в цель."""
        self.points += points

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy
        и стен по краям невидимого окна (размер невидимого окна 400х600).
        """
        self.x += self.vx
        if self.x >= 800 or self.x <= 400:
            self.vx = -self.vx
        self.y -= self.vy
        if self.y <= self.r or self.y >= 600 - self.r:
            self.vy = -self.vy

    def draw(self):
        """Просто рисуем несколько кругов друг на друге - это наша мишень"""
        pygame.draw.circle(screen, self.color1, (self.x, self.y), self.r)
        pygame.draw.circle(screen, self.color2, (self.x, self.y), self.r * 4 / 5)
        pygame.draw.circle(screen, self.color1, (self.x, self.y), self.r * 3 / 5)
        pygame.draw.circle(screen, self.color2, (self.x, self.y), self.r * 2 / 5)
        pygame.draw.circle(screen, self.color3, (self.x, self.y), self.r * 1 / 5)


class Poly_target(Target):
    def __init__(self):
        """ Инициализация нового многоугольника-мишени """
        super(Poly_target, self).__init__()
        self.amount_vertex = randint(3, 7)
        self.live_time_poly = 3  # Время отображения одного многоугольника в секундах

    def hit(self, points=1):
        """Попадание в цель."""
        self.points += points

    def draw(self):
        """
        Рисует один правильный многоугольник.
        position: координаты центра фигуры в скобках, например (200, 400)
        """
        n = self.amount_vertex
        pygame.draw.polygon(screen, self.color1, [
            (self.x + self.r * math.cos(2 * math.pi * i / n), self.y + self.r * math.sin(2 * math.pi * i / n))
            for i in range(n)
        ])

    def poly_cut_livetime(self, d_t):
        self.live_time_poly -= d_t


class Mina:
    def __init__(self):
        self.x = randint(0, WIDTH)
        self.y = randint(0, HEIGHT)
        self.size = randint(10, 15)
        self.amount = 2

    def draw(self):
        pass

    def check(self):
        pass


class Game:
    """Отвечает за события с пушкой, мячиками и мишенями на экране"""
    def __init__(self):
        self.balls = []  # Список шариков-снарядов
        self.bullets = 0
        self.gun = Gun()
        self.enemy = Enemy_Gun()
        self.targets = []
        self.ochki = 0
        self.FPS = 30
        self.amount_poly = 2
        self.amount_balls = 2

    def first_targets(self):
        """ прорисовка первых целей"""
        for i in range(self.amount_poly):
            self.targets.append(Poly_target())
        for i in range(self.amount_balls):
            self.targets.append(Ball_target())

    def change_target(self, t):
        """Удаляет старую мишень, создаёт новую"""
        self.targets.remove(t)
        if type(t) is Ball_target:
            self.targets.append(Ball_target())
        elif type(t) is Poly_target:
            self.targets.append(Poly_target())

    def remove_ball(self, ball):
        """Уменьшает жизнь упавшего мячика, а потом удаляет его"""
        ball.cut_livetime(1/self.FPS)
        if ball.livetime <= 0:
            self.balls.remove(ball)

    def change_poly(self, poly):
        """Заменяет мишень-многоугольник"""
        poly.poly_cut_livetime(1/self.FPS)
        if poly.live_time_poly <= 0:
            self.targets.remove(poly)
            self.targets.append(Poly_target())

    def repit_actions(self):
        """Включает в себя общие строчки кода, которые должны быть прописаны
        как до главного цикла, чтобы отобразить первые фигуры, так и в нём самом.
        Экономия места"""
        screen.fill(WHITE)

        self.draw_score(self.ochki)
        self.gun.draw()
        self.enemy.draw(self.gun.x, self.gun.y)

        for b in self.balls:
            b.draw()
        for target in self.targets:
            target.draw()
        pygame.display.update()

        clock.tick(self.FPS)


    def draw_score(self, score):
        """
        Пишет в левом верхнем углу экрана счёт игрока
        :param score: Score
        :type score: float
        :return: None
        :rtype: None
        """
        textsurface = myfont.render('Your Score: ' + str(score), False,
                                    BLACK)  # Поверхность с отображением кол-ва очков
        screen.blit(textsurface, (20, 20))



    def mainloop(self):
        finished = False

        self.first_targets()
        self.repit_actions()


        while not finished:
            self.repit_actions()

            self.enemy.fire_time -= 1/self.FPS
            if self.enemy.fire_time <= 0:
                self.enemy.fire_time = 5
                new_ball = self.enemy.fire2_end(self.gun.x, self.gun.y)
                self.balls.append(new_ball)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                    self.sort_results(name, self.ochki)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.gun.fire2_start()
                elif event.type == pygame.MOUSEBUTTONUP:
                    new_ball = self.gun.fire2_end(event) # Новый шарик вылетает из пушки после отпускания кнопки мыши
                    self.bullets += 1  # FIXME Зачем эти пули?
                    self.balls.append(new_ball)  # Новый шарик записан в список
                elif event.type == pygame.MOUSEMOTION:
                    self.gun.targetting(event)  # Пушка поворачивается за мышью
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.gun.motion_y = 'UP'
                    elif event.key == pygame.K_DOWN:
                        self.gun.motion_y = 'DOWN'
                    elif event.key == pygame.K_LEFT:
                        self.gun.motion_x = 'LEFT'
                    elif event.key == pygame.K_RIGHT:
                        self.gun.motion_x = 'RIGHT'
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        self.gun.motion_x = 'STOP'
                    elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                        self.gun.motion_y = 'STOP'

            self.gun.move_gun()

            for b in self.balls:
                b.move(1/self.FPS)
                if b.vx == 0 and b.vy == 0:
                    self.remove_ball(b)
                for target in self.targets:
                    if b.hit_test(target) and target.live == 1 and b in self.balls:
                        target.live = 0
                        target.hit()
                        self.ochki += target.points
                        self.balls.remove(b)
                        self.change_target(target)

            for target in self.targets:
                #target.move()
                if type(target) is Poly_target:
                    self.change_poly(target)

            self.gun.power_up()  # Нужно, чтобы пушка окрасилась в серый



        pygame.quit()

    def sort_results(self, text, score):
        """вносит результаты игрока в таблицу результатов 'scores.txt' и отсортировывает её,
        а затем записывает полученное в таблицу 'table.txt'
        :param text: имя игрока
        :param score: счёт игрока
        :return:  'scores.txt' & 'table.txt'
        """
        table = open('table_gun.txt', 'w')  # Будет с сортированными данными
        with open('scores_gun.txt', 'a') as output:  # Здесь данные в хронометрическом порядке
            print(text, '"', score, file=output)
        with open('scores_gun.txt', 'r') as f:
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

def main():

    global screen, myfont, clock, name, scores
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    name = input('Введите своё имя: ')
    scores = []

    game = Game()
    game.mainloop()


if __name__ == '__main__':
    main()
