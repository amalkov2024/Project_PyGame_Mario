import pygame
import sys
import os



class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5
        )

class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


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


def terminate():  # завершение игры
    pygame.quit()
    sys.exit()


def start_screen():
    pygame.mixer.music.load('data/Mario.mp3')  # подгружаем файл с музыкой
    pygame.mixer.music.play()  # включаем музыку
    intro_text = [
        "ЗАСТАВКА",
        "",
        "Правила игры",
        "Если в правилах несколько строк,",
        "приходится выводить их построчно",
    ]

    fon = pygame.transform.scale(load_image("fon.png"), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color("black"))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.stop()  # остановка музыки
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    try:
        # читаем уровень, убирая символы перевода строки
        with open(filename, "r") as mapFile:
            level_map = [line.strip() for line in mapFile]
            # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))
        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, "."), level_map))
    except FileNotFoundError:
        print("Файл не найден:", filename)
        print("Программа завершена")
        terminate()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ".":
                Tile("empty", x, y)
            elif level[y][x] == "#":
                Tile("wall", x, y)
            elif level[y][x] == "@":
                Tile("empty", x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y

def chioce_level_screen():

    intro_text = ["ЗАСТАВКА"]

    fon = pygame.transform.scale(load_image("fon.png"), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)



# Код самой игры

# Отображение имен файлов с уровнями игры для предварительного просмотра и выбора нужного
list_file = [
    file for file in os.listdir("data") if file[-4:] == ".txt" and file[:5] == "level"
]
if list_file:
    print(
        "Имена файлов с доступными для загрузки уровнями:"
    )  # для отображения файлы с уровнями игры должны именоваться level*.txt
    for f in list_file:
        print(f)

#level = input("Введите название файла в котором расположена карта уровня: ")
level = 'level.txt'
pygame.init()
pygame.key.set_repeat(200, 70) # контроль повторения удерживаемых клавиш
FPS = 50
# Размер окна игры 1280*720 размер клетки 40*40
step = tile_width = tile_height = 40
width = 32*tile_width
height = 18*tile_height


screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# Запуск игры
tile_images = {"wall": load_image("box.png"), "empty": load_image("grass.png")}
player_image = load_image("mario.png", -1)

camera = Camera()

# положение игрока и размер карты
player, level_x, level_y = generate_level(load_level(level))
# Inna
dx = -(player.rect.x + player.rect.w // 2 - width // 2)
dy = -(player.rect.y + player.rect.h // 2 - height // 2)

start_screen()  # Заставка перед началом игры
# Реализовать выбор уровня

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if player.rect.x - dx < step or \
                        load_level(level)[(player.rect.y - dy) // step] \
                                [(player.rect.x - dx) // step - 1] == '#':
                    continue
                player.rect.x -= step
                dx += step
                # player.rect.x -= step
            if event.key == pygame.K_RIGHT:
                if (player.rect.x - dx) // step == level_x or \
                        load_level(level)[(player.rect.y - dy) // step] \
                                [(player.rect.x - dx) // step + 1] == '#':
                    continue
                player.rect.x += step
                dx -= step
                # player.rect.x += step
            if event.key == pygame.K_UP:
                if player.rect.y - dy < step or load_level(level)[(player.rect.y - dy) // step - 1] \
                        [(player.rect.x - dx) // step] == '#':
                    continue
                player.rect.y -= step
                dy += step
                # player.rect.y -= step
            if event.key == pygame.K_DOWN:
                if (player.rect.y - dy) // step == level_y or \
                        load_level(level)[(player.rect.y - dy) // step + 1] \
                                [(player.rect.x - dx) // step] == '#':
                    continue
                player.rect.y += step
                dy -= step
                # player.rect.y += step

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS) # обновление экрана

terminate()
