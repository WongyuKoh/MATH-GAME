import sys
from random import *
import pygame
import time
from math import * 
import os
from pygame.locals import QUIT,KEYDOWN,K_LEFT,K_RIGHT,K_UP,K_DOWN,Rect,MOUSEBUTTONDOWN,K_SPACE,K_a,K_x,K_z,K_LCTRL,K_RCTRL ,VIDEORESIZE
pygame.init()
FPSCLOCK = pygame.time.Clock()

PATH=os.path.abspath('.')+'/image/'
#291 613
k=1.5
imsi_size=(291*k,613*k)
size=imsi_size
SURFACE = pygame.display.set_mode(size,pygame.RESIZABLE)
MAP_SIZE=(3,3) # 가로 세로
center=(size[0]/2,size[1]/2)
side_blank_space=[size[0]/10,size[1]/20]
mole_box_size=((size[0]-side_blank_space[0]*1)/MAP_SIZE[0],
               (size[0]-side_blank_space[0]*1)/MAP_SIZE[0]) # 가로, 세로

tile_left_up_pos=[center[0]-(MAP_SIZE[0]/2)*mole_box_size[0],center[1]-(MAP_SIZE[1]/2)*mole_box_size[1]]

color={
    "black":[0,0,0],
    "white":[255,255,255],
    "red":[255,0,0],
    "blue":[0,0,255],
    "yellow":[255,255,0],
    "green":[0,255,0],
    "gray":[192,192,192],
    "cyan":[0,183,235],
    "purple":[106,13,173],
    "orange":[249,146,69],
    "skyblue":[80,188,223],
    "whitegray":[214,213,203],
    "lightgreen":[129,193,71]
    }

MAP=[[0 for i in range(MAP_SIZE[0])]for g in range(MAP_SIZE[1])]
MAP_v=[[0 for i in range(MAP_SIZE[0])]for g in range(MAP_SIZE[1])]

