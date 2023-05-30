import math
import time
import sys
import pygame as pg

WIDTH = 1600
HIGHT = 900
txt_origin = ["攻撃","防御","魔法","回復","調教","逃走"]
HP = 50
MP = 10
ENE_HP = 200
ENE_MP = 0
ATK = 10
MJC = 20
DEF = 10
TAM = 5
TAME_POINT = 20
ENE_ATK = 20

class Text:
    def __init__(self,syo):
        self.text = syo
    
    def draw(self, scr, text_color, x, y):
        font = pg.font.SysFont("hg正楷書体pro", 100)
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=(x,y))
        scr.blit(text_surface, text_rect)
        
class Button:
    def __init__(self, x, y, width, height, color, hover_color, text, text_color, action, num, text2, hp_mp):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.action = action
        self.num = num
        self.text2 = text2
        self.hp_mp = hp_mp

    def draw(self,scr):
        pg.draw.rect(scr, self.color, self.rect)
        font = pg.font.SysFont("hg正楷書体pro", 50)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        scr.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action(self.num, self.text2, self.hp_mp)
                
class HP_MP:
    def __init__(self,turn):
        self.hp = HP
        self.mp = MP
        self.turn = turn
        self.e_hp = ENE_HP
        self.font = pg.font.SysFont("hg正楷書体pro", 50)
        self.pl_hp = self.font.render(f"HP:{self.hp} MP:{self.mp}", True, (255,255,255))
        self.ene_hp = self.font.render(f"HP:{self.e_hp}", True, (255,255,255))
        self.PL_action = ""
        
    def PL(self,hp,mp):
        self.hp=hp
        self.mp=mp
        self.pl_hp = self.font.render(f"HP:{self.hp} MP:{self.mp}", True, (255,255,255))
        
    def ENE(self,e_hp):
        self.e_hp=e_hp
        self.ene_hp = self.font.render(f"HP:{self.e_hp}", True, (255,255,255))


def action(i,text:Text, hp_mp:HP_MP):
    hp = int(hp_mp.hp)
    mp = int(hp_mp.mp)
    ene_hp = int(hp_mp.e_hp)
    if hp_mp.turn==1:    
        if txt_origin[i]=="攻撃":
            text.text = f"{ATK}与えた"
            ene_hp -= ATK
            hp_mp.ENE(ene_hp)
            hp_mp.turn = 0
        if txt_origin[i]=="防御":
            text.text = "盾を構えた"
            hp_mp.turn = 0
        if txt_origin[i]=="魔法":
            if mp>0:
                text.text = f"{MJC}与えた"
                ene_hp -= MJC
                mp-=1
                hp_mp.turn = 0
            else:
                text.text = "MPが足りません"
            hp_mp.ENE(ene_hp)
            hp_mp.PL(hp,mp)
        if txt_origin[i]=="回復":
            if hp<HP and mp>0:
                nokori=HP-hp
                if nokori>MJC:
                    hp+=MJC
                else:
                    hp+=nokori
                mp-=1
                if hp>=HP:
                    hp=HP
                hp_mp.PL(hp,mp)
                text.text = f"{MJC}回復した"
                hp_mp.turn = 0
            elif mp<1:
                text.text = "MPが足りません"
            elif hp>=50:
                text.text = "体力が満タンです"
    if hp_mp.turn==0:
        hp_mp.PL_action = txt_origin[i]


def ENE_action(PL_action,hp_mp:HP_MP,text:Text):
    hp = int(hp_mp.hp)
    mp = int(hp_mp.mp)
    if PL_action=="防御":
        damege = ENE_ATK - DEF
        hp -= damege
        hp_mp.PL(hp,mp)
    else:
        damege = ENE_ATK
        hp -= damege
        hp_mp.PL(hp,mp)
    text.text=f"{damege}ダメージくらった"
    hp_mp.turn=1
    
            
def main():
    global WIDTH,HIGHT,txt_origin
    turn=1
    bg_image = "./ex05/fig/back.png"
    pg.display.set_caption("RPG初期段階")
    screen = pg.display.set_mode((WIDTH, HIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load(bg_image)
    bg_img = pg.transform.scale(bg_img,(WIDTH,HIGHT))
    ene_img = pg.image.load("./ex05/fig/ene.png")
    ene_rct = ene_img.get_rect()
    win = pg.image.load("./ex05/fig/win.png")
    win = pg.transform.scale(win,(WIDTH/4,HIGHT/2))
    win2 = pg.transform.scale(win,(WIDTH-100,HIGHT/4))
    syo="野生のスライムが現れた"
    text = Text(syo)
    txt = []
    text_surface = HP_MP(turn)
    for i,tx in enumerate(txt_origin):
        if i%2==0:
            button = Button(125, 500+(i//2)*100, 100, 50, 
                            (100,100,100), (0,0,0), tx, 
                            (255,255,255), action, 
                            i, text, text_surface)
        else:
            button = Button(275, 500+(i//2)*100, 100, 50, 
                            (100,100,100), (0,0,0), tx, 
                            (255,255,255), action, 
                            i, text, text_surface)
        txt.append(button)
        
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            for button in txt:
                button.handle_event(event)
        if text_surface.turn==0:
            PL_action=text_surface.PL_action
            ENE_action(PL_action,text_surface,text)
        screen.blit(bg_img,[0,0])
        screen.blit(ene_img,[WIDTH/2-ene_rct.width/2+100,HIGHT/2])
        screen.blit(win,[50,400])
        screen.blit(win2,[50,50])
        text.draw(screen, (255,255,255), WIDTH/2,150)
        for i in txt:
            i.draw(screen)
        screen.blit(text_surface.pl_hp, [100,350])
        screen.blit(text_surface.ene_hp, [WIDTH/2-ene_rct.width/2+225,HIGHT/2-50])
        pg.display.update()
        clock.tick(100)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()