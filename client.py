import pygame
from network import Network
from player import Player
from colors import *

width = 500
height = 500


win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')

# client_number = 0
#
# def read_Pos(str_pos):
#     str_pos = str_pos.split(',')
#     return int(str_pos[0]), int(str_pos[1])
#
#
# def make_Pos(tup_pos):
#     return str(tup_pos[0]) + ',' + str(tup_pos[1])


def redrawWindow(win, player, player_2):
    win.fill(WHITE)
    player.draw(win)
    player_2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    player = n.getP()

    print(n.getP())
    clock = pygame.time.Clock()
    while run:

        clock.tick(60)
        player_2 = n.send(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        player.move()
        redrawWindow(win, player, player_2)


main()