class PB(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.SURFACE=SURFACE
        self.board_pos=(size[0]/2,side_blank_space[1]) # 중앙 x 좌표, 상단 y좌표


        self.board_image=pygame.image.load(PATH+"board.png").convert_alpha()
        self.board_image_rect=self.board_image.get_rect()
        K=(size[0]-side_blank_space[0]*4)/self.board_image_rect.height
        self.board_size=[self.board_image_rect.height*K*1.5,self.board_image_rect.width*K/2.3]
        
        """print((size[0]-side_blank_space[0]*4))
        print(self.board_image_rect.height,self.board_image_rect.width)
        print(self.board_size)"""
        
        self.board_image=pygame.transform.scale(self.board_image,self.board_size)
        self.board_image_rect=self.board_image.get_rect()
        self.board_image_mask=pygame.mask.from_surface(self.board_image)
        self.board_image_rect.midtop=self.board_pos
        
        self.text_size=50
        
        self.myFont = pygame.font.SysFont( "arial", self.text_size, True, False) 
        self.port_myFont = pygame.font.SysFont( "arial", self.text_size//3, True, False) 
        self.text="5,15,□,35,45,55"
        self.port_text="a"
        self.text_pos=(self.board_pos[0],self.board_pos[1]+self.board_size[1]/2-4)
        #_Title= self.myFont.render("Pygame Text Test", True, color["black"])
        
        self.first_element=randint(1,5)
        self.d=randint(1,10)
        self.answer=0
        self.percent=[0,0]
        self.last_percent=[1,MAP_SIZE[0]*MAP_SIZE[1]]
        
        self.PB_category={
            "blank":0,\

            
        }
        
        self.pb_list=list(self.PB_category)
        
    def n_port_draw(self,n,pos):
        TEXT = self.myFont.render(self.port_text, True, color["black"])
        rect=TEXT.get_rect()
        rect.midleft=pos
        self.SURFACE.blit(TEXT,rect)
        
        TEXT = self.port_myFont.render(str(n), True, color["black"])
        rect=TEXT.get_rect()
        rect.topleft=(pos[0]+self.text_size/2,pos[1]+self.text_size/4)
        self.SURFACE.blit(TEXT,rect)


        
    def draw(self):
        
        
        TEXT = self.myFont.render(self.text, True, color["black"])
        self.text_rect=TEXT.get_rect()
        self.text_rect.center=self.text_pos
        
        
        self.SURFACE.blit(self.board_image,self.board_image_rect)
        self.SURFACE.blit(TEXT,self.text_rect)
        
        #self.n_port_draw(13,(self.text_pos[0]-self.text_size/2,self.text_pos[1]))
        
    def new_pb(self):
        self.text=""
        self.first_element=randint(1,5)
        self.d=randint(1,10)
        category=self.pb_list[randint(0,len(self.pb_list)-1)]
        self.percent=[1,MAP_SIZE[0]*MAP_SIZE[1]]
        if category=="blank":
            number=randint(3,6)
            idx=randint(1,number)
            v=self.first_element
            for i in range(number):
                if idx==i+1:
                    self.text+="□"
                    self.answer=v
                else:
                    self.text+=str(v)
                v+=self.d

                if i+1!=number:
                    self.text+=","
        
class MOLE(pygame.sprite.Sprite):
    def __init__(self,pos,text):

        pygame.sprite.Sprite.__init__(self)
        self.SURFACE=SURFACE
        self.pos=pos

        self.mole_pos=[self.pos[0],self.pos[1]+25]
        
        self.k=5.5
        
        self.POS=[0,0]
        
        #mole
        self.mole_image=pygame.image.load(PATH+"mole.png").convert_alpha()
        self.mole_image_Rect=self.mole_image.get_rect()
        self.mole_image_size=(self.mole_image_Rect.height/self.k,self.mole_image_Rect.width/self.k)
        self.mole_image=pygame.transform.scale(self.mole_image,self.mole_image_size)
        self.mole_image_Rect=self.mole_image.get_rect()
        self.mole_image_image_mask=pygame.mask.from_surface(self.mole_image)
        self.mole_image_Rect.center=self.mole_pos
        
        self.mole_vo=Virtual_Object([self.mole_image,self.mole_image_Rect,self.mole_image_image_mask])
        
        #hide up
        self.mole_up_image=pygame.image.load(PATH+"hide_up.png").convert_alpha()
        self.mole_up_image_Rect=self.mole_up_image.get_rect()
        self.mole_up_image_size=(self.mole_up_image_Rect.width/self.k,self.mole_up_image_Rect.height/self.k)
        self.mole_up_image=pygame.transform.scale(self.mole_up_image,self.mole_up_image_size)
        self.mole_up_image_Rect=self.mole_up_image.get_rect()
        self.mole_up_image_mask=pygame.mask.from_surface(self.mole_up_image)
        self.mole_up_image_Rect.midbottom = (self.pos[0],self.pos[1])

        
        #hide down
        self.mole_down_image=pygame.image.load(PATH+"hide_down.png").convert_alpha()
        self.mole_down_image_Rect=self.mole_down_image.get_rect()
        self.mole_down_image_size=(self.mole_down_image_Rect.width/self.k,self.mole_down_image_Rect.height/self.k)
        self.mole_down_image=pygame.transform.scale(self.mole_down_image,self.mole_down_image_size)
        self.mole_down_image_Rect=self.mole_down_image.get_rect()
        self.mole_down_image_mask=pygame.mask.from_surface(self.mole_down_image)
        self.mole_down_image_Rect.midtop = (self.pos[0],self.pos[1]-1)

        
        #hole in
        self.hole_in_image=pygame.image.load(PATH+"hole_in.png").convert_alpha()
        self.hole_in_image_Rect=self.hole_in_image.get_rect()
        self.hole_in_image_size=(self.hole_in_image_Rect.width/self.k,self.hole_in_image_Rect.height/self.k)
        self.hole_in_image=pygame.transform.scale(self.hole_in_image,self.hole_in_image_size)
        self.hole_in_image_Rect=self.hole_in_image.get_rect()
        self.hole_in_image_mask=pygame.mask.from_surface(self.hole_in_image)
        self.hole_in_image_Rect.center = self.pos
        
        
        #text
        
        self.myFont = pygame.font.SysFont( "arial", 22, True, False) # 7자리 20, 6자리 22, 5자리 25, 4자리 30  | 최대 30
        self.text=str(text)
        self.text_pos=(self.mole_pos[0],self.mole_pos[1]+10)
        #_Title= self.myFont.render("Pygame Text Test", True, color["black"])
        
        self.up=0
        self.v=1
        self.uptime=uniform(1,2)
        self.birthtime=time.time()
        self.delay_time=uniform(0,5)
        #print(self.delay_time)

        self.delete=0
        
    def draw(self):
        if self.up==1:
            if self.pos[1]-self.mole_pos[1]<25:
                self.mole_pos[1]-=0.5*self.v
        if self.up==-1:
            if self.pos[1]-self.mole_pos[1]>-25:
                self.mole_pos[1]+=0.5*self.v
            else:
                self.delete=1
            
                
        self.mole_image_Rect.center=self.mole_pos
        self.mole_vo.rect=self.mole_image_Rect
        self.text_pos=(self.mole_pos[0],self.mole_pos[1]+10)
        #self.mole_up_image_Rect.midbottom = (self.pos[0],self.pos[1])
        #self.mole_down_image_Rect.midtop = (self.pos[0],self.pos[1]-1)
        #self.hole_in_image_Rect.center = self.pos
        
        TEXT = self.myFont.render(self.text, True, color["black"])
        self.text_rect=TEXT.get_rect()
        self.text_rect.center=self.text_pos
        
        self.SURFACE.blit(self.hole_in_image,self.hole_in_image_Rect) # mole
        self.SURFACE.blit(self.mole_up_image,self.mole_up_image_Rect) # hide up
        self.SURFACE.blit(self.mole_image,self.mole_image_Rect) # mole
        self.SURFACE.blit(TEXT,self.text_rect) # text
        self.SURFACE.blit(self.mole_down_image,self.mole_down_image_Rect) # hide down
            
class MousePointer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.SURFACE=SURFACE
        self.pos=(0,0)
        
        #hammer
        self.mousepointer_image=pygame.image.load(PATH+"hammer.png").convert_alpha()
        self.mousepointer_Rect=self.mousepointer_image.get_rect()
        self.mousepointer_size=(self.mousepointer_Rect.height/7,self.mousepointer_Rect.width/7)
        self.mousepointer_image=pygame.transform.scale(self.mousepointer_image,self.mousepointer_size)
        self.mousepointer_Rect=self.mousepointer_image.get_rect()
        self.mousepointer_image_mask=pygame.mask.from_surface(self.mousepointer_image)
        
        #hammer crash
        self.mousepointer_crash_image=pygame.image.load(PATH+"hammer_crash.png").convert_alpha()
        self.mousepointer_crash_image=pygame.transform.scale(self.mousepointer_crash_image,self.mousepointer_size)
        self.mousepointer_crash_Rect=self.mousepointer_crash_image.get_rect()
        self.mousepointer_crash_image_mask=pygame.mask.from_surface(self.mousepointer_crash_image)
        
        self.draw_image=0 # 0 : hammer 1 : hammer crash
        self.crash_delay=0.3
        self.crash_time=0
        
    def draw(self,pos):
        if self.draw_image==0:
            self.mousepointer_Rect.center=pos
            self.SURFACE.blit(self.mousepointer_image,self.mousepointer_Rect)
        else:
            self.mousepointer_crash_Rect.center=pos
            self.SURFACE.blit(self.mousepointer_crash_image,self.mousepointer_crash_Rect)
        
    def crash(self):
        self.draw_image=1
        self.crash_time=time.time()
        
    def crash_stop(self):
        self.draw_image=0
        
class Virtual_Object(pygame.sprite.Sprite):
    def __init__(self,object): #object = [image, rect, mask]
        pygame.sprite.Sprite.__init__(self)
        self.image=object[0]
        self.rect=object[1]
        self.mask=object[2]
        self.radius=0

class ALARM():
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.SURFACE=SURFACE
        
        #alarm
        self.Gamerule=0
        self.Gameclear=0
        
        

        
        
        #game start
        self.start_size=(100*1.5,50*1.5)
        self.start_image=pygame.image.load(PATH+"start.png").convert_alpha()
        self.start_image=pygame.transform.scale(self.start_image,self.start_size)
        self.start_Rect=self.start_image.get_rect()
        self.start_image_mask=pygame.mask.from_surface(self.start_image)
        self.start_Rect.center=(size[0]/2, side_blank_space[1]*13)
        self.start_vo=Virtual_Object([self.start_image,self.start_Rect,self.start_image_mask])
        
        #explanation
        self.gamerule_size=(100*1.5,50*1.5)
        self.gamerule_image=pygame.image.load(PATH+"gamerule.png").convert_alpha()
        self.gamerule_image=pygame.transform.scale(self.gamerule_image,self.gamerule_size)
        self.gamerule_Rect=self.gamerule_image.get_rect()
        self.gamerule_image_mask=pygame.mask.from_surface(self.gamerule_image)
        self.gamerule_Rect.center=(size[0]/2, side_blank_space[1]*14 + self.start_size[1])
        self.gamerule_vo=Virtual_Object([self.gamerule_image,self.gamerule_Rect,self.gamerule_image_mask])
        
        #game clear
        ## retry button
        self.re_b_size=(100,50)
        self.re_b_image=pygame.image.load(PATH+"re.png").convert_alpha()
        self.re_b_image=pygame.transform.scale(self.re_b_image,self.re_b_size)
        self.re_b_Rect=self.re_b_image.get_rect()
        self.re_b_image_mask=pygame.mask.from_surface(self.re_b_image)
        self.re_txt_size=25
        self.re_b_Rect.center=(size[0]/2, side_blank_space[1]*8)
        self.re_b_vo=Virtual_Object([self.re_b_image,self.re_b_Rect,self.re_b_image_mask])
        
        
        
        self.re_text_font = pygame.font.SysFont("malgungothic", self.re_txt_size, True, False)
        self.re_text=\
        """
        """
        
        ##blurred effect
        self.blurred_effect_size=size
        self.blurred_effect_image=pygame.image.load(PATH+"background_blurred_effect.png").convert_alpha()
        self.blurred_effect_image=pygame.transform.scale(self.blurred_effect_image,self.blurred_effect_size)
        self.blurred_effect_image.set_alpha(230)
        self.blurred_effect_Rect=self.blurred_effect_image.get_rect()
        self.blurred_effect_image_mask=pygame.mask.from_surface(self.blurred_effect_image)
        
        #close button
        self.closebutton_size=(50,50)
        self.closebutton_image=pygame.image.load(PATH+"closebutton.png").convert_alpha()
        self.closebutton_image=pygame.transform.scale(self.closebutton_image,self.closebutton_size)
        self.closebutton_Rect=self.closebutton_image.get_rect()
        self.closebutton_image_mask=pygame.mask.from_surface(self.closebutton_image)
        self.txt_size=15
        self.closebutton_Rect.center=(size[0]-side_blank_space[0]-side_blank_space[0]/4, side_blank_space[1]*3)
        self.close_button_vo=Virtual_Object([self.closebutton_image,self.closebutton_Rect,self.closebutton_image_mask])
        
        self.text_font = pygame.font.SysFont("malgungothic", self.txt_size, True, False)
        
        self.text=\
        "두더지 때리기 게임에 오신걸 환영합니다!!\n\n"+\
        "두더지 때리기 게임은 기존 두더지 때리기 게임처럼 \n\n"+\
        "두더지가 올라왔을 때 때리면 되는 간단한 게임입니다. \n\n\n "+\
        "하지만 기존과 다르게 \n\n 두더지가 들고 올라오는 칠판에 숫자가 쓰여있습니다. \n\n\n"+\
        "칠판에 쓰여져 있는 숫자는 \n\n상단 보드판에 나타난 문제에 대한 답입니다.\n\n"+\
        "상단 보드판에는 등차수열의 형태로 나타나게 되는데, \n\n"+\
        "그중 □ 가 있는 곳에 들어갈 숫자를 골라주시면 됩니다. \n\n\n\n"+\
        "등차수열이란?\n\n"+\
        "첫번째항부터 차례로 일정한 수를 더하여 \n\n 만들어지는 수열을 말합니다.\n\n"+\
        "이때 첫번째 항을 초항, \n\n 더하는 일정한 수를 공차라고 합니다.\n\n"+\
        "이정도 내용을 숙지하고 이제 게임을 즐겨봅시다!!"
        

        
    def retry_button(self):
        self.SURFACE.blit(self.re_b_image,self.re_b_Rect)
        
    def start_button(self):
        self.SURFACE.blit(self.start_image,self.start_Rect)
        
    def gamerule_button(self):
        self.SURFACE.blit(self.gamerule_image,self.gamerule_Rect)
        
    def blurred_effect(self):
        self.SURFACE.blit(self.blurred_effect_image,self.blurred_effect_Rect)
        
    def close_button(self):
        self.SURFACE.blit(self.closebutton_image,self.closebutton_Rect)
        
    def close_button_click(self):
        self.Gamerule=0

        
    def gamerule(self):
        self.blurred_effect()
        pygame.draw.rect(self.SURFACE,color["whitegray"],[side_blank_space[0]/2,side_blank_space[1]*2,size[0]-side_blank_space[0],size[1]-side_blank_space[1]*4])
        self.close_button()
        stack=self.text.split("\n")
        for i in range(len(stack)):
            print(stack[i])
            text_Title=self.text_font.render(stack[i], True, color["black"])
            Rect=text_Title.get_rect()
            Rect.midtop=(size[0]/2,side_blank_space[1]*2.5+self.closebutton_size[1] + self.txt_size*i)
            self.SURFACE.blit(text_Title, Rect)
    
 
    def gameclear(self,SCORE): # time 은 남은 시간
        self.blurred_effect()
        self.Gameclear=2
        pygame.draw.rect(self.SURFACE,color["whitegray"],[side_blank_space[0]/2,side_blank_space[1]*2,size[0]-side_blank_space[0],size[1]-side_blank_space[1]*10])
        
        self.re_text=f"Game Finished!!\nYour Score is {SCORE}"
            
        self.retry_button()
        stack=self.re_text.split("\n")
        for i in range(len(stack)):
            text_Title=self.re_text_font.render(stack[i], True, color["black"])
            Rect=text_Title.get_rect()
            Rect.midtop=(size[0]/2,side_blank_space[1]*2+self.re_b_size[1] + self.re_txt_size*i)
            self.SURFACE.blit(text_Title, Rect)

class interface():
    def __init__(self,time_pos):
        pygame.sprite.Sprite.__init__(self)
        self.SURFACE=SURFACE
        

        #time
        self.playtime=0
        self.start_time=0
        self.time_pos=time_pos
        self.time_size=40
        self.time_font = pygame.font.SysFont("arial", self.time_size, True, False)
        self.Time=0
        
        #score
        self.score_pos=(self.time_pos[0],self.time_pos[1]+self.time_size)
        self.score_size=30
        self.score_font = pygame.font.SysFont("arial", self.score_size, True, False)
        
            
        
    def time_draw(self):
        self.Time=self.playtime-(time.time()-self.start_time)
        text_Title=self.time_font.render(f"{int(self.Time//60)} : {round(self.Time%60,1)}", True, color["black"])
        Rect=text_Title.get_rect()
        Rect.x=self.time_pos[0]
        Rect.y=self.time_pos[1]
        self.SURFACE.blit(text_Title, Rect)
        
    def score_draw(self,score):
        text_Title=self.score_font.render(f"score : {score}", True, color["black"])
        Rect=text_Title.get_rect()
        Rect.x=self.score_pos[0]
        Rect.y=self.score_pos[1]
        self.SURFACE.blit(text_Title, Rect)
    
    def game_start(self):
        self.start_time=time.time()
        self.playtime=60

def new_mole(pos,p,ans):
    RD=randint(1,p[1]+1)
    if RD<=p[0]:
        #answer
        MAP_v[pos[1]][pos[0]]=ans
        MAP[pos[1]][pos[0]]=MOLE([tile_left_up_pos[0]+mole_box_size[0]*pos[0]+mole_box_size[0]/2,
                                tile_left_up_pos[1]+mole_box_size[1]*pos[1]+mole_box_size[1]/2],MAP_v[pos[1]][pos[0]])
        MAP[pos[1]][pos[0]].POS=pos
    
        return 1
    else:
        #not answer
        if randint(1,2)==1:
            MAP_v[pos[1]][pos[0]]=randint(ans-10,ans-1)
        else:
            MAP_v[pos[1]][pos[0]]=randint(ans+1,ans+10)
            
        MAP[pos[1]][pos[0]]=MOLE([tile_left_up_pos[0]+mole_box_size[0]*pos[0]+mole_box_size[0]/2,
                                tile_left_up_pos[1]+mole_box_size[1]*pos[1]+mole_box_size[1]/2],MAP_v[pos[1]][pos[0]])
        MAP[pos[1]][pos[0]].POS=pos

        return 0

def GAMESTART():
    global MAP,MAP_v,mousepointer,alarm,INTERFACE
    
    alarm.Gameclear=0
    


    PROBLEM=PB()
    PROBLEM.new_pb()
    SCORE=0

    MAP_v=[[0 for i in range(MAP_SIZE[0])]for g in range(MAP_SIZE[1])]
    MAP=[[MOLE([tile_left_up_pos[0]+mole_box_size[0]*i+mole_box_size[0]/2,
                tile_left_up_pos[1]+mole_box_size[1]*g+mole_box_size[1]/2],123) for i in range(MAP_SIZE[0])]for g in range(MAP_SIZE[1])]
        
    for i in range(MAP_SIZE[1]):
        for g in range(MAP_SIZE[0]):
            change=new_mole((g,i),PROBLEM.percent,PROBLEM.answer)
            if change==1:
                PROBLEM.last_percent=[*PROBLEM.percent]
                PROBLEM.last_percent[0]=min(PROBLEM.last_percent[0],PROBLEM.last_percent[1])
                PROBLEM.percent[0]=1
                PROBLEM.percent[1]+=1
            else:
                PROBLEM.percent[0]+=1
            
    INTERFACE.game_start()

    while 1:

        SURFACE.fill(color["lightgreen"])
        
        if alarm.Gameclear:
        
            for EVENT in pygame.event.get():
                if EVENT.type==QUIT:pygame.quit();sys.exit()
                if EVENT.type==MOUSEBUTTONDOWN:
                                
                    if pygame.mouse.get_pressed()[0]:

                        A=Virtual_Object([mousepointer.mousepointer_image,mousepointer.mousepointer_Rect,mousepointer.mousepointer_image_mask])
                        
                        if pygame.sprite.collide_mask(A,alarm.re_b_vo):
                            return
                        
                        
            
        if alarm.Gameclear:
            alarm.gameclear(SCORE)
        
        if alarm.Gameclear==0:
        
            for EVENT in pygame.event.get():
                if EVENT.type==QUIT:pygame.quit();sys.exit()
                if EVENT.type==MOUSEBUTTONDOWN:

                
                    
                    if pygame.mouse.get_pressed()[0]:
                        
                        mouse_pos=pygame.mouse.get_pos()
                        mouse_pos_idx=[(mouse_pos[0]-tile_left_up_pos[0])//mole_box_size[0],(mouse_pos[1]-tile_left_up_pos[1])//mole_box_size[1]]
                        #print(mouse_pos_idx) #x,y
                        mouse_pos_idx[0]=int(mouse_pos_idx[0])
                        mouse_pos_idx[1]=int(mouse_pos_idx[1])
                        if 0<=mouse_pos_idx[0]<MAP_SIZE[0] and 0<=mouse_pos_idx[1]<MAP_SIZE[1]:
                        
                            A=Virtual_Object([mousepointer.mousepointer_image,mousepointer.mousepointer_Rect,mousepointer.mousepointer_image_mask])
                            B=MAP[mouse_pos_idx[1]][mouse_pos_idx[0]].mole_vo
                            
                            """print((MAP[mouse_pos_idx[1]][mouse_pos_idx[0]].mole_image_Rect.centerx,
                                MAP[mouse_pos_idx[1]][mouse_pos_idx[0]].mole_image_Rect.centery),
                                mouse_pos)"""
                            
                            if pygame.sprite.collide_mask(A,B):
                                if mousepointer.draw_image==0:
                                    if MAP[mouse_pos_idx[1]][mouse_pos_idx[0]].up!=0:
                                        #print("!!!!")
                                        if PROBLEM.answer==MAP_v[mouse_pos_idx[1]][mouse_pos_idx[0]]:
                                            #print("-"*30)
                                            PROBLEM.new_pb()
                                            
                                            PROBLEM.percent=[1,MAP_SIZE[0]*MAP_SIZE[1]]
                                            PROBLEM.last_percent=[1,MAP_SIZE[0]*MAP_SIZE[1]]
                                            for i in range(MAP_SIZE[1]):
                                                for g in range(MAP_SIZE[0]):
                                                    if i==mouse_pos_idx[1] and g==mouse_pos_idx[0]:continue
                                                    if PROBLEM.answer==MAP_v[i][g]:
                                                        PROBLEM.last_percent=[*PROBLEM.percent]
                                                        PROBLEM.last_percent[0]=min(PROBLEM.last_percent[0],PROBLEM.last_percent[1])
                                                        PROBLEM.percent[0]=1
                                                        PROBLEM.percent[1]+=1
                                                    else:
                                                        PROBLEM.percent[0]+=1
                                                        
                                            new_mole(mouse_pos_idx,PROBLEM.last_percent,PROBLEM.answer)
                                            SCORE+=3
                                        
                                        else:
                                            SCORE-=1
                                            
                                        MAP[mouse_pos_idx[1]][mouse_pos_idx[0]].up=-1
                                        MAP[mouse_pos_idx[1]][mouse_pos_idx[0]].v*=2
                                            
                                        
                                                        
                                        mousepointer.crash()
                                    #MAP[mouse_pos_idx[1]][mouse_pos_idx[0]].up*=-1
                
            """pos=[*tile_left_up_pos]
            for i in range(MAP_SIZE[0] + 1):
                #세로줄
                pygame.draw.line(SURFACE,color["black"],[pos[0],pos[1]],[pos[0],pos[1]+MAP_SIZE[1]*mole_box_size[1]])
                pos[0]+=mole_box_size[0]
                
            pos=[*tile_left_up_pos]
            for i in range(MAP_SIZE[1] + 1):
                #가로줄
                pygame.draw.line(SURFACE,color["black"],[pos[0],pos[1]],[pos[0]+MAP_SIZE[0]*mole_box_size[0],pos[1]])
                pos[1]+=mole_box_size[1]"""
                
                
            for i in range(MAP_SIZE[1]):
                for g in range(MAP_SIZE[0]):
                    if MAP[i][g].up==0:
                        if time.time()-MAP[i][g].birthtime>=MAP[i][g].delay_time:
                            MAP[i][g].up=1
                            MAP[i][g].birthtime=time.time()
                            #print("!#!",i,g)
                        
                    if MAP[i][g].up==1 and time.time()-MAP[i][g].birthtime>=MAP[i][g].uptime:
                        MAP[i][g].up=-1
                    MAP[i][g].draw()
                    if MAP[i][g].delete==1:
                        if MAP_v[i][g]==PROBLEM.answer:
                            new_mole((g,i),PROBLEM.last_percent,PROBLEM.answer)
                        else:
                            PROBLEM.percent[0]-=1
                            PROBLEM.percent[0]=max(1,PROBLEM.percent[0])
                            new_mole((g,i),PROBLEM.percent,PROBLEM.answer)
                        
                    
            PROBLEM.draw()
        
        mousepointer.draw(pygame.mouse.get_pos())

        if mousepointer.draw_image==1 and time.time()-mousepointer.crash_time>=mousepointer.crash_delay:
            mousepointer.crash_stop()
            
        if alarm.Gameclear==0:
            
            INTERFACE.time_draw()
            INTERFACE.score_draw(SCORE)
            
            if time.time()-INTERFACE.start_time>=INTERFACE.playtime:
                alarm.gameclear(SCORE)
        
            
        pygame.display.update()
    
background_image=pygame.image.load(PATH+"background.png").convert_alpha()
background_image_rect=background_image.get_rect()
K=size[0]/background_image_rect.width
background_image_size=[background_image_rect.width*K,background_image_rect.height*K]
background_image=pygame.transform.scale(background_image,background_image_size)
background_image_rect=background_image.get_rect()
background_image_rect.topleft=(0,0)
    
mousepointer=MousePointer()
alarm=ALARM()
INTERFACE=interface([side_blank_space[0],size[1]-side_blank_space[1]*5])
    
while 1:
    SURFACE.fill(color["lightgreen"])
    SURFACE.blit(background_image,background_image_rect)
    for EVENT in pygame.event.get():
        if EVENT.type==QUIT:pygame.quit();sys.exit()
        if EVENT.type==VIDEORESIZE:
            size=(EVENT.w,EVENT.h)#(291*k,613*k)
            SURFACE = pygame.display.set_mode(size,pygame.RESIZABLE)
            
        if EVENT.type==MOUSEBUTTONDOWN:
        
            if alarm.Gamerule==1:
                if pygame.mouse.get_pressed()[0]:
                    
                    A=Virtual_Object([mousepointer.mousepointer_image,mousepointer.mousepointer_Rect,mousepointer.mousepointer_image_mask])
                    
                    
                    if pygame.sprite.collide_mask(A,alarm.close_button_vo):
                        alarm.Gamerule=0
            
            if pygame.mouse.get_pressed()[0]:

                A=Virtual_Object([mousepointer.mousepointer_image,mousepointer.mousepointer_Rect,mousepointer.mousepointer_image_mask])
                
                
                if pygame.sprite.collide_mask(A,alarm.start_vo):
                    GAMESTART()
                        
                if pygame.sprite.collide_mask(A,alarm.gamerule_vo):
                    alarm.Gamerule=1
                
                
    if alarm.Gamerule==1:
        alarm.gamerule()
                
    else:           
        alarm.start_button()
        alarm.gamerule_button()
    mousepointer.draw(pygame.mouse.get_pos())
    
    pygame.display.update()