import threading, time, turtle
global instances
instances = []

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
            
class Left(Behavior):
    def __init__(self):
        instances.append(self)
        
    def update(self):
        print("Left Update ")

class Right(Behavior):
    def __init__(self):
        instances.append(self)

    def update(self):
        print("Right Update ")

def createLeft():
    left = Left()

def createRight():
    right = Right()

def deleteObj():
    if len(instances) <= 0:
        return
    instances.pop()
    
                           
#main-----------------------------#
screen = turtle.Screen()
screen.onkey(createLeft,"Left")
screen.onkey(createRight,"Right")
screen.onkey(deleteObj, "space")
screen.listen()

while True:    
    Behavior.call_update(*instances)
    turtle.update()
    time.sleep(0.1)
    
turtle.mainloop()
#---------------------------------#

