import pygame
from pygame.draw import *
from math import pi

FPS = 30
screen = pygame.display.set_mode((800, 800))

LightCyan=[224, 255, 255]
MediumSeaGreen=[60, 179, 113]
DeepPink=[255, 20, 147]
LightGrey=[211, 211, 211]
Gray=[128, 128, 128]
Red=[255, 0, 0]
White=[255, 255, 255]
Maroon=[128, 0, 0]
BLACK = [ 0,   0,   0]
Gold=[255, 215, 0]

screen.fill(LightCyan)
rect(screen, MediumSeaGreen, [0, 400, 800, 800])
ellipse(screen, Gray, [200, 250, 150, 300])
circle(screen, LightGrey, [275, 225], 55)
polygon(screen, DeepPink, [[500, 225], [400, 550], [600, 550]])
circle(screen, LightGrey, [500, 225], 55)
lines(screen, BLACK, False, [[450, 550], [430, 680], [420, 680]], 3)
lines(screen, BLACK, False, [[550, 550], [570, 680], [580, 680]], 3)
lines(screen, BLACK, False, [[250, 550], [230, 680], [220, 680]], 3)
lines(screen, BLACK, False, [[300, 550], [320, 680], [310, 680]], 3)
line(screen, BLACK, [345, 350], [400, 480], 3)
line(screen, BLACK, [460, 350], [400, 480], 3)
line(screen, BLACK, [205, 350], [130, 480], 3)
lines(screen, BLACK, False, [[540, 350], [630, 380], [720, 300]], 3)
line(screen, BLACK, [680, 380], [730, 250], 3)
polygon(screen, Red, [[730, 250], [720, 200], [770, 215]])
polygon(screen, Maroon, [[130, 480], [100, 400], [65, 435]])
circle(screen, Red, [735, 204], 15)
circle(screen, Red, [757, 211], 15)
circle(screen, Gold, [91, 410], 15)
circle(screen, Red, [76, 425], 15)
circle(screen, White, [77, 405], 15)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()







