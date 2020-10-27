import pygame
import random
from utils.network import Network
from utils.level import Level
from utils.maze_solve import maze_solve
from sprites.player import Player
from sprites.wall import Wall
from sprites.power_up import PowerUp, get_type
from utils.maze_copy import maze_copy

class Game():
    def __init__(self):
        # Setup
        pygame.init()
        self.width = 1020
        self.height = 560
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Online Tank Game")

        self.players_list = None
        self.walls_list = None
        self.bullets_list = None
        self.power_up_list = None
        self.steps = None
        self.game_over_font = pygame.font.SysFont("monospace", 20)

        # Players
        self.player1 = None
        self.player2 = None
        self.points = {}
        self.points[0] = 0
        self.points[1] = 0

        self.tank_id_death_sound = None

        # Level
        self.level = None
        self.game_over_timer = None

        # Load audio and start background music
        background_music = pygame.mixer.Sound('sounds/rabadab.wav')
        background_music.set_volume(0.03)
        background_music.play(-1)
        self.reset()
        # Start main loop
        self.main()

    def reset(self):
        if self.players_list:
            for player in self.players_list:
                if not player.visible:
                    continue
                if not self.points[player.tank_id]:                    
                    self.points[player.tank_id] = 1
                else: 
                    self.points[player.tank_id] += 1

        # Load level
        self.level = Level()

        self.players_list = pygame.sprite.Group()
        self.walls_list = pygame.sprite.Group()
        self.path_list = pygame.sprite.Group()
        self.bullets_list = pygame.sprite.Group()
        self.power_up_list = pygame.sprite.Group()

        self.walls_list.add(self.level.walls)
        # Players
        free_spot = self.level.get_free_spot(False)
        if free_spot:
            self.player1 = Player("red", *free_spot, self.bullets_list, 0, "Skalle Falde")
            self.players_list.add(self.player1)
        free_spot = self.level.get_free_spot(False)
        if free_spot:
            self.player2 = Player("blue", *free_spot, self.bullets_list, 1, "Kapper")
            self.players_list.add(self.player2)

    # Draw
    def redraw_window(self, screen, new_players):
        screen.fill((255,255,255))
        self.walls_list.draw(self.screen)    
        self.power_up_list.draw(self.screen)    

        if self.steps:
            prev_step = None
            for step in self.steps:
                if prev_step:
                    pos_1 = self.level.pos_from_field(step)
                    pos_2 = self.level.pos_from_field(prev_step)
                    line_w = 5
                    pygame.draw.rect(screen, [200,0,0], [pos_1[0] + 4, pos_1[1] +  + 4, pos_2[0] - pos_1[0], pos_2[1] - pos_1[1]])
                prev_step = step
                self.level.level_list_path[step[0]][step[1]] = '#'

            # for r in range(len(self.level.level_list_path)):  # Print the maze we are working with
            #     line = ''
            #     for c in range(len(self.level.level_list_path[0])):
            #         line += str(self.level.level_list_path[r][c])
            #     print(line)
        else:
            print('Could not solve maze')

        self.bullets_list.draw(self.screen)        
        for player in self.players_list:
            if player.visible:
                player.draw(self.screen)                
        
        screen.blit(self.game_over_font.render("P1" + str("("+self.player1.power_up["type"] + ")" if self.player1.power_up else "") + ": " + str(self.points[0]) + " P2" + str("(" + self.player2.power_up["type"] + ")" if self.player2.power_up else "") + ": " + str(self.points[1]), 0, (10,10,10)), (50,20))
        pygame.display.flip()

    def player_shoot(self, player):
        print("shoot {}".format(player))
        bullets = player.shoot()
        if bullets:
            for bullet in bullets:
                self.bullets_list.add(bullet)    

    # Main loop
    def main(self):    
        clock = pygame.time.Clock()
        run = True    
        power_up_ticks = pygame.time.get_ticks()
        maze_solve_ticks = pygame.time.get_ticks()
        maze_solve_start = None
        maze_solve_end = None
        while run:
            if self.player1.shooting:
                self.player_shoot(self.player1)
            if self.player2.shooting:
                self.player_shoot(self.player2)                
            # Handle events
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                elif event.type == pygame.USEREVENT:
                    for player in self.players_list:
                        if player.tank_id == self.tank_id_death_sound["tank_id"]:
                            player.play_death_sound_step = self.tank_id_death_sound["next_step"]       
                elif event.type == pygame.KEYDOWN:     
                    if event.key == pygame.K_SPACE:    
                        self.player1.shooting = True                                          
                    elif event.key == pygame.K_m:
                        self.player2.shooting = True                    
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE and self.player1.shooting:                       
                        self.player1.shooting = False
                        if self.player1.power_up["should_explode"] == 2:
                            self.player1.power_up["should_explode"] = 3
                    elif event.key == pygame.K_m and self.player2.shooting:
                        self.player2.shooting = False
                        if self.player2.power_up["should_explode"] == 2:
                            self.player2.power_up["should_explode"] = 3
            # Add power up
            if pygame.time.get_ticks() - power_up_ticks > 500:
                spot = self.level.get_free_spot()
                if spot:
                    self.power_up_list.add(PowerUp(*spot))
                    power_up_ticks = pygame.time.get_ticks()

            # Solve maze between players
            if pygame.time.get_ticks() - maze_solve_ticks > 500:
                maze_solve_start = self.level.field_from_pos([self.player1.rect.centerx, self.player1.rect.centery])
                maze_solve_end = self.level.field_from_pos([self.player2.rect.centerx, self.player2.rect.centery])

                self.level.level_list_path = maze_copy(self.level.level_list_clean)         
                self.steps = maze_solve(maze_copy(self.level.level_list_clean), maze_solve_start, maze_solve_end)                
                maze_solve_ticks = pygame.time.get_ticks()



            # Move and update players and bullets
            for player in self.players_list:
                update_message = player.move(self.walls_list, self.bullets_list, self.power_up_list)
                if not update_message == None:                    
                    if "tank_id" in update_message:
                        self.tank_id_death_sound = update_message
                    elif "spot_free" in update_message:
                        self.level.set_free_spot(update_message["spot_free"])
                    
            self.bullets_list.update(self.walls_list, self.players_list)

            if len(self.players_list) <= 1:
                if self.game_over_timer == None:
                    print("game over")
                    self.game_over_timer = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - self.game_over_timer > 1000:
                    self.game_over_timer = None
                    self.reset()

            # Draw self.screen with new changes
            self.redraw_window(self.screen, [self.player1, self.player2])
            clock.tick(60)

game = Game()