import pygame
from pygame.draw import *
import math
FPS = 30
screen = pygame.display.set_mode((400, 400))
White=[255, 255, 255]
BLACK = [ 0,   0,   0]
Red=[255, 0, 0]
Yellow = [255, 255, 0]

screen.fill(White)

#lines(screen, BLACK, True, [[100, 100], [150, 50], [250, 150], [200, 200]])
circle(screen,Yellow, [200, 200], 190)
circle(screen,Red, [115, 200], 53)
circle(screen,Red, [285, 200], 40)
circle(screen,BLACK, [125, 210], 20)
circle(screen,BLACK, [275, 210], 20)
polygon(screen, BLACK, [[(115+200)/2+10, 200-40+10], [(115+200)/2+30, 200-40-10],
                        [50, 10], [30, 30]])
rect(screen, BLACK, [160, 280, 80, 40])
polygon(screen, BLACK, [[285-40*0.5, 200-40*(3)**(0.5)/2], [285-(40+20)*0.5, 200-(40+20)*(3)**(0.5)/2],
                        [285-(40+20)*0.5 + 100*(3)**(0.5)/2, 200-(40+20)*(3)**(0.5)/2 - 100*0.5],
                        [285-40*0.5+ 100*(3)**(0.5)/2, 200-40*(3**(0.5))/2- 100*0.5]])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
