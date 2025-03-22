import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_index = 0

    def animation_state(self):
        self.animation_index = (self.animation_index + 0.04) % len(self.frames)
        self.image = self.frames[int(self.animation_index)]

    def update(self,direction):
        self.rect.x += direction
        self.animation_state()

class Blue_Alien(Alien):
    def __init__(self,x,y):
        super().__init__()
        frame_1 = pygame.image.load("graphics/blue.png").convert_alpha()
        frame_2 = pygame.image.load("graphics/blue_2.png").convert_alpha()
        self.frames = [frame_1,frame_2]
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(topleft = (x,y))
        self.value = 300

class Green_Alien(Alien):
    def __init__(self,x,y):
        super().__init__()
        frame_1 = pygame.image.load("graphics/green.png").convert_alpha()
        frame_2 = pygame.image.load("graphics/green_2.png").convert_alpha()
        self.frames = [frame_1,frame_2]
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(topleft = (x,y))
        self.value = 200

class Red_Alien(Alien):
    def __init__(self,x,y):
        super().__init__()
        frame_1 = pygame.image.load("graphics/red.png").convert_alpha()
        frame_2 = pygame.image.load("graphics/red_2.png").convert_alpha()
        self.frames = [frame_1,frame_2]
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(topleft = (x,y))
        self.value = 100

class Extra(pygame.sprite.Sprite):
    def __init__(self,side,screen_width):
        super().__init__()
        self.image = pygame.image.load("graphics/UFO.png").convert_alpha()

        if side == "right":
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft = (x,70))

    def update(self):
        self.rect.x += self.speed
