## Galaga
## 캐릭터는 아래에서 생성되어 상 하 좌 우 이동, 총알 발사
## 적은 위에서 생성되어 총알 발사
## get&set file 사용해 로컬에 랭크 저장

#import---------------------------#
import time, turtle, random, threading
#global---------------------------#
global instances
instances = []
#class----------------------------#
class Behavior:
    def update(self):
        pass
    
    @classmethod
    def call_update(cls, *instances):
        threads = []
        for instance in instances:
            thread = threading.Thread(target=instance.update)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
            
class Enemy(Behavior):
    def __init__(self):
        instances.append(self)
        
    def update(self):
        print("Enemy update\n")
        
class eBullet(Behavior):
    def __init__(self):
        instances.append(self)
        
    def update(self):
        print("eBullet update\n")
        
class Player(Behavior):
    def __init__(self):
        instances.append(self)
        self.col = turtle.Turtle()
        self.col.speed(5)
        self.col.shape("turtle")
        self.col.left(90)
        
    def update(self):
         print("Player update\n")

    def moveL(self):
        print("move left")
        x = self.col.xcor()
        y = self.col.ycor()
        self.col.goto(x-50,y)
        
    def moveR(self):
        print("move right")
        x = self.col.xcor()
        y = self.col.ycor()
        self.col.goto(x+50,y)
        
class pBullet(Behavior):
    def __init__(self):
        instances.append(self)
        
    def update(self):
        print("pBullet update\n")
        
class UI(Behavior):
    def __init__(self):
        instances.append(self)
        
    def update(self):
        print("UI update\n")
#main-----------------------------#
screen = turtle.Screen()
player = Player()

.onkeypress(lambda: player.moveL(),"Left")
.onkeypress(lambda: player.moveR(),"Right")

#while True:
#    Behavior.call_update(*instances)
#    time.sleep(0.001)

#---------------------------------#
