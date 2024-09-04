import pygame

class Floor(pygame.sprite.Sprite):
    def __init__(self,game,width,height,color, pos_x,pos_y):
        super().__init__()

        self.game = game
        self.width = width
        self.height = height
        self.color = color

        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        self.rect.x = pos_x
        self.rect.y = pos_y








