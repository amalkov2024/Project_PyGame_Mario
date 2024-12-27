import pygame
import sys
import os

def terminate():  # завершение игры
    pygame.quit()
    sys.exit()

def load_image(name, color_key=None):
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print("Cannot load image:", name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Levelnum(pygame.sprite.Sprite):
    def __init__(self, level_type, pos_x, pos_y):
        super().__init__(levels_group, all_sprites)
        self.image = level_images[level_type]
        self.rect = self.image.get_rect().move(pos_x, image_level_height * pos_y)



def image_gen_level(level):
    x, y =  10, 0
    for i in level:
        y+=1
        Levelnum(level[i],x,y)
    return
def chioce_level_screen():
    global list_file
    choice_level=list_file[0]

    fon = pygame.transform.scale(load_image("fon.png"), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  choice_level# начинаем игру
        levels_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)




pygame.init()
pygame.key.set_repeat(200, 70) # контроль повторения удерживаемых клавиш
FPS = 50
# Размер окна игры 1280*720 размер клетки 40*40
step = tile_width = tile_height = 40
width = 32*tile_width
height = 18*tile_height
image_level_height = 55


screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
# Группа спрайтов для отображения уровней
levels_group = pygame.sprite.Group()
# изображения для спрайтов уровней
list_file = [
        file for file in os.listdir("data") if file[-4:] == ".txt" and file[:5] == "level"
    ]
level_images = dict()
for i in list_file:
    level_images[i[:-4]] = i[:-4]+'.png'

# Запуск игры
tile_images = {"wall": load_image("box.png"), "empty": load_image("grass.png")}
player_image = load_image("mario.png", -1)

level = chioce_level_screen()  # Выбор уровня игры
