import pygame as pg

class Player():
    def __init__(self, x, y, width, height, speed, health, sourceImage, footY, gravity, jumpPower, sidePadding):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.sourceImage = sourceImage
        self.xChange = 0
        self.yChange = 0
        self.gravity = gravity
        self.jumpPower = jumpPower

        self.sidePadding = sidePadding
        self.jumps_available = 2


        self.jumping = False
        self.on_ground = True

        self.freezeFrame = 0

        if y is None:
            self.y = footY - self.height
            self.footY = footY
        elif footY is None:
            self.footY = self.y + self.height

        self.image = pg.image.load(self.sourceImage)
        self.image = pg.transform.scale(self.image, (self.width, self.height))

        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()


    def check_walk(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] and keys[pg.K_RIGHT]:
            pass
        elif keys[pg.K_LEFT]:
            self.xChange = -self.speed
        elif keys[pg.K_RIGHT]:
            self.xChange = self.speed
        
        if self.on_ground:
            self.jumps_available = 2

        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                if self.jumps_available > 0:
                    self.jumping = True
                    self.yChange = self.jumpPower
                    self.on_ground = False
                    self.jumps_available -= 1
    

    def collision(self, tileList):
        collided = False
        ifDead = False
        ifWin = False
        self.rect.x = self.x
        self.rect.y = self.y

        self.rect.y += self.yChange
        for tile in tileList:
            if self.rect.colliderect(tile[1]):
                collided = True
                if tile[2] == "Assets/lava.jpeg":
                    ifDead = True
                if tile[2] == "Assets/diamond.png":
                    ifWin = True
                if self.yChange > 0:    # Moving down
                    self.rect.bottom = tile[1].top
                    self.y = self.rect.y
                    self.yChange = 0
                    self.on_ground = True
                elif self.yChange < 0:  # Moving up
                    self.rect.top = tile[1].bottom
                    self.y = self.rect.y
                    self.yChange = 0
        
        self.rect.x = self.x
        self.rect.y = self.y

        self.rect.x += self.xChange
        for tile in tileList:
            if self.rect.colliderect(tile[1]):
                if tile[2] == "Assets/lava.jpeg":
                    ifDead = True
                if tile[2] == "Assets/diamond.png":
                    ifWin = True
                if self.xChange > 0:    # Moving right
                    self.rect.right = tile[1].left
                    self.x = self.rect.x
                    self.xChange = 0
                    self.on_ground = True
                elif self.xChange < 0:  # Moving left
                    self.rect.left = tile[1].right
                    self.x = self.rect.x
                self.xChange = 0
        
        self.rect.x = self.x
        self.rect.y = self.y

        return collided, ifDead, ifWin
    

    def move(self, tileList, freeze=False):
        collided, ifDead, ifWin = self.collision(tileList)
        if not collided:
            self.on_ground = False

        if freeze or self.freezeFrame > 0:
            self.xChange = 0
            self.yChange = 0
            if freeze:
                self.freezeFrame = 50
            else:
                self.freezeFrame -= 1

        if self.xChange != 0:
            self.x += self.xChange
            self.xChange = 0
        self.y += self.yChange

        
        self.check_walk()
        if not self.on_ground:
            self.yChange += self.gravity

        self.rect.x = self.x
        self.rect.y = self.y

        return ifDead, ifWin
        

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


    def check_collision(self, enemies):
        for enemy in enemies:
            enemy_rect = pg.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if self.rect.colliderect(enemy_rect):
                offsetX = int(enemy.x - self.x)
                offsetY = int(enemy.y - self.y)
                if self.mask.overlap(enemy.mask, (offsetX, offsetY)):
                    return True
        return False