import pygame
import os
import sys


def load_images(path, suffix, lst):

    for image in os.listdir(str(path)):
        if image.endswith(str(suffix)):
            lst.append(pygame.image.load(str(path) + str(image)).convert_alpha())


class Buttons(pygame.sprite.Sprite):
    def __init__(self,game,x,y,image,alpha,fade):
        super().__init__()
        self.game = game
        self.image = image
        self.alpha = alpha
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.hover = False
        self.alpha_velocity = 0.2
        self.fade = fade




    def update(self):
        self.game.screen.blit(self.image,(self.rect.x,self.rect.y))






        print(self.alpha_velocity)

        if self.rect.collidepoint(self.game.mouse_pos):
            self.hover = True
        else:
            self.hover = False


