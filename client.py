#!/path/to/python
# Filename: client.py

import pygame
from network import Network
from player import Player
import globals

pygame.init()
width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Online Tank Game")

all_sprites_list = pygame.sprite.Group()

players_list = pygame.sprite.Group()
bullets_list = pygame.sprite.Group()

player = Player("red", 100, 100)
player.set_coords(200, 300)

players_list.add(player)

clock = pygame.time.Clock()

def redrawWindow(screen,new_players):
    screen.fill((255,255,255))
    # all_sprites_list.draw(screen)
    bullets_list.draw(screen)
    players_list.draw(screen)
    pygame.display.flip()

def main():    
    run = True
    bad_move = pygame.mixer.Sound('sounds/bad_move.wav')
    bad_move.set_volume(0.5)
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bad_move.play()
                    bullet = player.shoot()
                    all_sprites_list.add(bullet)
                    bullets_list.add(bullet)        

        all_sprites_list.update()
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