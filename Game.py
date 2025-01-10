import os
import sys

import pygame


class Toorel(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, direct='right'):
        super().__init__(toorel_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.direction = direct

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction, 'black')
        all_sprites.add(bullet)
        toorel_bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direct, color='YELLOW'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        if direct == 'up':
            self.speedx = 0
            self.speedy = -10
        elif direct == 'down':
            self.speedx = 0
            self.speedy = 10
        elif direct == 'right':
            self.speedx = 10
            self.speedy = 0
        elif direct == 'left':
            self.speedx = -10
            self.speedy = 0

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0 or self.rect.top > 730 or self.rect.x < 0 or self.rect.x > 1280:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, name_img, pos_x, pos_y):
        super().__init__(coin_group, all_sprites)
        self.image = load_image(name_img)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 5, tile_height * pos_y + 5)
        self.image.set_colorkey((255, 255, 255))


class Strelka(pygame.sprite.Sprite):
    def __init__(self, name_img, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(name_img)
        self.rect = self.image.get_rect().move(
            pos_x, image_level_height * pos_y
        )
        # self.rect.x = pos_x
        # self.rect.y = pos_y
        self.image.set_colorkey((255, 255, 255))


class Levelnum(pygame.sprite.Sprite):  # класс спрайтов  для "выбор уровня"
    def __init__(self, level_type, pos_x, pos_y):
        super().__init__(levels_group, all_sprites)
        self.image = level_images[level_type]
        self.rect = self.image.get_rect().move(pos_x, image_level_height * pos_y)


def image_gen_level(level_img):  # генерируем спрайты "выбор уровня Level n"
    x, y = 20, 1
    for level_name in level_img:
        y += 1
        Levelnum(level_name, x, y)
    return


def chioce_level_screen():
    # группа спрайтов стрелки для выбора
    strelka_group = pygame.sprite.Group()
    coord_x = 255 + 20
    coord_y = 2
    dy = 1  # выбранный уровень
    strelka_level = Strelka('strelka.png', coord_x, coord_y)
    strelka_group.add(strelka_level)
    play_game = Strelka('play.png', width - 200, 11)
    strelka_group.add(play_game)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_DOWN and 0 < dy < 9:
                    strelka_level.rect.y += image_level_height
                    dy += 1
                elif event.key == pygame.K_UP and 1 < dy < 10:
                    strelka_level.rect.y -= image_level_height
                    dy -= 1
                elif event.key == pygame.K_SPACE:
                    return dy - 1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_game.rect.collidepoint(event.pos):
                    return dy - 1  # начинаем игру
        screen.fill(pygame.Color(0, 0, 0))
        # отрисовка фона старт
        fon = pygame.transform.scale(load_image("fon.png"), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 45)
        intro_text = "Выбери уровень"
        text_coord = 80
        string_rendered = font.render(intro_text, 1, pygame.Color("black"))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        # отрисовка фона финиш
        levels_group.draw(screen)
        strelka_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direct='left'):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 8, tile_height * pos_y + 0
        )
        self.direction = direct

    def shoot(self):
        pygame.mixer.music.load('data/music/bullet.mp3')  # подгружаем файл с музыкой
        pygame.mixer.music.play()  # включаем музыку
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
        all_sprites.add(bullet)
        bullets.add(bullet)


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
    pygame.mixer.music.load('data/music/Mario.mp3')  # подгружаем файл с музыкой
    pygame.mixer.music.play()  # включаем музыку
    intro_text = [
        "Super Mario 2D",
        "",
        "",
        "",
        "проект PyGame",
        "2025 year",
    ]

    fon = pygame.transform.scale(load_image("fon.png"), (width, height))
    screen.blit(fon, (0, 0))
    text_size = 220
    text_coord = 100
    for line in intro_text:
        font = pygame.font.Font(None, text_size)
        text_size = 100
        string_rendered = font.render(line, 1, pygame.Color("blue"))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 1280 // 2 - intro_rect.centerx
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.stop()  # остановка музыки
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def game_over(score_end, level_end, music_game_over='mario-smert.mp3', fon_game_over='game_over.png'):
    pygame.mixer.music.load('data/music/' + music_game_over)  # подгружаем файл с музыкой
    pygame.mixer.music.play()  # включаем музыку
    intro_text = [
        "SCORE: " + str(score_end),
        "LEVEL: " + str(level_end)
    ]
    fon = pygame.transform.scale(load_image(fon_game_over), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 80)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color("RED"))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # остановка музыки
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()  # остановка музыки
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    try:
        # читаем уровень, убирая символы перевода строки
        with open(filename, "r") as mapFile:
            level_map = [line.strip() for line in mapFile]
            # и подсчитываем максимальную длину
        # max_width = max(map(len, level_map))
        max_width = 32
        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, "."), level_map))
    except FileNotFoundError:
        print("Файл не найден:", filename)
        print("Программа завершена")
        terminate()


