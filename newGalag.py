import pygame, threading
from time import sleep

# 클래스 멤버변수에 접근할 때 = 내부: cls 외부: GM 접근
# GameManager-------------------------------------------------------------------------#
class GM: 
    @classmethod
    def init(cls):
        cls.instances = []
        cls.score = 0 
        cls.display = pygame.display.set_mode((800,600))
        cls.font = pygame.font.SysFont('Comic Sans MS', 30)
        cls.keystates = {pygame.K_LEFT: False, pygame.K_RIGHT: False}
        cls.running = True
        cls.player = Player()
        cls.clock = pygame.time.Clock()
        cls.timer = pygame.time.get_ticks()
        cls.isgaov = False
        
    @classmethod
    def ioupdate(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GM.running = False
            if event.type == pygame.KEYDOWN: # 동시 입력에도 이동이 매끄럽게 되기 위해 수정
                if event.key in cls.keystates:
                    cls.keystates[event.key] = True
                    cls.player.move()
                if event.key == pygame.K_SPACE:
                    cls.player.fire()
                    
            if event.type == pygame.KEYUP:
                if event.key in GM.keystates:
                    cls.keystates[event.key] = False
                    cls.player.move()
        
        cls.display.fill((0,0,0))        
        cls.scoretext = cls.font.render(f"score: {cls.score}",False, (255,255,255))
        cls.hptext = cls.font.render(f"HP: {cls.player.hp}",False,(255,255,255))
        cls.display.blit(cls.hptext, (10,520))
        cls.display.blit(cls.scoretext,(10,550))        
        
    @classmethod
    def genenemy(cls):
        cls.now = pygame.time.get_ticks()
        if cls.now - cls.timer >= 5000:
            cls.timer = cls.now
            enemy = Enemy()
            
    @classmethod
    def callupdates(cls, *instances):
        cls.threads = []
        for instance in instances:
            thread = threading.Thread(target=instance.update)
            cls.threads.append(thread)
            thread.start()

        for thread in cls.threads:
            thread.join()
            
    @classmethod
    def gameover(cls):
        cls.isgaov = True
        print("GameOver")
        cls.instances.clear()
        cls.gaovtext = cls.font.render("Game Over",False, (255,255,255)) # 종료 구현
        cls.display.fill((0,0,0))
        cls.display.blit(cls.gaovtext,(320,270))
        cls.display.blit(cls.scoretext, (330,300))
        pygame.display.update()
        
    @classmethod
    def diffup(cls):
        if cls.score >= 150:
            for instance in cls.instances:
                if instance.tag == "enemy":
                    instance.Dx += 1
        
# Player---------------------------------------------------------------------------------#
class Player(GM): # 벽에 닿으면 이동 안되게 설정
    allie = "player"
    tag = "player"
    hp = 100
    def __init__(self):
        GM.instances.append(self)
        self.col = pygame.image.load("plane.gif")
        self.X, self.Y, self.Dx, self.Dy = 400, 550, 0, 0
        self.rect = pygame.Rect(self.X, self.Y, self.col.get_width(), self.col.get_height())
        
    def fire(self):
        missile = Missile(self.X, self.Y, -1)
        missile.allie = "player"

    def move(self):            
        if GM.keystates[pygame.K_LEFT]:
            self.Dx = -4*self.lWall
        elif GM.keystates[pygame.K_RIGHT]:
            self.Dx = 4*self.rWall
        else:
            self.Dx = 0

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.death()

    def death(self):
        GM.isgaov = True
        del self

    def update(self):
        self.rect = pygame.Rect(self.X, self.Y, self.col.get_width(), self.col.get_height())
        self.X += self.Dx
        if self.X <= 0: # 멈출 때만 적용됨 
            self.lWall = 0
        elif self.X > 750:
            self.rWall = 0
        else:
            self.lWall, self.rWall = 1, 1
        GM.display.blit(self.col, (self.X, self.Y))

# Enemy----------------------------------------------------------------------------------#
class Enemy(GM):
    allie = "enemy"
    tag = "enemy"
    def __init__(self):
        GM.instances.append(self)
        self.timer = pygame.time.get_ticks()
        self.col = pygame.image.load("plane.gif")
        self.X, self.Y, self.Dx, self.Dy = 0, 10, 2, 2
        self.rect = pygame.Rect(self.X, self.Y, self.col.get_width(), self.col.get_height())
        
    def fire(self):
        if self.now - self.timer >= 1000: # 0으로 하면 정확도 떨어져 수정 
            self.timer = self.now
            missile = Missile(self.X, self.Y, 1)
            missile.allie = "enemy"
    
    def death(self):
        GM.score += 15
        GM.instances.remove(self)
        del self

    def update(self):
        if self.Y > 600:
            GM.instances.remove(self)
            return
        
        self.rect = pygame.Rect(self.X, self.Y, self.col.get_width(), self.col.get_height())
        self.X += self.Dx
        self.now = pygame.time.get_ticks()
        
        if self.X <= 0 or self.X > 750: # 방향 전환 
            self.Dx *= -1
            self.Y += 30
            
        self.fire()

        GM.display.blit(self.col, (self.X, self.Y))
        
# Missile--------------------------------------------------------------------------------#            
class Missile(GM):
    allie = ""
    tag = "missile"
    def __init__(self, pX, pY, pDir):
        GM.instances.append(self)
        self.timer = pygame.time.get_ticks()
        self.col = pygame.image.load("plane.gif")
        self.X, self.Y, self.Dx, self.Dy = pX, pY, 0, 8*pDir
        self.rect = pygame.Rect(self.X, self.Y, self.col.get_width(), self.col.get_height())
        
    def update(self):
        self.now = pygame.time.get_ticks()
        self.rect = pygame.Rect(self.X, self.Y, self.col.get_width(), self.col.get_height())
        for target in GM.instances:
            if self.rect.colliderect(target.rect):
                if target.tag == "player" and self.allie == "enemy":
                    self.death()
                    target.hit()
                elif target.tag == "enemy" and self.allie == "player":
                    self.death()
                    target.death()
                
        self.Y += self.Dy
            
        if self.now - self.timer >= 2000: # 0으로 하면 정확도 떨어져 수정 
            self.timer = self.now
            self.death()
            
        GM.display.blit(self.col, (self.X, self.Y))
        
    def death(self):
        GM.instances.remove(self) #

# main---------------------------------------------#
pygame.init()
GM.init()
enemy = Enemy()
while GM.running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            GM.running = False
    while GM.running and not GM.isgaov:
        GM.ioupdate()
        GM.genenemy()
        GM.callupdates(*GM.instances)
        GM.diffup()
        pygame.display.update()
        GM.clock.tick(60) # 1초 당 60 프레임
        if GM.isgaov:
            GM.gameover()
            break
pygame.quit()
