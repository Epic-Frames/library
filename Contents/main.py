import pygame as pg
import sys
import json
import random
from enemy import Enemy
from text import Text
from player import Player
from world import World

pg.init()

TILE_SIZE = 32
SCREEN_X = 1280
SCREEN_Y = 720
SCREEN = pg.display.set_mode((SCREEN_X, SCREEN_Y))
world = World("Assets/dirt.jpeg", "Assets/lava.jpeg", "Assets/diamond.png", TILE_SIZE)
pg.display.set_caption("Cave of Malice v0.2.0 - alpha")
clock = pg.time.Clock()

# git test
player = Player(100, 574, 28.5, 48, 5, 2, "Assets/player.png", None, 0.5, -6, 10)

font = pg.font.Font(None, 36)
startupFont = pg.font.Font(None, 56)

background = pg.image.load("Assets/bg.png")
background = pg.transform.scale(background, (SCREEN_X, SCREEN_Y))

levelCount = 3

mode = ""

levels = [[] for _ in range(levelCount + 1)]

studioText = Text(None, None, "Epic Frame Studio", startupFont, (250, 250, 250), SCREEN_X, SCREEN_Y)
deathText = Text(None, None, "You died!", font, (0, 0, 0), SCREEN_X, SCREEN_Y)
winText = Text(None, None, "You Win", font, (0, 0, 0), SCREEN_X, SCREEN_Y)

for i in range(levelCount):
    levels[i + 1] = world.load_map("level" + str(i + 1) + ".txt")
    if levels[i + 1] == 0:
        pg.quit()
        sys.exit()

currentPage = "start_animation"
currentLevel = 3
level = levels[currentLevel]

FPS = 30

enemies = []

# Load json
try:
    with open("enemies.json", "r") as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print("JSON file not found. Quitting...")
    pg.quit()
    sys.exit()

def spawn_enemies(level):
    global enemies
    enemies = []
    eflevel = data["levels"][str(level)]
    for enemyd in eflevel:
        enemy = Enemy(enemyd["type"], enemyd["init_x"], enemyd["init_y"], enemyd["width"], enemyd["height"], enemyd["speed"], enemyd["health"], enemyd["src_img"], enemyd["dir"], enemyd["num1"], enemyd["num2"])
        enemies.append(enemy)
        enemy = None

def draw_button(x, y, width, height, color, text):
    pg.draw.rect(SCREEN, color, (x, y, width, height))
    text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
    SCREEN.blit(text, text_rect)


def width():
    print("2 point perspective")


def start_animation():
    startTime = pg.time.get_ticks()
    duration = 4000
    frame, halfFrames = None, None
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    return "game"

        SCREEN.fill((0, 0, 0))

        if frame or halfFrames != 0:
            frame, halfFrames = studioText.blink(SCREEN, duration / 1000 - 1.5, frame, halfFrames, 1500, pg.time.get_ticks())
        

        if pg.time.get_ticks() - startTime > duration:
            return "game"


        pg.display.update()
        clock.tick(FPS)

def game():
    global level, currentLevel
    world.load_tiles(level)
    # mode = "Jump"
    spawn_enemies(currentLevel)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    currentLevel += 1
                    return "game"
        SCREEN.blit(background, (0, 0))

        if mode == "Jump":
            if player.on_ground:
                player.jumping = True
                player.yChange = player.jumpPower
                player.on_ground = False

        # Move characters
        ifFreeze = False
        for enemy in enemies:
            if enemy.move():
                ifFreeze = True

        if ifFreeze:
            ifDead, ifWin = player.move(world.tileList, freeze=True)
        else:
            ifDead, ifWin = player.move(world.tileList, freeze=False)
        

        # Detect collision
        if player.check_collision(enemies):
            ifDead = True

        # Display character
        world.draw_map(SCREEN)
        player.draw(SCREEN)
        for enemy in enemies:
            enemy.draw(SCREEN)
        
        if ifWin | ifDead:
            if ifWin:
                if currentLevel < levelCount:
                    currentLevel += 1
                    level = levels[currentLevel]
                    player.x = 100
                    player.y = 574
                    return "game"
                currentLevel = 1
                level = levels[currentLevel]
                return "win_screen"
            else: 
                return "game_over"

        clock.tick(FPS)
        pg.display.update()


def game_over():
    while True:
        mouse_x, mouse_y = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if 590 <= mouse_x <= 690 and 500 <= mouse_y <= 550:
                    player.x = 100
                    player.y = 572
                    for enemy in enemies:
                        enemy.x = 200
                        enemy.y = 597
                        enemy.direction = 1
                    return "game"
        
        SCREEN.fill((255, 0, 0))

        deathText.show(SCREEN)

        button_text = pg.font.Font(None, 36).render(f"Restart", True, (0, 0, 0))
        draw_button(590, 500, 100, 50, (194, 194, 194), button_text)

        clock.tick(FPS)
        pg.display.update()


def win_screen():
    while True:
        mouse_x, mouse_y = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if 590 <= mouse_x <= 690 and 500 <= mouse_y <= 550:
                    player.x = 100
                    player.y = 572
                    for enemy in enemies:
                        enemy.x = 200
                        enemy.y = 597
                        enemy.direction = 1
                    return "game"
        
        SCREEN.fill((0, 255, 0))

        winText.show(SCREEN)

        button_text = pg.font.Font(None, 36).render(f"Restart", True, (0, 0, 0))
        draw_button(590, 500, 100, 50, (194, 194, 194), button_text)

        clock.tick(FPS)
        pg.display.update()


        
def main():
    global currentPage
    while True:
        if currentPage == "start_animation":
            currentPage = start_animation()
        elif currentPage == "game":
            currentPage = game()
        elif currentPage == "game_over":
            currentPage = game_over()
        elif currentPage == "win_screen":
            currentPage = win_screen()

if __name__ == "__main__":
    main()