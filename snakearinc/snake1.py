import pygame as pg
import random as rd

pg.init()
scrwidht = 400
scrheight = 400
gridl = 20
scr = pg.display.set_mode((scrwidht,scrheight))


class Apple:
    def __init__(self,image,pos):
        self.image = image
        self.pos = self.image.get_rect().move(pos)

    def eaten(self):
        self.pos = self.pos.move(self.pos.left*-1,self.pos.top*-1)
        self.pos = self.pos.move(rd.randint(0,scrwidht/gridl-1)*gridl,rd.randint(0,scrheight/gridl-1)*gridl)


class SnakePart:
    def __init__(self,image,type,heading,pos):
        self.type = type
        self.image = image
        self.heading = heading
        self.pos = self.image.get_rect().move(pos)

    def teleport(self,pos):
        self.pos = self.pos.move(-self.pos.left,-self.pos.top)
        self.pos = self.pos.move(pos)

    def move(self):
        global gameower
        headcorhist.append(self.pos.topleft)
        if self.heading == "up":
            self.xspd = 0
            self.yspd = -1*gridl
        elif self.heading == "down":
            self.xspd = 0
            self.yspd = 1*gridl
        elif self.heading == "right":
            self.xspd = 1*gridl
            self.yspd = 0
        elif self.heading == "left":
            self.xspd = -1*gridl
            self.yspd = 0
        self.pos = self.pos.move(self.xspd,self.yspd)


def blitobjs():
    scr.blit(bg1,(0,0))
    for o in slist:
        scr.blit(o.image,o.pos)
    scr.blit(apple.image,apple.pos)
    writetosc("Score: " + str(score), (280, 20), redclr)

def checkkeys():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                shead.heading = "up"
            elif event.key == pg.K_s:
                shead.heading = "down"
            elif event.key == pg.K_d:
                shead.heading = "right"
            elif event.key == pg.K_a:
                shead.heading = "left"


def writetosc(txt,pos,clr):
    text = font.render(txt,1,clr)
    scr.blit(text,pos)


def spawnbody():
    npos = headcorhist[-len(slist)]
    s = SnakePart(pg.image.load("sbody.png").convert(),"body","up",npos)
    slist.append(s)


def checkcol():
    global gameower
    if abs(apple.pos.center[0]-shead.pos.center[0]) < 10 and abs(apple.pos.center[1]-shead.pos.center[1]) < 10:
        global score
        apple.eaten()
        spawnbody()
        score += 1
    if abs(scrwidht+gridl - shead.pos.right) == 0 or abs(scrheight+gridl - shead.pos.bottom) == 0 or shead.pos.top < 0 or \
            shead.pos.left < 0:
        gameower = True
    for s in slist:
        if s.type == "body" and s.pos.topleft == shead.pos.topleft:
            gameower = True



def movebody():
    for i in range(1,len(slist)):
        slist[i].teleport(headcorhist[-i])



font = pg.font.SysFont("monospace",20)
goldclr = (255, 170, 0)
redclr = (255,0,0)
while True:
    scr.blit(pg.image.load("startsc.png").convert(),(0,0))
    try:
        writetosc("Score is: " + str(score), (100, 150), redclr)
    except: pass
    pg.display.update()
    kp = False
    while not kp:
        pg.time.delay(50)
        for event in pg.event.get():
            if event.type == pg.QUIT: quit()
            if event.type == pg.KEYDOWN: kp = True

    score = 0
    bg1 = pg.image.load('bg1.jpg').convert()
    scr.blit(bg1,(0,0))
    apple = Apple(pg.image.load("apple.png").convert(),(rd.randint(0,scrwidht/gridl-1)*gridl,(rd.randint(0,scrheight/gridl-1)*gridl)))
    shead = SnakePart(pg.image.load("shead.png").convert(),"head","right",(60,100))
    slist = [shead]
    headcorhist = []
    scr.blit(shead.image,shead.pos)
    scr.blit(apple.image,apple.pos)
    pg.display.update()

    gameower = False
    while not gameower:

        shead.move()
        checkkeys()
        movebody()
        checkcol()
        blitobjs()

        pg.display.update()
        pg.time.delay(200)
    scr.blit(pg.image.load("not_jumpscene.png").convert(),(0,0))
    pg.display.update()
    pg.time.delay(500)
