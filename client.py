import pygame
from utils.network import Network
from utils.level_interpreter import level_interpreter
from sprites.player import Player
from sprites.wall import Wall

# Setup
pygame.init()
width = 940
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Online Tank Game")

players_list = pygame.sprite.Group()
walls_list = pygame.sprite.Group()
bullets_list = pygame.sprite.Group()

# Load level 1
# should return list of free spots
walls = level_interpreter(1)
walls_list.add(walls)

# Load audio and start background music
pygame.mixer.music.load('sounds/rabadab.wav')
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)

# Initial player
player = Player("red", 0, 0)
players_list.add(player)

# Draw
def redraw_window(screen,new_players):
    screen.fill((255,255,255))
    walls_list.draw(screen)    
    bullets_list.draw(screen)
    players_list.draw(screen)
    pygame.display.flip()

# Main loop
def main():    
    clock = pygame.time.Clock()
    run = True    
    while run:
        # Handle events
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = player.shoot()
                    if bullet:
                        bullets_list.add(bullet)        

        # Move and update players and bullets
        player.move(walls_list, bullets_list)
        bullets_list.update(walls_list, players_list)

        # Draw screen with new changes
        redraw_window(screen, [player])
        clock.tick(60)
  
# Start main loop
main()