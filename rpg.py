import math
import random
import sys
import pygame as pg

WIDTH = 1600
HIGHT = 900
txt_origin = ["攻撃","防御","魔法","回復","調教","逃走"]
HP = 50
MP = 10
ENE_HP = 10

class Button:
    def __init__(self, x, y, width, height, color, hover_color, text, text_color, action, num):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.action = action
        self.num = num

    def draw(self,scr):
        pg.draw.rect(scr, self.color, self.rect)
        font = pg.font.SysFont("hg正楷書体pro", 50)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        scr.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action(self.num)
    
        
def action(i):
    p = ["攻撃","防御","魔法","回復","調教","逃走"]
    print(p[i])
        
def main():
    global WIDTH,HIGHT,txt_t,txt_origin
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
    font1 = pg.font.SysFont("hg正楷書体pro", 100)
    font2 = pg.font.SysFont("hg正楷書体pro", 50)
    text = "野生のスライムが現れた"
    txt = []
    text_surface1 = font2.render(f"HP:{HP} MP:{MP}", True, (255,255,255))
    text_surface2 = font2.render(f"HP:{ENE_HP}", True, (255,255,255))
    for i,tx in enumerate(txt_origin):
        if i%2==0:
            button = Button(125, 500+(i//2)*100, 100, 50, (50,50,50), (0,0,0), tx, (255,255,255), action, i)
        else:
            button = Button(275, 500+(i//2)*100, 100, 50, (50,50,50), (0,0,0), tx, (255,255,255), action, i)
        txt.append(button)
        
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            for button in txt:
                button.handle_event(event)

        screen.blit(bg_img,[0,0])
        screen.blit(ene_img,[WIDTH/2-ene_rct.width/2+100,HIGHT/2])
        screen.blit(win,[50,400])
        screen.blit(win2,[50,50])
        x=200
        for chr in text:
            rendered_text = font1.render(chr, True, (255, 255, 255))
            text_width = rendered_text.get_width()
            screen.blit(rendered_text,[x,100])
            x += text_width
        for i in txt:
            i.draw(screen)
        screen.blit(text_surface1,[100,350])
        screen.blit(text_surface2,[WIDTH/2-ene_rct.width/2+225,HIGHT/2-50])
        pg.display.update()
        clock.tick(100)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()