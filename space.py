from pygame import *
from random import *
from time import sleep
'''Required classes'''



#directory
image_background = "background.jpg"
image_player = "spaceship.png"
image_enemy = "meteorit.png"
image_bullet = "rocket.png"
music1 = "music.mp3"


#parent class for sprites
class GameSprite(sprite.Sprite):
   #class constructor
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        # each sprite must store an image property
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed
        # each sprite must store the rect property it is inscribed in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#child class for the player sprite (controlled by arrows)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    
    def fire(self):
        bullet = Bullet(image_bullet,self.rect.centerx,self.rect.top,-15)
        bullet.rect.centerx = self.rect.centerx
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            missed += 1
            self.speed = randint(1,5)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


#Game scene:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("SpaceWar")
background = transform.scale(image.load(image_background), (win_width, win_height))


#Game characters:
player = Player(image_player, 5, win_height - 80, 10)

#enemy
enemies = sprite.Group()
for i in range(1,6):
    enemy  = Enemy(image_enemy,randint(80,win_width-80),-40,randint(1,5))
    enemies.add(enemy)

#bullet
bullets = sprite.Group()


game = True
finish = False
clock = time.Clock()
FPS = 60


#music
mixer.init()
mixer.music.load(music1)
mixer.music.play()
mixer.music.set_volume(0.05)

#text
font.init()
font1 = font.Font(None,80)
font2 = font.Font(None,30)
win = font1.render('YOU WIN!',True,(0,255,0))
lose = font1.render('YOU LOSE!',True,(255,0,0))

#scoring
score = 0
missed = 0
win = 50
lost = 10
life = 3


while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    
    if not finish:
        window.blit(background,(0,0))
        player.update()
        enemies.update()
        player.reset()
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)
        
        #bullet collide with enemy
        collides = sprite.groupcollide(enemies, bullets,True,True)
        for c in collides:
            score += 1
            enemy  = Enemy(image_enemy,randint(80,win_width-80),-40,randint(1,5))
            enemies.add(enemy)
            
        #player collide with enemy
        if sprite.spritecollide(player,enemies, False):
            sprite.spritecollide(player,enemies, True)
            life -= 1
            
        
        #add score
        text = font2.render('Score: '+ str(score),1,(255,255,255))
        window.blit(text,(10,20))
        
        #enemy missed
        text_missed = font2.render('Missed: '+ str(missed),1,(255,255,255))
        window.blit(text_missed,(10,50))
        
        #total lifea
        if life == 3:
            life_color = (0,150,0)
        elif life == 2:
            life_color = (150,150,0)
        elif life == 1:
            life_color = (150,0,0)
        
        text_life= font2.render('Life: '+ str(life),1,(life_color))
        window.blit(text_life,(630,10))
        
        #win
        if score >= win:
            finish = True
            text_win= font1.render('YOU WIN!!!',True,(0,255,0))
            window.blit(text_win,(200,200))
        #lose
        if life == 0 or missed >= lost:
            finish = True
            text_lose= font1.render('YOU LOSE!!!',True,(255,0,0))
            window.blit(text_lose,(200,200))
        
   
    display.update()
    clock.tick(FPS)





