#Создай собственный Шутер!

from pygame import *
from random import randint


class GameSprite(sprite.Sprite):
    def __init__(self,img, x,y, w,h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y 
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def collidepoint(self, x,y):
        return self.rect.collidepoint(x,y)
class Player(GameSprite):
    def update(self):
        keypressed = key.get_pressed()
        if keypressed[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed
        if keypressed[K_RIGHT] and self.rect.x < 700-10-65:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.y,15, 30, 5)
        bullets.add(bullet)
    


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 700 -self.rect.height:
            self.rect.x = randint(10, 700-10-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(1,4)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()
       


window = display.set_mode((700, 500))
display.set_caption('Шутер')



game = True
finish = True
menu = True
lost = 0
score = 0
background = transform.scale(image.load('doroga.jpg'), (700,500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
clock = time.Clock()
fps = 70

    

font.init()
#font1 = font.Font(None, 36)
font1 = font.SysFont('Arial', 36)

player = Player('sold.png', 300, 400, 65, 100, 5)
bullets = sprite.Group()
enemy_count = 5
enemyes = sprite.Group()
for i in range(enemy_count):
    enemy = Enemy('zombi.png', randint(10, 700-10-70), -40, 60, 100, randint(1,2))
    enemyes.add(enemy)

button = GameSprite('g11938.png', 300, 200, 100, 50, 0)


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    if menu:
        window.blit(background, (0,0))
        button.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if button.collidepoint(pos[0], pos[1]):
                menu = False
                finish = False
    
    if not finish:
        window.blit(background, (0, 0))

        player.update()
        player.reset()

        enemyes.update()
        enemyes.draw(window)

        bullets.update()
        bullets.draw(window)

        lost_enemy = font1.render('Пропущено: '+str(lost), 1, (255,255,255))
        window.blit(lost_enemy, (10,10))
        score_enemy = font1.render('Убито: '+str(score), 1, (255,255,255))
        window.blit(score_enemy, (10,50))
        
        #проверка усл
        sprite_list = sprite.groupcollide(enemyes, bullets, True, True)
        for i in range(len(sprite_list)):
            score += 1
            enemy = Enemy('zombi.png', randint(10, 700-10-70), -40, 60, 100, randint(1,2))
            enemyes.add(enemy)
        if score >=50:
            finish = True
            text_win = font1.render('XD', 1, (255,255,255))
            window.blit(text_win, (350,250))

        sprite_list = sprite.spritecollide(player, enemyes, True)
        if lost>=5 or len(sprite_list)>0:
            finish = True
            text_lose = font1.render(':(', 1, (255,255,255))
            window.blit(text_lose, (350,250))


    clock.tick(fps) 
    display.update()

    
    