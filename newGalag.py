import pygame, threading, pdb, csv

# GameManager-------------------------------------------------------------------------#
class GM: 
    @classmethod
    def init(cls):
        cls.instances = []
        cls.score = 0 
        cls.display = pygame.display.set_mode((800,600))
        cls.font = pygame.font.SysFont('Comic Sans MS', 30)
        cls.keystates = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}
        cls.running = True
        cls.player = Player()
        cls.clock = pygame.time.Clock()
        cls.timer = pygame.time.get_ticks()
        cls.isgaov = False
        cls.cooltime = 2000
        cls.name = cls.getname()
        
    @classmethod
    def update(cls):
        cls.setdiff()
        cls.genenemy()
        cls.getinput()
        cls.display.fill((0,0,0))        
        cls.scoretext = cls.font.render(f"score: {cls.score}",False, (255,255,255))
        cls.hptext = cls.font.render(f"HP: {cls.player.hp}",False,(255,255,255))
        cls.display.blit(cls.hptext, (10,520))
        cls.display.blit(cls.scoretext,(10,550))
        
    @classmethod
    def getinput(cls):
        for event in pygame.event.get():
            try:
                if event.type == pygame.QUIT:
                    GM.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key in cls.keystates:
                        cls.keystates[event.key] = True
                        cls.player.move()
                    if event.key == pygame.K_SPACE:
                        cls.player.fire()
                        
                if event.type == pygame.KEYUP:
                    if event.key in GM.keystates:
                        cls.keystates[event.key] = False
                        cls.player.move()
            except:
                print("catch exception::GM::getinput()")
            
    @classmethod
    def genenemy(cls):
        cls.now = pygame.time.get_ticks()
        if cls.now - cls.timer >= cls.cooltime:
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
        print(f"GameOver score: {cls.score}")
        cls.instances.clear()
        cls.gaovtext = cls.font.render("Game Over",False, (255,255,255))
        cls.restartbtn = Button(350, 470, 100, 30, "Restart")
        cls.rankbtn = Button(350, 530, 100, 30, "Ranking")
        cls.ranking = Ranking(250,10,300,500) 
        cls.isrankopen = False
        cls.updatecsv()
        
        while cls.isgaov:
            for event in pygame.event.get():
                try:
                    if event.type == pygame.QUIT:
                        GM.running = False
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if cls.restartbtn.rect.collidepoint(event.pos):
                            print("Restart")
                            cls.isgaov = False
                            cls.init()
                        elif cls.rankbtn.rect.collidepoint(event.pos):
                            if cls.isrankopen:
                                print("closed")
                                cls.isrankopen = False
                            else:
                                print("Ranking")
                                cls.isrankopen = True
                                
                except:
                    print("catch exception::GM::gameover")
            cls.display.fill((0,0,0))
            cls.display.blit(cls.gaovtext,(320,270))
            cls.display.blit(cls.scoretext, (330,300))
            cls.restartbtn.draw()
            cls.rankbtn.draw()
            cls.ranking.draw()
            pygame.display.update()
        
    @classmethod
    def setdiff(cls):
        cls.rank = cls.score//100
        if cls.rank > 15:
            cls.rank = 15      
        cls.cooltime = 2000 - (cls.rank * 100)

    @classmethod
    def getname(cls):
        rect = pygame.Rect(330,500,100,20)
        guidefont = pygame.font.SysFont('Comic Sans MS',18)
        inputfont = pygame.font.SysFont('Comic Sans MS',14)
        guidetext = guidefont.render("Input name", False, (255,255,255))
        inputext = ""
        while True:
            pygame.draw.rect(cls.display, (0,0,0), rect)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        enterkey = True
                        return inputext
                    elif event.key == pygame.K_BACKSPACE:
                        inputext = inputext[:-1]
                    else:
                        if len(inputext) <= 10:
                            inputext += event.unicode
                        
            
            cls.display.blit(guidetext, (330,470))
            pygame.draw.rect(GM.display, (255,255,255),rect)
            tsurface = inputfont.render(inputext, True, (0,0,0))
            trect = tsurface.get_rect(center=rect.center) 
            GM.display.blit(tsurface, trect)
            pygame.display.update()

    @classmethod
    def readcsv(cls):
        csvpath = "rankdata.csv"
        with open(csvpath, 'r', newline='', encoding='utf-8') as csvfile:
            rankdata = csv.reader(csvfile)
            data = list(rankdata)
        return data
            
    @classmethod
    def updatecsv(cls):
        csvpath = "rankdata.csv"
        data = cls.readcsv()
        new_row = [cls.name, str(cls.score)]
        data.append(new_row)
        data.sort(key=lambda x: int(x[1]) if x[1].isdigit() else 0, reverse=True)
        with open(csvpath, 'w', newline='', encoding='utf-8') as csvfile:
            csv.writer(csvfile).writerows(data)
        
# Ranking--------------------------------------------------------------------------------#
class Ranking: 
    def __init__(self,x,y,width,height):
        self.rect = pygame.Rect(x,y,width,height)
        self.font = pygame.font.SysFont('Comic Sans MS',20)
        
    def draw(self):
        if GM.isrankopen:
            pygame.draw.rect(GM.display, (0,0,0), self.rect)
            pygame.draw.rect(GM.display, (255,255,255), self.rect, 2)
            lineheight = 25
            csvtext = "\n".join([f"{row[0]:<10} {row[1]}" for row in GM.readcsv()[:20]])
            lines = csvtext.split("\n")
            for index, line in enumerate(lines):
                tsurface = self.font.render(line, True, (255,255,255))
                trect = tsurface.get_rect(center=(self.rect.centerx, self.rect.top + index * lineheight + 20))
                GM.display.blit(tsurface, trect)

