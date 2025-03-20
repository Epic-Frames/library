import pygame as pg
import random

class Enemy():
    def __init__(self, enemyType, x, y, width, height, speed, health, sourceImage, direction, num1, num2):
        self.type = enemyType
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health

        if self.type == "Spider":
            self.x1 = num1
            self.x2 = num2
        elif self.type == "Lava Bubbles":
            self.y1 = num1
            self.y2 = num2
        elif self.type == "Watcher":
            self.x1 = num1
            self.x2 = num2

        self.direction = direction

        self.sourceImage = sourceImage
    
        self.image = pg.image.load(self.sourceImage)
        self.image = pg.transform.scale(self.image, (self.width, self.height))

        self.mask = pg.mask.from_surface(self.image)


    def move(self):
        if self.type == "Spider":
            self.x += self.speed * self.direction
            if self.x <= self.x1:
                self.direction = 1
            elif self.x >= self.x2:
                self.direction = -1
        elif self.type == "Lava Bubbles":
            self.y += self.speed * self.direction
            if self.y <= self.y1:
                self.direction = 1
            elif self.y >= self.y2:
                self.direction = -1
        elif self.type == "Watcher":
            self.x += self.speed * self.direction
            if self.x <= self.x1:
                self.direction = 1
            elif self.x >= self.x2:
                self.direction = -1
            if random.randint(0, 1000) == 1:
                return True
        return False

    
    # def check_alive(self):
    #     if self.health <= 0:
    #         return False
    #     return True
    

    # def clear_enemy(self):
    #     self.x = -500
    

    # def take_damage(self, damage):
    #     self.health -= damage
    

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))