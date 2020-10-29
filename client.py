import pygame
import random
from utils.network import Network
from utils.level import Level
from utils.maze_solve import maze_solve
from sprites.player import Player
from sprites.wall import Wall
from sprites.power_up import PowerUp, get_type
from utils.maze_copy import maze_copy
import utils.vector as vector
import math

class Game():
    def __init__(self):
        # Setup
        pygame.init()
        self.width = 1020
        self.height = 680
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
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
        sprite_groups = {'players_list': self.players_list, 'walls_list': self.walls_list, 'path_list': self.path_list, 'bullets_list': self.bullets_list, 'power_up_list': self.power_up_list}

        self.walls_list.add(self.level.walls)
        # Players
        free_spot = self.level.get_free_spot(False)
        if free_spot:
            self.player1 = Player("red", *free_spot, sprite_groups, 0, "Mads")
            self.players_list.add(self.player1)
        free_spot = self.level.get_free_spot(False)
        if free_spot:
            self.player2 = Player("blue", *free_spot, sprite_groups, 1, "Kasper")
            self.players_list.add(self.player2)

    def calc_acc_vec(self, bullet_pos, step_pos, acc, s):
        step_vec = vector.points_to_vec(bullet_pos, step_pos)
        div = vector.len_vec(step_vec) * ((s+1)**2)  
        if not div == 0:
            add = 10 / div
            return vector.dot(step_vec, add)
        return [0,0]
        


    # Draw
    def redraw_window(self, screen, new_players):
        screen.fill((255,255,255))
        self.walls_list.draw(self.screen)    
        self.power_up_list.draw(self.screen)    

        for bullet in self.bullets_list:
            if bullet.power_up['type'] == 'missile' and bullet.power_up['homing']:
                if 'steps' in bullet.power_up:
                    bullet_vec = [bullet.x_pos, bullet.y_pos]
                    bullet_pos = [bullet.rect.centerx, bullet.rect.centery]
                    acc = [0, 0]                    
                    target_player = None
                    if bullet.power_up['steps'] == [] or bullet.power_up['steps'] == False or len(bullet.power_up['steps']) <= 1:
                        least_len_vec = None
                        for player in self.players_list:
                            player_pos = [player.rect.centerx, player.rect.centery]
                            bullet_player_vec = vector.subtract(player_pos, bullet_pos)
                            len_bullet_player_vec = vector.len_vec(bullet_player_vec)                            
                            if least_len_vec == None:
                                target_player = player      
                                least_len_vec = len_bullet_player_vec                    
                            else:
                                if len_bullet_player_vec < least_len_vec:                                                                      
                                    target_player = player  
                                    least_len_vec = len_bullet_player_vec                                                                                 
                        
                        step_pos = [0, 0]                       
                        if target_player:
                            step_pos = [target_player.rect.centerx, target_player.rect.centery]
                        acc_add = self.calc_acc_vec(bullet_pos.copy(), step_pos.copy(), acc.copy(), 0)
                        acc = vector.add(acc, acc_add)             
                    else:
                        s = 0
                        for step in bullet.power_up['steps']:
                            if s < 2:
                                step_pos = self.level.pos_from_field(step)
                                acc_add = self.calc_acc_vec(bullet_pos.copy(), step_pos.copy(), acc.copy(), s)
                                acc = vector.add(acc, acc_add)
                            else:
                                break
                            s += 1


                            # Draw maze red line
                            # if prev_step:
                            #     pos_1 = self.level.pos_from_field(step)
                            #     pos_2 = self.level.pos_from_field(prev_step)
                            #     line_w = 5
                            #     pygame.draw.rect(screen, [200,0,0], [pos_1[0] + 4, pos_1[1] +  + 4, pos_2[0] - pos_1[0], pos_2[1] - pos_1[1]])
                            # prev_step = step
                            # self.level.level_list_path[step[0]][step[1]] = '#'
                    # acc *                     
                        player1_pos = self.level.field_from_pos([self.player1.rect.centerx, self.player1.rect.centery])
                        player2_pos = self.level.field_from_pos([self.player2.rect.centerx, self.player2.rect.centery])
                        end_pos = bullet.power_up['steps'][-1]
                        if end_pos == player1_pos:
                            target_player = self.player1
                        elif end_pos == player2_pos:
                            target_player = self.player2

                    if target_player:
                        step_pos = [target_player.rect.centerx, target_player.rect.centery]
                        bullet.power_up["target"] = target_player.tank_id
                    acc = vector.dot(acc, 10)
                    bullet_vec = vector.add(bullet_vec, acc)

                    new_vec_speed = vector.len_vec(bullet_vec)
                    if not new_vec_speed == 0:
                        bullet_vec = vector.dot(bullet_vec, bullet.vel / new_vec_speed)                  
                    bullet.x_pos = bullet_vec[0]
                    bullet.y_pos = -bullet_vec[1]
                                        
                    if bullet.x_pos == 0:
                        bullet.x_pos += 0.1
                    if bullet.y_pos == 0:
                        bullet.y_pos += 0.1
                    if bullet.x_pos < 0 and bullet.y_pos > 0:
                        bullet.ang = math.atan(bullet.y_pos / bullet.x_pos) * 180 / math.pi + 180
                    elif bullet.x_pos < 0 and bullet.y_pos < 0:
                        bullet.ang = math.atan(bullet.y_pos / bullet.x_pos) * 180 / math.pi - 180
                    else:
                        bullet.ang = math.atan(bullet.y_pos / bullet.x_pos) * 180 / math.pi
                else:
                    print('Could not solve maze')

        self.bullets_list.draw(self.screen)        
        for player in self.players_list:
            if player.visible:
                player.draw(self.screen)                
        
        screen.blit(self.game_over_font.render("P1" + str("("+self.player1.power_up["type"] + ")" if self.player1.power_up else "") + ": " + str(self.points[0]), 0, (156, 12, 12)), [50, 20])
        screen.blit(self.game_over_font.render("P2" + str("("+self.player2.power_up["type"] + ")" if self.player2.power_up else "") + ": " + str(self.points[1]), 0, (15,86,183)), [self.width / 2, 20])
        
        pygame.display.flip()

    def player_shoot(self, player):
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
            if pygame.time.get_ticks() - power_up_ticks > 3000:
                spot = self.level.get_free_spot()
                if spot:
                    self.power_up_list.add(PowerUp(*spot))
                    power_up_ticks = pygame.time.get_ticks()

            # Solve maze between players
            if pygame.time.get_ticks() - maze_solve_ticks > 200:
                for bullet in self.bullets_list:
                    if bullet.power_up['type'] == 'missile':
                        maze_solve_start = self.level.field_from_pos([bullet.rect.centerx, bullet.rect.centery])

                        maze_solve_end = []
                        maze_solve_end.append(self.level.field_from_pos([self.player1.rect.centerx, self.player1.rect.centery]))
                        maze_solve_end.append(self.level.field_from_pos([self.player2.rect.centerx, self.player2.rect.centery]))

                        self.level.level_list_path = maze_copy(self.level.level_list_clean)   
                        bullet.power_up['steps'] = maze_solve(maze_copy(self.level.level_list_clean), maze_solve_start, maze_solve_end)                        
                maze_solve_ticks = pygame.time.get_ticks()



            # Move and update players and bullets
            for player in self.players_list:
                update_message = player.move()
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
            clock.tick(30)

game = Game()