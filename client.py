import pygame
import random
from utils.network import Network
from utils.level import Level
from sprites.player import Player
from sprites.wall import Wall
from sprites.power_up import PowerUp

class Game():
    def __init__(self):
        # Setup
        pygame.init()
        self.width = 940
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Online Tank Game")

        self.players_list = None
        self.walls_list = None
        self.bullets_list = None
        self.power_up_list = None

        self.game_over_font = pygame.font.SysFont("monospace", 20)

        # Players
        self.player1 = None
        self.player2 = None
        self.points = {}
        self.points[0] = 0
        self.points[1] = 0

        # Level
        self.level = None
        self.game_over_timer = None

        # Load audio and start background music
        pygame.mixer.music.load('sounds/rabadab.wav')
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)
        self.reset()
        # Start main loop
        self.main()

    def reset(self):
        if self.players_list:
            for player in self.players_list:
                if not self.points[player.tank_id]:                    
                    self.points[player.tank_id] = 1
                else: 
                    self.points[player.tank_id] += 1

        # Load level
        self.level = Level()

        self.players_list = pygame.sprite.Group()
        self.walls_list = pygame.sprite.Group()
        self.bullets_list = pygame.sprite.Group()
        self.power_up_list = pygame.sprite.Group()

        self.walls_list.add(self.level.walls)
        # Players
        free_spot = self.level.get_free_spot(False)
        if free_spot:
            self.player1 = Player("red", *free_spot, 0)
            self.players_list.add(self.player1)
        free_spot = self.level.get_free_spot(False)
        if free_spot:
            self.player2 = Player("blue", *free_spot, 1)
            self.players_list.add(self.player2)

    # Draw
    def redraw_window(self, screen ,new_players):
        screen.fill((255,255,255))
        self.walls_list.draw(self.screen)    
        self.power_up_list.draw(self.screen)    
        self.bullets_list.draw(self.screen)
        self.players_list.draw(self.screen)
        screen.blit(self.game_over_font.render("P1: " + str(self.points[0]) + " P2: " + str(self.points[1]), 0, (10,10,10)), (50,20))
        pygame.display.flip()

    # Main loop
    def main(self):    
        clock = pygame.time.Clock()
        run = True    
        power_up_ticks = pygame.time.get_ticks()
        while run:
            # Handle events
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet = self.player1.shoot()
                        if bullet:
                            self.bullets_list.add(bullet)        
                    elif event.key == pygame.K_m:
                        bullet = self.player2.shoot()
                        if bullet:
                            self.bullets_list.add(bullet)      
            # Add power up
            if pygame.time.get_ticks() - power_up_ticks > 3000:
                spot = self.level.get_free_spot()
                if spot:
                    self.power_up_list.add(PowerUp(*spot))
                    power_up_ticks = pygame.time.get_ticks()

            # Move and update players and bullets
            self.player1.move(self.walls_list, self.bullets_list)
            self.player2.move(self.walls_list, self.bullets_list)
            self.bullets_list.update(self.walls_list, self.players_list)

            if len(self.players_list) <= 1:
                if self.game_over_timer == None:
                    print("game over")
                    self.game_over_timer = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - self.game_over_timer > 3000:
                    self.game_over_timer = None
                    self.reset()

            # Draw self.screen with new changes
            self.redraw_window(self.screen, [self.player1, self.player2])
            clock.tick(60)

game = Game()