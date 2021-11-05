import pygame
import math
from random import choice, randint


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


class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.color1 = GREY
        self.color2 = LIMEGREEN
        self.lenght = 80
        self.width = 10
        self.x = 60
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
        try:
            self.angle = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
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
        #pygame.image.load("C:\Users\пк\Pictures\Фото на студенческий.JPG")

    def power_up(self):
        if self.f2_on == 1:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

#class Ball_target(Target):
#class Poly_target(Target):
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
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy
        и стен по краям невидимого окна (размер невидимого окна 400х600).
        """
        self.x += self.vx
        if self.x >= 800 or self.x <= 400:
            self.vx = -self.vx
        self.y -= self.vy
        if self.y <= self.r or self.y >= 600-self.r:
            self.vy = -self.vy

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        """Просто рисуем несколько кругов друг на друге - это наша мишень"""
        pygame.draw.circle(screen, self.color1, (self.x, self.y), self.r)
        pygame.draw.circle(screen, self.color2, (self.x, self.y), self.r * 4 / 5)
        pygame.draw.circle(screen, self.color1, (self.x, self.y), self.r * 3 / 5)
        pygame.draw.circle(screen, self.color2, (self.x, self.y), self.r * 2 / 5)
        pygame.draw.circle(screen, self.color3, (self.x, self.y), self.r * 1 / 5)



class Game:
    """Отвечает за события с пушкой, мячиками и мишенями на экране"""
    def __init__(self):
        self.balls = []
        self.bullets = 0
        self.gun = Gun()
        self.targets = []
        self.ochki = 0
        self.FPS = 30

    def change_target(self, t):
        """Удаляет старую мишень, создаёт новую"""
        self.targets.remove(t)
        self.targets.append(Target())

    def remove_ball(self, ball):
        """Удаляет мячик"""
        ball.cut_livetime(1/self.FPS)
        if ball.livetime <=0 :
            self.balls.remove(ball)





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
        clock = pygame.time.Clock()
        finished = False

        while not finished:

            if len(self.targets) < 2:
                for i in range(2):
                    self.targets.append(Target())

            screen.fill(WHITE)

            self.draw_score(self.ochki)
            self.gun.draw()

            for b in self.balls:
                b.draw()
            for target in self.targets:
                target.draw()
            pygame.display.update()

            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.gun.fire2_start()
                elif event.type == pygame.MOUSEBUTTONUP:
                    new_ball = self.gun.fire2_end(event)  # Новый шарик вылетает из пушки после отпускания кнопки мыши
                    self.bullets += 1  # FIXME Зачем эти пули?
                    self.balls.append(new_ball)  # Новый шарик записан в список
                elif event.type == pygame.MOUSEMOTION:
                    self.gun.targetting(event)  # Пушка поворачивается за мышью

            for b in self.balls:
                b.move(1/self.FPS)
                if b.vx == 0 and b.vy == 0:
                    self.remove_ball(b)
                for target in self.targets:
                    if b.hit_test(target) and target.live == 1:
                        target.live = 0
                        target.hit()
                        self.ochki += target.points
                        self.change_target(target)

            for target in self.targets:
                target.move()

            self.gun.power_up()  # Нужно, чтобы пушка окрасилась в серый

        pygame.quit()


def main():

    global screen, myfont
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    game = Game()
    game.mainloop()


if __name__ == '__main__':
    main()
