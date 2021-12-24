import pygame
import os
import random
FPS = 60
WIDTH = 600
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("洪承棋不要亂吠拉幹")
clock = pygame.time.Clock()

eat_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
upgrade_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()
font_name = os.path.join("font.ttf")

player_img = pygame.image.load(os.path.join("img", "images.jfif")).convert()
poops_img = []
for i in range(1, 4):
    poop_img = pygame.image.load(os.path.join("img", f"poop{i}.jpeg")).convert()
    poops_img.append(pygame.transform.scale(poop_img, (30, 30)))
icon = pygame.image.load(os.path.join("img", "icon.png")).convert()
icon = pygame.transform.scale(icon, (25, 19))
pygame.display.set_icon(icon)

def draw_full(surf, hp, x, y):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp / 50) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_init():
    screen.fill(BLACK)
    draw_text(screen, "洪承棋不要亂吠拉幹", 64,  WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "請用方向件讓他吃飽 他就會停止吠叫", 22,  WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "按任意鍵開始遊戲", 18,  WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:
                waiting = False
                return False
                
def draw_end():
    screen.fill(BLACK)
    draw_text(screen, "恭喜你，洪承棋已經停止吠叫了 !", 40,  WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "若再按任意鍵，洪承棋會再次開始吠叫！", 26,  WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
                return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (120, 100))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed [pygame.K_RIGHT]:
            self.rect.x += 15
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH
        elif key_pressed [pygame.K_LEFT]:
            self.rect.x -= 15
            if self.rect.left <= 0:
                self.rect.left = 0
        elif key_pressed [pygame.K_UP]:
            self.rect.y -= 15
            if self.rect.top <= 0:
                self.rect.top = 0
        elif key_pressed [pygame.K_DOWN]:
            self.rect.y += 15
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT

class Poop(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(poops_img)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(30, 570)
        self.rect.y = random.randrange(30, 570)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)
    
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree %= 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()


running = True
show_init = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        score = 0
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        poops = pygame.sprite.Group()
        p1 = Poop()
        p2 = Poop()
        all_sprites.add(p1)
        poops.add(p1)
        all_sprites.add(p2)
        poops.add(p2)
    clock.tick(FPS)
    #輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #更新
    all_sprites.update()
    hits = pygame.sprite.spritecollide(player, poops, True, pygame.sprite.collide_circle)
    for hit in hits:
        eat_sound.play()
        p = Poop()
        all_sprites.add(p)
        poops.add(p)
        score += 1
    if score == 25:
        upgrade_sound.play()
    if score > 25:
        player_img = pygame.image.load(os.path.join("img", "300.jfif")).convert()
        player.image = pygame.transform.scale(player_img, (90, 60))
    if score >= 50:
        if draw_end():
            break
        else:    
            show_init = True

    #顯示
    screen.fill(BLACK)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_full(screen, score, 5, 15)
    all_sprites.draw(screen)
    pygame.display.update()
pygame.quit()
