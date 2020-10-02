#!/path/to/python
# Filename: client.py

import pygame
from network import Network
from player import Player

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Online Tank Game")

all_sprites_list = pygame.sprite.Group()

player = Player("red", 100, 100)
player.set_coords(200, 300)

all_sprites_list.add(player)

clock = pygame.time.Clock()

def redrawWindow(screen,new_players):
    screen.fill((255,255,255))
    all_sprites_list.draw(screen)    
    pygame.display.flip()


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

        # all_sprites_list.update()

        player.update()

        player.move()
        redrawWindow(screen, [player])
        clock.tick(60)
        
    n = Network()        
    print("Connected to server: {}:{}".format(n.server, n.port))
    p, players = n.getP()
    print(p)

    while run:
        clock.tick(60)
        # print((players[p].x_pos, players[p].y_pos))
        new_players = n.send([p, players[p]])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        players[p].move()
        redrawWindow(screen, new_players)
  
main()