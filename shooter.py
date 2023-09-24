from pygame import*
from random import randint
import time as t
init()
mixer.music.load("t.ogg")
mixer.music.play(-1)
mixer.music.set_volume(0.5)
fire_sound = mixer.Sound("fire3.ogg")
fire_sound.set_volume(0.5)

win_width = 700
win_height = 500

font.init()

score = 0
lost = 0

win = display.set_mode((win_width, win_height))
display.set_caption("Day in Kyiv")

background = transform.scale(image.load("kyiv3.jfif"), (win_width, win_height))
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, weight, height, speed):
        super().__init__()

        self.image = transform.scale(image.load(img), (weight, height))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__(img, x, y, w, h, speed)
        self.reload = 0
        self.rate = 5


    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_SPACE] and self.reload >= self.rate:
            self.reload = 0
            fire_sound.play()
            self.fire()
        elif self.reload < self.rate:
            self.reload += 1

    def fire(self):
        bul = Bullet("bullet2.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bul)



class Enemy(GameSprite):
    #рух ворога
    def update(self):
        self.rect.y += self.speed 
        global lost
        if self.rect.y > win_height:
            lost += 1
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
        #зникає, якщо дійдедо краю екрана
        if self.rect.y > win_height:


            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()



ship = Player("rocketplayer1.png", 5, win_height - 100, 80, 100, 6)



finish = False
run = True
FPS = 60

bullets = sprite.Group()



monsters = sprite.Group()
for i in range(5):
    x = randint(80, win_width - 80)
    speed = randint(1,3)
    monster = Enemy("shahed.png", x, -40, 80, 50, speed)
    monsters.add(monster)

f = font.Font(None, 36)
start_time = t.time()



while run:

    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        curret_time = t.time()
        win.blit(background, (0,0))
        text_score = f.render(f"Рахунок: {score}", True, (255, 255, 255))
        win.blit(text_score, (10,20))

        text_lost = f.render(f"Пропущено: {lost}", True, (255, 255, 255))
        win.blit(text_lost, (10, 60))

        text_time = f.render(f"Залишилося часу: {20 - (int(curret_time) - int(start_time))}", True, (255, 255, 255))
        win.blit(text_time, (10, 80))


        monsters.update()
        bullets.update()

        ship.update()
        ship.reset()
        monsters.draw(win)
        bullets.draw(win)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            x = randint(80, win_width - 80)
            speed = randint(1, 2)
            monster = Enemy("shahed.png", x, -40, 80, 50, speed)
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= 10 or int(curret_time) - int(start_time) >= 20:
            finish = True
            lose = f.render(f"You LOSE!!!", True, (255, 255 ,255))
            win.blit(lose, (200, 200))

        if score >= 30:
            finish = True
            won = f.render("WIN!!!!", True, (255, 150, 0))
            win.blit(won, (200, 200))



        display.update()


    

    clock.tick(FPS)