def generate_level(level):  # генерируем спрайты карты каждую клетку
    new_player, x, y, door = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ".":
                Tile("empty", x, y)
            elif level[y][x] == "#":
                Tile("wall", x, y)
            elif level[y][x] == '+':
                Tile("empty", x, y)
                Coin('coin.png', x, y)
            elif level[y][x] == 'c':
                Tile("doorclose", x, y)
                door = (x, y)
            elif level[y][x] == 'u':
                Tile("empty", x, y)
                Toorel("toorel_up", x, y, 'up')
            elif level[y][x] == 'd':
                Tile("empty", x, y)
                Toorel("toorel_down", x, y, 'down')
            elif level[y][x] == 'l':
                Tile("empty", x, y)
                Toorel("toorel_left", x, y, 'left')
            elif level[y][x] == 'r':
                Tile("empty", x, y)
                Toorel("toorel_right", x, y, 'right')
            elif level[y][x] == "@":
                Tile("empty", x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, door


# Код самой игры
try:
    # читаем из файла highscore
    with open('data/highscore.txt', 'r') as file:
        highscore = max(int(x) for x in file.readline())
except FileNotFoundError:
    highscore = 0

score = 0  # общий счёт игры
lives = 3  # количество жизней на старте
pygame.init()
pygame.key.set_repeat(200, 70)  # контроль повторения удерживаемых клавиш
FPS = 50
# Размер окна игры 1280*720 размер клетки 40*40
step = tile_width = tile_height = 40
width = 32 * tile_width  # 32 клетки в ширину
height = 18 * tile_height  # 18 клеток в высоту
image_level_height = 55  # высота для спрайтов "выбора уровня"
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
start_screen()  # Заставка перед началом игры
# основной персонаж
player = None
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
levels_group = pygame.sprite.Group()  # Группа спрайтов для отображения уровней
coin_group = pygame.sprite.Group()  # Группа спрайтов монет
bullets = pygame.sprite.Group()  # Группа для пуль
toorel_group = pygame.sprite.Group()  # группа для турелей
toorel_bullets = pygame.sprite.Group()  # группа пуль турелей
# Запуск игры

# список уровней
list_file = [
    file for file in os.listdir("data") if file[-4:] == ".txt" and file[:5] == "level"
]
# изображения для спрайтов уровней
level_images = dict()
for i in list_file:
    level_images[i[:-4]] = load_image(i[:-4] + '.png')
image_gen_level(level_images)  # добавляем спрайты уровней

tile_images = {"wall": load_image("box.png"), "empty": load_image("grass.png"),
               "doorclose": load_image("doorclose.png"), "dooropen": load_image("dooropen.png"),
               "toorel_up": load_image("toorel_up.png"), "toorel_down": load_image("toorel_down.png"),
               "toorel_left": load_image("toorel_left.png"), "toorel_right": load_image("toorel_right.png")}
player_image = load_image("mario.png", -1)
chioce_level_num = chioce_level_screen()  # номер стартового уровня
time_level_start = pygame.time.get_ticks() // 1000  # время начала игры
time_bullet = 0
while chioce_level_num <= 8 and lives > 0:  # цикл проигрывания уровня
    level_name = list_file[chioce_level_num]  # Выбор уровня игры level = filename 'level.txt'
    level_map = load_level(level_name)  # карта уровня список строк
    # положение игрока и размер карты
    player, level_x, level_y, door_level = generate_level(level_map)
    # подсчет количества монет в текущем уровне
    count_coin_cur_level = sum(s.count('+') for s in level_map)
    count_coin_level = 0
    level_end = False
    dx = player.rect.x
    dy = player.rect.y
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # running = False
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # running = False
                    terminate()
                if event.key == pygame.K_LEFT:
                    if (player.rect.x - step) < 0 or dx < 40 or \
                            level_map[(player.rect.y) // step] \
                                    [(player.rect.x - 8) // step - 1] == '#':
                        continue
                    player.image = load_image("mario_left.png", -1)
                    player.rect.x -= step
                    dx -= step
                    player.direction = 'left'
                if event.key == pygame.K_RIGHT:
                    if (player.rect.x + step) > 1280 or dx > 1240 or \
                            level_map[(player.rect.y) // step] \
                                    [(player.rect.x - 8) // step + 1] == '#':
                        continue
                    player.image = load_image("mario_right.png", -1)
                    player.rect.x += step
                    dx += step
                    player.direction = 'right'
                if event.key == pygame.K_UP:
                    if (player.rect.y - step) < 0 or dy < 40 or level_map[(player.rect.y) // step - 1] \
                            [(player.rect.x - 8) // step] == '#':
                        continue
                    player.image = load_image("mario_up.png", -1)
                    player.rect.y -= step
                    dy -= step
                    player.direction = 'up'
                if event.key == pygame.K_DOWN:
                    if (player.rect.y + step) > 720 or dy > 680 or \
                            level_map[(player.rect.y) // step + 1] \
                                    [(player.rect.x - 8) // step] == '#':
                        continue
                    player.image = load_image("mario_down.png", -1)
                    player.rect.y += step
                    dy += step
                    player.direction = 'down'
                if event.key == pygame.K_SPACE:
                    player.shoot()
        screen.fill(pygame.Color(0, 0, 0))
        tiles_group.draw(screen)
        coin_group.draw(screen)
        player_group.draw(screen)
        bullets.draw(screen)
        toorel_group.draw(screen)
        toorel_bullets.draw(screen)
        time_level = pygame.time.get_ticks() // 1000 - time_level_start
        # вывод общего счета в игре  и количества оставшихся жизней
        title_level = 'SCORE: ' + str(score) + ' ' * (20 - len(str(score))) + 'LIVES: ' + str(lives) + \
                      ' ' * (5 - len(str(lives))) + 'LEVEL: ' + str(chioce_level_num + 1) + \
                      ' ' * (5 - len(str(chioce_level_num + 1))) + 'TIME: ' + str(time_level) + \
                      ' ' * (20 - len(str(time_level))) + 'HIGHSCORE: ' + str(highscore)
        font = pygame.font.Font(None, 40)
        string_rendered = font.render(title_level, 1, pygame.Color("black"))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 10
        intro_rect.y = 10
        screen.blit(string_rendered, intro_rect)
        # вывод общего счета окончание  и количества оставшихся жизней
        pygame.display.flip()
        all_sprites.update()  # обновление
        clock.tick(FPS)  # обновление экрана
        coin_pickup = pygame.sprite.spritecollide(player, coin_group, True)  # проверяем столкновение с монетой
        if coin_pickup:
            count_coin_level += 1  # увеличиваем количество подобранных монет
            score += 1  # увеличиваем общий счет
            pygame.mixer.music.load('data/music/coin.mp3')  # подгружаем файл с музыкой
            pygame.mixer.music.play()  # включаем музыку
        if count_coin_cur_level * 0.6 < count_coin_level:  # уровень завершен
            level_end = True
            Tile("dooropen", *door_level)
        if level_end and ((player.rect.x - 8) // step, player.rect.y // step) == door_level:  # уровень пройден
            pygame.mixer.music.load('data/music/next_level.mp3')  # подгружаем файл с музыкой
            pygame.mixer.music.play()  # включаем музыку
            chioce_level_num += 1
            player.kill()  # удаляем игрока с поля
            toorel_group.empty()
            tiles_group.empty()
            coin_group.empty()
            player_group.empty()
            bullets.empty()
            running = False

        player_kill_toorel = pygame.sprite.groupcollide(bullets, toorel_group, True,
                                                        True)  # удаление подстрелянных турелей

        bullet_kill_toorel = pygame.sprite.groupcollide(toorel_bullets, tiles_group, False,
                                                        False)  # проверка столкновения пуль турелей с ящиками
        for key_bul in bullet_kill_toorel:
            if bullet_kill_toorel[key_bul][0].image == tile_images['wall']:
                key_bul.kill()  # если пуля столкнулась с ящиком то удаляем ее (спрайт)

        bullet_kill_player = pygame.sprite.groupcollide(bullets, tiles_group, False,
                                                        False)  # проверка столкновения пуль игрока с ящиками
        for key_bul in bullet_kill_player:
            if bullet_kill_player[key_bul][0].image == tile_images['wall']:
                key_bul.kill()  # если пуля столкнулась с ящиком то удаляем ее (спрайт)

        toorel_pickup = pygame.sprite.spritecollide(player, toorel_group,
                                                    True)  # проверяем столкновение игрока с турелью
        bullets_pickup = pygame.sprite.spritecollide(player, toorel_bullets,
                                                     True)  # проверяем столкновение игрока с пулей от турели
        if toorel_pickup or bullets_pickup:
            if lives == 1:
                game_over(score, chioce_level_num + 1)
            else:
                pygame.mixer.music.load('data/music/mario-smert.mp3')  # подгружаем файл с музыкой
                pygame.mixer.music.play()  # включаем музыку
                lives -= 1
                score -= count_coin_level  # вычитаем монеты собранные не текущем уровне
                player.kill()
                toorel_group.empty()
                tiles_group.empty()
                coin_group.empty()
                player_group.empty()
                bullets.empty()
                toorel_bullets.empty()
                running = False
        # стрельба турелями start
        if time_level % 3 == 0 and time_bullet != time_level:
            for tur in toorel_group.sprites():
                tur.shoot()
            time_bullet = time_level
        # стрельба турелями end

# записываем в файл highscore
if score > highscore:
    with open('data/highscore.txt', 'w+') as file:
        file.write(str(score))
game_over(score, chioce_level_num + 1, 'world_clear_fanfare.mp3', 'you_win.png')
terminate()
