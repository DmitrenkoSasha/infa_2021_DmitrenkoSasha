import math
from random import choice, randint

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, x=40, y=450):
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

    def move(self, d_t):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        d_t: время, прошедшее между двумя тиками экрана.
        """
        self.x += self.vx
        if self.x >= 800 or self.x <= 0:
            self.vx = -self.vx
        self.y -= self.vy
        self.vy -= 9.8 * d_t
        if self.y <= 0 or self.y >= 600:
            self.vy = -0.6*self.vy
        if self.vy > 0 and self.vy * d_t < 9.8 * d_t**2/2 and self.y >= 600 - self.r:
            self.vx = 0
            self.vy = 0





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
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= obj.r**2:
            return True
        else:
            return False



class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.color = GREY
        self.lenght = 40
        self.width = 10
        self.x = 40
        self.y = 450

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        new_ball = Ball()
        new_ball.r += 5
        self.angle = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = - self.f2_power * math.sin(self.angle)
        self.f2_on = 0
        self.f2_power = 10

        return new_ball

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
        elif self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """Рисует пушку. Ствол смотрит на точку, куда наведён курсор."""
        pygame.draw.polygon(screen, self.color, [[self.x, self.y], [self.x + self.width * math.sin(self.angle), self.y - math.cos(self.angle) * self.width],
                                                 [self.x + math.cos(self.angle) * self.lenght + self.width * math.sin(self.angle),
                                                  self.y + math.sin(self.angle) * self.lenght - math.cos(self.angle) * self.width],
                                                [self.x + math.cos(self.angle) * self.lenght,self.y + math.sin(self.angle) * self.lenght]])





    def power_up(self):
        if self.f2_on == 1:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):
        """ Инициализация новой цели. """
        self.points = 0
        self.live = 1
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(20, 50)
        self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)





class Game:
    def __init__(self):
        self.balls = []
        self.bullets = 0
        self.gun = Gun()
        self.targets = []
        self.ochki = 0


    def new_target(self):
        """Удаляет старую мишень, создаёт новую"""
        target = Target()
        return target

    def draw_score(score):
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
        clock = pygame.time.Clock()
        finished = False

        while not finished:


            if self.targets == []:
                for i in range(2):
                    self.targets.append(self.new_target())
                    print(self.targets)
            screen.fill(WHITE)

            for i in range(len(self.targets)):
                self.ochki += self.targets[i].points

            textsurface = myfont.render('Your Score: ' + str(self.ochki), False,
                                        BLACK)  # Поверхность с отображением кол-ва очков
            screen.blit(textsurface, (20, 20))

            self.gun.draw()

            for i in range(len(self.targets)):
                self.targets[i].draw()

            for b in self.balls:
                b.draw()
            pygame.display.update()

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.gun.fire2_start()
                elif event.type == pygame.MOUSEBUTTONUP:
                    new_ball = self.gun.fire2_end(event)  # Новый шарик вылетает из пушки после отпускания кнопки мыши
                    self.bullets += 1
                    self.balls.append(new_ball)  # Новый шарик записан в список
                elif event.type == pygame.MOUSEMOTION:
                    self.gun.targetting(event)  # Пушка поворачивается за мышью

            for b in self.balls:
                b.move(1/FPS)
                if b.hit_test(self.target) and self.target.live == 1:
                    self.target.live = 0
                    self.target.hit()
                    self.new_target()
            self.gun.power_up()

        pygame.quit()


def main():

    global screen, myfont, targets
    targets = []
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    game = Game()
    game.mainloop()


if __name__ == '__main__':
    main()
