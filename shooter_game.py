#Создай собственный Шутер!

from pygame import *
from random import randint
import time as timer

lost_ememies = 0
win_enemies = 0 
bullet_draw = 0
sprites_list = []
cooldown = 0.4
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 75))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
        


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        maslina = Bullet("bullet.png", 300, 300, 15)
        bullets.add(maslina)
        sound1.play
            
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (65, 45))
        self.rect.x = randint(20, 640)
    def update(self):
        self.rect.y += self.speed      
        if self.rect.y > 500:
            self.rect.y = -40
            self.rect.x = randint(0, 700)
            global lost_ememies
            lost_ememies+=1
        window.blit(self.image,(self.rect.x, self.rect.y))
        

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (20, 30))
        self.rect.y = player.rect.y
        self.rect.x = player.rect.x+5
    def update(self):
        window.blit(self.image,(self.rect.x+17, self.rect.y))
        self.rect.y -= self.speed
        if self.rect.y > 500:
            self.kill()


class Laser(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (80, 1050))
    def update(self):
        self.rect.y = player.rect.y-1040
        self.rect.x = player.rect.x-4

class Buffs(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (60, 60))
    def update(self):
        self.rect.x = randint(30, 630)
        window.blit(self.image,(self.rect.x, self.rect.y))



run = True 

R = 500
W = 700

window = display.set_mode((W, R))
background = transform.scale(image.load('galaxy.jpg'),(700,500))
font.init()

font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 36)


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
sound1 = mixer.Sound('fire.ogg')

clock = time.Clock()

FPS = 60

clock.tick(FPS)


display.update()


player = Player('rocket.png' ,335 , 400, 8)

zloy_4el_1 = Enemy("ufo.png", 0, -40, 2)
zloy_4el_2 = Enemy("ufo.png", 0, -40, 2)
zloy_4el_3 = Enemy("ufo.png", 0, -40, 2)
zloy_4el_4 = Enemy("ufo.png", 0, -40, 2)
zloy_4el_5 = Enemy("ufo.png", 0, -40, 2)


monsters = sprite.Group()

monsters.add(zloy_4el_1)
monsters.add(zloy_4el_2)
monsters.add(zloy_4el_3)
monsters.add(zloy_4el_4)
monsters.add(zloy_4el_5)

bullets = sprite.Group()
maslina = Bullet("bullet.png", 300, 300, 0)
laser = Laser("laser.png", 300, 300, 8)




bullet_cd_fast = Buffs("bullet_x2.png",-1000,400,2)

buff_accept= 0
time_2 = 0
while run:
    window.blit(background, (0,0))    

    text_win = font1.render("Побеждено амёб: " + str(win_enemies), 1, (255, 255,255))
    window.blit(text_win, (10,10))
    text_lose = font1.render("Не побеждено амёб: " + str(lost_ememies), 1, (255, 255,255))
    window.blit(text_lose, (10, 41))

    player.reset()
    player.update()

    sprites_list = sprite.groupcollide(monsters, bullets, False, True)

        
    

        
    laser.update()
    laser.reset()


    keys = key.get_pressed()
    if keys[K_SPACE]:
        time_1 = timer.time()
        if time_1-time_2 >= cooldown:
            
            player.fire()
            
            time_2 = timer.time()
    if sprites_list:
        for i in sprites_list:
            i.rect.y = -40
            i.rect.x = randint(0, 630)
            win_enemies+=1
    
    #x2 - collide
    if sprite.collide_rect(player, bullet_cd_fast):
        bullet_cd_fast.rect.x = 1000
        bullet_cd_fast.rect.y = 1000
        cooldown = 0.2
            
    bullets.update()
    monsters.update()

    #attachment_lose_win-start
    if win_enemies >= 100:
        zloy_4el_1.speed = 0
        zloy_4el_2.speed = 0
        zloy_4el_3.speed = 0
        zloy_4el_4.speed = 0
        zloy_4el_5.speed = 0
        maslina.speed = 0
    if lost_ememies == 1:
        zloy_4el_1.speed = 0
        zloy_4el_2.speed = 0
        zloy_4el_3.speed = 0
        zloy_4el_4.speed = 0
        zloy_4el_5.speed = 0
        maslina.speed = 0
    #attachment_lose_win-end




    #quit-start
    for e in event.get():
        if e.type == QUIT:
            run = False
    #quit-end


    #x2_buff-start
    if sprites_list:
        if buff_accept != 2:
            buff_random = randint(0, 25)
            print(buff_random)
            if buff_random == 1:
                buff_accept = 1
                bullet_cd_fast.update()

    if buff_accept == 1:
        bullet_cd_fast.reset()
        buff_accept = 2
    #x2_buff-end

    bullet_cd_fast.reset()
    display.update()
    clock.tick(FPS)