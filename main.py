import pygame,sys
from player import Player
from alien import Blue_Alien,Red_Alien,Green_Alien,Alien,Extra
import obstacle
from laser import Laser
from random import choice,randint


#copying another tutorial for this one, but made my own sprites and not following as intently this time just using as a guideline really
#downloaded the font from google fonts idk how that works its scary

class Game:
    def __init__(self):
        # health and score setup
        self.lives = 3
        self.live_surf = pygame.image.load("graphics/ship.png").convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * (self.lives - 1) + 10)
        self.score = 0
        self.font = pygame.font.Font("font/VT323/VT323-Regular.ttf",30)
        # player setup
        player_sprite = Player((screen_width/2,screen_height),screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #obstacle setup
        self.shape = obstacle.shape
        self.block_size = 4
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 5
        self.obstacle_x_posistions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        # 11 is the width of the pbstacle sprite
        self.create_multible_obstacles(*self.obstacle_x_posistions,x_start = (screen_width/self.obstacle_amount - self.block_size*11)/2,y_start = 480)

        # alien setup
        self.aliens = pygame.sprite.Group()
        self.cols = 8
        self.alien_setup(rows = 6, cols = self.cols,x_start = (screen_width/(self.cols+3) - 48)/2)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()
        
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400,600)

    def create_obstacle(self,x_start,y_start,offset_x):
        for row_index,row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                if col == "X":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size,(153,0,0),x,y)
                    self.blocks.add(block)

    def create_multible_obstacles(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_obstacle(x_start,y_start,offset_x)

    def alien_setup(self,rows,cols,x_start):
        for row_index in range(rows):
            for col_index in range(cols):
                x = x_start + col_index * (screen_width / (cols+3))
                y = 100 + row_index * 48

                if row_index == 0:
                    alien_sprite = Blue_Alien(x,y)
                elif row_index >= 1 and row_index <=2:
                    alien_sprite = Green_Alien(x,y)
                else:
                    alien_sprite = Red_Alien(x,y)
                self.aliens.add(alien_sprite)

    def alien_posistion_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        random_alien = choice(self.aliens.sprites())
        laser_sprite = Laser(random_alien.rect.center,screen_height,6)
        self.alien_lasers.add(laser_sprite)

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(["right","left"]),screen_width))
            self.extra_spawn_time = randint(400,600)

    def collision_checks(self):
        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    self.score += 500
                    laser.kill()

        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)
                if pygame.sprite.spritecollide(alien,self.player,False):
                    pygame.quit()
                    sys.exit()
        else:
            pygame.quit()
            sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * self.live_surf.get_size()[0])
            screen.blit(self.live_surf,(x,8))

    def display_score(self):
        score_surf = self.font.render(f"score: {self.score}",False,"white")
        score_rect = score_surf.get_rect(topleft = (10,5))
        screen.blit(score_surf,score_rect)
        
    def run(self):
        
        self.alien_posistion_checker()
        self.aliens.update(self.alien_direction)
        self.extra_alien_timer()
        self.collision_checks()

        self.extra.update()

        
        self.alien_lasers.update()

        self.player.update()
        
        self.player.draw(screen)
        self.player.sprite.lasers.draw(screen)

        self.blocks.draw(screen)

        self.aliens.draw(screen)

        self.alien_lasers.draw(screen)

        self.extra.draw(screen)

        self.display_lives()
        self.display_score()
        
    
if __name__ == "__main__":
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER  = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

        screen.fill((30,30,30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
                