# Button---------------------------------------------------------------------------------#
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont('Comic Sans MS', 25)
        
    def draw(self): 
        if self.text == "Ranking" or self.text == "Close":
            if GM.isrankopen:
                self.text = "Close"
            else:
                self.text = "Ranking"
        pygame.draw.rect(GM.display, (255,255,255),self.rect)
        tsurface = self.font.render(self.text, True, (0,0,0))
        trect = tsurface.get_rect(center=self.rect.center)
        GM.display.blit(tsurface, trect)
        
# Player---------------------------------------------------------------------------------#
class Player(GM): 
    allie = "player"
    tag = "player"
    hp = 1
    def __init__(self):
        GM.instances.append(self)
        self.col = pygame.image.load("player.png")
        self.X, self.Y, self.Dx, self.Dy = 400, 550, 0, 0
        self.rect = pygame.Rect(self.X, self.Y, self.col.get_width(), self.col.get_height())
        
    def fire(self):
        missile = Missile(self.X+12, self.Y-22, -1)
        missile.allie = "player"

    def move(self):
        if GM.keystates[pygame.K_LEFT]:
            self.Dx = -4
        elif GM.keystates[pygame.K_RIGHT]:
            self.Dx = 4
        else:
            self.Dx = 0
        if GM.keystates[pygame.K_UP]:
            self.Dy = -4
        elif GM.keystates[pygame.K_DOWN]:
            self.Dy = 4
        else :
            self.Dy = 0

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.death()

    def death(self):
        GM.isgaov = True
        del self

    def update(self):
        self.X += self.Dx 
        self.Y += self.Dy
        self.rect = pygame.Rect(self.X, self.Y, self.col.get_width(), self.col.get_height())
        
        if self.X < 0: 
            self.X = 0
        elif self.X > 750:
            self.X = 750
        if self.Y < 50: 
            self.Y = 50
        elif self.Y > 550:
            self.Y = 550
        
        GM.display.blit(self.col, (self.X, self.Y))

# Enemy----------------------------------------------------------------------------------#
class Enemy(GM):
    allie = "enemy"
    tag = "enemy"
    def __init__(self):
        GM.instances.append(self)
        self.timer = pygame.time.get_ticks()
        self.col = pygame.image.load("enemy.png")
        self.X, self.Y, self.Dx, self.Dy = 0, 10, 2, 2
        self.rect = pygame.Rect(self.X, self.Y, self.col.get_width(), self.col.get_height())
        self.cooltime = 1000
        
    def fire(self):
        if self.now - self.timer >= self.cooltime: 
            self.timer = self.now
            missile = Missile(self.X+16, self.Y+30, 1)
            missile.allie = "enemy"
            
    
    def death(self):
        GM.score += 15
        GM.instances.remove(self)
        del self

    def update(self):
        self.setdiff()
        self.fire()
        self.X += self.Dx
        self.rect = pygame.Rect(self.X, self.Y, self.col.get_width(), self.col.get_height())
        self.now = pygame.time.get_ticks()
        
        if self.X <= 0 or self.X > 750: 
            self.Dx *= -1
            self.Y += 30
            
        if self.Y > 600:
            GM.instances.remove(self)
            return
            
        
        GM.display.blit(self.col, (self.X, self.Y))
        
    def setdiff(self):
        self.rank = GM.score//100
        if self.rank > 15:
            self.rank = 15
        self.cooltime = 1000 - (self.rank * 50)
        
# Missile--------------------------------------------------------------------------------#            
class Missile(GM):
    allie = ""
    tag = "missile"
    def __init__(self, pX, pY, pDir):
        GM.instances.append(self)
        self.timer = pygame.time.get_ticks()
        if pDir == 1:
            self.col = pygame.image.load("emissile.png")
        else:
            self.col = pygame.image.load("pmissile.png")            
        self.X, self.Y, self.Dx, self.Dy = pX, pY, 0, 8*pDir
        self.rect = pygame.Rect(self.X, self.Y, self.col.get_width(), self.col.get_height())

    def checkcoll(self):
        for target in GM.instances:
            try :
                if self.rect.colliderect(target.rect):
                    if target.tag == "player" and self.allie == "enemy":
                        self.death()
                        target.hit()
                    elif target.tag == "enemy" and self.allie == "player":
                        self.death()
                        target.death()
            except:
                print("catch exception::Missile::checkcoll()")
                
    def update(self):
        self.checkcoll()
        self.now = pygame.time.get_ticks()
        self.Y += self.Dy
        self.rect = pygame.Rect(self.X, self.Y, self.col.get_width(), self.col.get_height())                
            
        if self.now - self.timer >= 2000: 
            self.timer = self.now
            self.death()
            
        GM.display.blit(self.col, (self.X, self.Y))
        
    def death(self):
        GM.instances.remove(self)

# main---------------------------------------------#
pygame.init()
GM.init()
while GM.running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            GM.running = False
            
    while GM.running and not GM.isgaov:
        GM.update()
        GM.callupdates(*GM.instances)
        pygame.display.update()
        GM.clock.tick(60)
        
        if GM.isgaov:
            GM.gameover()
            break
                
pygame.quit()
