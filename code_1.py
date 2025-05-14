# import thư viện

import pygame
from pygame.locals import *

pygame.init()

background  = pygame.image.load("./asset/img/background.png")
ground = pygame.image.load("./asset/img/ground.png")

clock = pygame.time.Clock()

# game variables
fps = 60
ground_scroll = 0 #điểm bắt đầu của mặt đất
scroll_speed = 4 # mỗi lần mặt đất sẽ di chuyển 4 pixel

background_scroll = 0
bg_scroll_speed = 0.03


screen_width = 864
screen_height = 639
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Flappy Bird")

run = True

while run:

    clock.tick(fps)

    screen.blit(background, (background_scroll,0))
    screen.blit(ground, (ground_scroll,539))
    ground_scroll -= scroll_speed # di chuyển mặt đất về bên trái
    background_scroll -= bg_scroll_speed

    if(abs(ground_scroll) > 20):
        ground_scroll = 0
    if(abs(background_scroll) > 325):
        background_scroll = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    pygame.display.update()            

pygame.quit()