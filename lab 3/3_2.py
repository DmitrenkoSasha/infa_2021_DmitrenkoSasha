import pygame
from pygame.draw import *
from pygame.transform import *

FPS = 30
screen = pygame.display.set_mode((1440, 800))
#----Творческая часть---
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
def main(): # эта функция рисует основную часть, повторяющуюся 2 раза
    rect(screen, MediumSeaGreen, [0, 400, 800, 800]) #трава
    ellipse(screen, Gray, [200, 250, 150, 300]) #туловище мальчика
    circle(screen, LightGrey, [275, 225], 55) #голова мальчика
    polygon(screen, DeepPink, [[500, 225], [400, 550], [600, 550]]) #туловище девочки
    circle(screen, LightGrey, [500, 225], 55) #голова девочки
    lines(screen, BLACK, False, [[450, 550], [430, 680], [420, 680]], 3) #правая нога девочки
    lines(screen, BLACK, False, [[550, 550], [570, 680], [580, 680]], 3)#её левая нога 
    lines(screen, BLACK, False, [[250, 550], [230, 680], [220, 680]], 3)#правая нога мальчика
    lines(screen, BLACK, False, [[300, 550], [320, 680], [310, 680]], 3)#его левая нога
    line(screen, BLACK, [345, 350], [400, 480], 3)#левая рука мальчика
    line(screen, BLACK, [460, 350], [400, 480], 3)#правая рука девочки
    line(screen, BLACK, [205, 350], [130, 480], 3)#правая рука мальчика
    lines(screen, BLACK, False, [[540, 350], [630, 380], [720, 300]], 3)#левая рука девочки
    
main() #рисует слева мальчика и девочку

screen.blit(pygame.transform.flip(screen, True, False), dest=(0, 0)) # отображает нарисованное вправо

main() #ещё рисует обоих слева 
line(screen, BLACK, [720, 300], [725, 180], 1) #палка под морож.
line(screen, BLACK, [1310, 480], [1310, 300], 1) #палка под сердечко


#Создаём поверхность
def newsurf(x, y):
    surf = pygame.Surface((x, y), pygame.SRCALPHA, 32)
    surf = surf.convert_alpha()
    return(surf)

#Мороженное:
def moroghenoe(surf, x, y):
    polygon(surf, Maroon, [[150, 150], [100, 70], [65, 105]])
    circle(surf, Gold, [91, 80], 15)
    circle(surf, Red, [76, 95], 15)
    circle(surf, White, [77, 75], 15)
    screen.blit(surf, (x, y))

surf1 = newsurf(150, 150)    
moroghenoe(surf1, 0, 330)#у парня в руке

surf2 = newsurf(150, 150)
moroghenoe(surf2, 575, 30)#на палочке

surf3 = newsurf(150,250)#готовим поверхность под сердечко и рисуем его
circle(surf3, Red, [115, 204], 15)
circle(surf3, Red, [137, 211], 15)
polygon(surf3, Red, [[110, 250], [100, 200], [150, 215]])

rot = pygame.transform.rotate(surf3, 45)#поворачиваем поверхность
rot_rect = rot.get_rect(center=(1200, 235))#ориентируем поверхность на рисунке
screen.blit(rot, rot_rect)
pygame.display.update()

# Увеличиваем мороженное вдвое
scale = pygame.transform.scale(
        surf2, (surf2.get_width() * 2,
                   surf2.get_height() * 2))
scale_rect = scale.get_rect(
        center=(575, 30))
screen.blit(scale, scale_rect)


pygame.display.update()
#----Обязательная часть---
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
