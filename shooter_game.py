#Создай собственный Шутер!

from pygame import *
from random import *

mixer.init()
font.init()
font1  = font.Font(None,70)
font2  = font.Font(None,25)

window_w = 350
window_h = 600
window = display.set_mode((window_w,window_h))
display.set_caption("Шутер")
background = transform.scale(image.load('pitch.png'), (window_w,window_h))
mixer.music.load('space.ogg')
mixer.music.play()
shoot = mixer.Sound('fire.ogg')
clock = time.Clock()
FPS = 120
game = True
class GameSprite(sprite.Sprite):
    def __init__(self,image2,speed,x,y,w,h):
        super().__init__()
        self.image = transform.scale(image.load(image2),(w,h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
    def reset(self):
        window.blit(self.image,(self.rect.x , self.rect.y))


    
class Player(GameSprite):
    ready_shoot = True
    shoot_timer = 0
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < window_w - self.w - 5:
            self.rect.x += self.speed
        if keys[K_SPACE] and self.ready_shoot:
            self.ready_shoot = False
            self.shoot_timer = 40
            bullets.add(Bullet('football.png',2,self.rect.centerx,self.rect.top,20,20))
        if self.shoot_timer > 0:
            self.shoot_timer -= 1 
        else:
            self.ready_shoot = True



player = Player("leo.png", 5, window_w/2, 499, 50,50)
loss = 0
class Enemy(GameSprite):
    def update(self):
        global loss
        self.rect.y += self.speed
        if self.rect.y >= window_h:
            self.rect.x = randint(1,window_w-self.w)
            self.rect.y = 0 - self.h
            loss += 1
    
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed 
        if  self.rect.y <0:
            self.kill()

enemies = sprite.Group()
bullets = sprite.Group()
for i in range (5):
    enemies.add(Enemy('ron.png',randint(1,2),randint(1,window_w-50),-50,50,50))

finish = False
points = 0
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
    window.blit(background,(0,0))
    if finish == False:
        player.update()
        player.reset()
        enemies.draw(window)
        enemies.update()
        bullets.draw(window)
        bullets.update()
        kill_list = sprite.groupcollide(bullets,enemies, True, True)
        for i in kill_list:
            points += 1
            enemies.add(Enemy('ron.png',randint(1,2),randint(1,window_w-50),-50,50,50))
        if points >= 15:
            finish = True 
            win = font1.render('YOU WON!', True,(0,0,0))
        if loss >= 10:
            finish = True
            win = font1.render('YOU LOSE!', True,(0,0,0))
        score = font2.render('score - '+str(points), True,(0,0,0))
        miss = font2.render('missed - '+str(loss), True,(0,0,0))
        window.blit(score,(5,0))
        window.blit(miss,(5,40))
        
    else:
        window.blit(win,(window_w/2 - 130,window_h/2+50))

    display.update()
    clock.tick(FPS)

