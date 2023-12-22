## Galaga
## 캐릭터는 아래에서 생성되어 상 하 좌 우 이동, 총알 발사
## 적은 위에서 생성되어 총알 발사
## get&set file 사용해 로컬에 랭크 저장
import time, turtle, random
#class----------------------------#
class Behavior:
        score = 0
    def __init__(self):
        
    def play_game(self):
        
    def save_rank(self):

    def gen_player(self):

    def gen_enemy(self):
        
    def update(self):
        pass
        
    def call_update(*instances):
        for instance ininstances:
            instance.update()
            
class Enemy(Behavior):
    def __init__(self):

    def fire(self):
        
    def death(self):
        
class eBullet(Behavior):
    def __init__(self):

    def destroy():
        
class Player(Behavior):
    def __init__(self):

    def fire(self):
        
    def death(self):
        
class pBullet(Behavior):
    def __init__(self):

    def destroy(self):

class UI(Behavior):
    def __init__(self):
        
#main-----------------------------#


behavior = Behavior()
While True:
    behavior.call_update()
    sleep(0.001)

#---------------------------------#
