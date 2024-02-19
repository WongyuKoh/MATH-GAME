# 최적화
#https://velog.io/@whdnjsdyd111/python-library-pygame-1.-%EA%B0%9C%EC%9A%94#%EC%B5%9C%EC%A0%81%ED%99%94
#https://camel-it.tistory.com/140

# 그룹
# https://gusrl4025.tistory.com/7
# http://cs.sch.ac.kr/lecture/Python/6-PythonGUI-sprite.pdf

# 가상환경
# https://oceanlightai.tistory.com/25
# https://velog.io/@jaehyeong/%EC%95%84%EB%82%98%EC%BD%98%EB%8B%A4Anaconda-%EA%B0%80%EC%83%81%ED%99%98%EA%B2%BD-%EC%83%9D%EC%84%B1


"""import gspread
from oauth2client.service_account import ServiceAccountCredentials"""

import sys
from random import *
import pygame
import time
from copy import deepcopy as dc
from math import * 
import os
from pygame.locals import QUIT,KEYDOWN,K_LEFT,K_RIGHT,K_UP,K_DOWN,Rect,MOUSEBUTTONDOWN,K_SPACE,K_a,K_x,K_z,K_LCTRL,K_RCTRL ,VIDEORESIZE
pygame.init()
FPSCLOCK = pygame.time.Clock()

class Virtual_Object(pygame.sprite.Sprite):
    def __init__(self,object): #object = [image, rect, mask]
        pygame.sprite.Sprite.__init__(self)
        self.image=object[0]
        self.rect=object[1]
        self.mask=object[2]
        self.radius=0


font_path=os.getenv('SystemRoot')
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

MAP=[]

IMAGE={
    "board.png":pygame.image.load(PATH+"board.png").convert_alpha(),
    "mole.png":pygame.image.load(PATH+"mole.png").convert_alpha(),
    "hide_up.png":pygame.image.load(PATH+"hide_up.png").convert_alpha(),
    "hide_down.png":pygame.image.load(PATH+"hide_down.png").convert_alpha(),
    "hole_in.png":pygame.image.load(PATH+"hole_in.png").convert_alpha(),
    "hammer.png":pygame.image.load(PATH+"hammer.png").convert_alpha(),
    "hammer_crash.png":pygame.image.load(PATH+"hammer_crash.png").convert_alpha(),
    "start.png":pygame.image.load(PATH+"start.png").convert_alpha(),
    "gamerule.png":pygame.image.load(PATH+"gamerule.png").convert_alpha(),
    "re.png":pygame.image.load(PATH+"re.png").convert_alpha(),
    "background_blurred_effect.png":pygame.image.load(PATH+"background_blurred_effect.png").convert_alpha(),
    "closebutton.png":pygame.image.load(PATH+"closebutton.png").convert_alpha(),
    "background.png":pygame.image.load(PATH+"background.png").convert_alpha(),
       
}
MASK={}
#board.png
K=(size[0]-side_blank_space[0]*4)/IMAGE["board.png"].get_height()
board_size=[IMAGE["board.png"].get_height()*K*1.5,IMAGE["board.png"].get_width()*K/2.3]
IMAGE["board.png"]=pygame.transform.scale(IMAGE["board.png"],board_size)
MASK['board.png']=pygame.mask.from_surface(IMAGE["board.png"])

#mole
k=5.5
mole_image_size=(IMAGE["mole.png"].get_height()/k,IMAGE["mole.png"].get_width()/k)
IMAGE["mole.png"]=pygame.transform.scale(IMAGE["mole.png"],mole_image_size)
MASK['mole.png']=pygame.mask.from_surface(IMAGE["mole.png"])
up_distnace=mole_image_size[1]*(25/(512/k))


#hide up
mole_up_image_size=(IMAGE['hide_up.png'].get_width()/k,IMAGE['hide_up.png'].get_height()/k)
IMAGE['hide_up.png']=pygame.transform.scale(IMAGE['hide_up.png'],mole_up_image_size)
MASK['hide_up.png']=pygame.mask.from_surface(IMAGE['hide_up.png'])


#hide down
mole_down_image_size=(IMAGE['hide_down.png'].get_width()/k,IMAGE['hide_down.png'].get_height()/k)
IMAGE['hide_down.png']=pygame.transform.scale(IMAGE['hide_down.png'],mole_down_image_size)
MASK['hide_down.png']=pygame.mask.from_surface(IMAGE['hide_down.png'])


#hole in
hole_in_image_size=(IMAGE['hole_in.png'].get_width()/k,IMAGE['hole_in.png'].get_height()/k)
IMAGE['hole_in.png']=pygame.transform.scale(IMAGE['hole_in.png'],hole_in_image_size)
MASK['hole_in.png']=pygame.mask.from_surface(IMAGE['hole_in.png'])

#hammer
mousepointer_size=(IMAGE['hammer.png'].get_height()/7,IMAGE['hammer.png'].get_width()/7)
IMAGE['hammer.png']=pygame.transform.scale(IMAGE['hammer.png'],mousepointer_size)
MASK['hammer.png']=pygame.mask.from_surface(IMAGE['hammer.png'])

#hammer crash
IMAGE['hammer_crash.png']=pygame.transform.scale(IMAGE['hammer_crash.png'],mousepointer_size)
MASK['hammer_crash.png']=pygame.mask.from_surface(IMAGE['hammer_crash.png'])

#game start
start_size=(100*1.5,50*1.5)
IMAGE["start.png"]=pygame.transform.scale(IMAGE["start.png"],start_size)
MASK["start.png"]=pygame.mask.from_surface(IMAGE["start.png"])

#explanation
gamerule_size=(100*1.5,50*1.5)
IMAGE["gamerule.png"]=pygame.transform.scale(IMAGE["gamerule.png"],gamerule_size)
MASK["gamerule.png"]=pygame.mask.from_surface(IMAGE["gamerule.png"])

## retry button
re_b_size=(100,50)
IMAGE["re.png"]=pygame.transform.scale(IMAGE["re.png"],re_b_size)
MASK["re.png"]=pygame.mask.from_surface(IMAGE["re.png"])
re_txt_size=25


##blurred effect
blurred_effect_size=size
IMAGE['background_blurred_effect.png']=pygame.transform.scale(IMAGE['background_blurred_effect.png'],blurred_effect_size)
IMAGE['background_blurred_effect.png'].set_alpha(230)
MASK['background_blurred_effect.png']=pygame.mask.from_surface(IMAGE['background_blurred_effect.png'])

#close button
closebutton_size=(50,50)
IMAGE["closebutton.png"]=pygame.transform.scale(IMAGE["closebutton.png"],closebutton_size)
MASK["closebutton.png"]=pygame.mask.from_surface(IMAGE["closebutton.png"])
txt_size=15


class PB(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.board_pos=(size[0]/2,side_blank_space[1]) # 중앙 x 좌표, 상단 y좌표


        self.board_image_rect=IMAGE["board.png"].get_rect()
        self.board_image_rect.midtop=self.board_pos
        
        self.text_size=50
        
        self.myFont = pygame.font.SysFont('/'.join([font_path,'fonts/arial.ttc']), self.text_size, True, False) 
        self.port_myFont = pygame.font.SysFont('/'.join([font_path,'fonts/arial.ttc']), self.text_size//3, True, False) 
        self.text="5,15,□,35,45,55"
        self.port_text="a"
        self.text_pos=(self.board_pos[0],self.board_pos[1]+board_size[1]/2-4)
        #_Title= self.myFont.render("Pygame Text Test", True, color["black"])
        
        self.first_element=randint(1,5)
        self.d=randint(1,10)
        self.answer=0
        self.percent=[0,0]
        self.last_percent=[1,MAP_SIZE[0]*MAP_SIZE[1]]
        
        self.PB_category={
            #"blank",
            #"common difference",
            "nth value",

            
        }
        """
        수열 문제 유형
        1. 빈칸 o 3점
        2. 공차 구하기 o 3점
        3. n번째 항 구하기  5점      n번째 항 : an, 1번째 항 : a1
        
        지수함수
        
        로그함수
        
        삼각함수
        
        """
        
        self.pb_list=list(self.PB_category)
        
    def draw(self):
        
        SURFACE.blit(IMAGE["board.png"],self.board_image_rect)
        stack=self.text.split("\n")
        centery=(len(stack)-1)*self.text_size
        for i in range(len(stack)):
            #print(stack[i])

            TEXT = self.myFont.render(stack[i], True, color["black"])
            self.text_rect=TEXT.get_rect()
            self.text_rect.center=[self.text_pos[0],self.text_pos[1]+self.text_size*i-centery/2]
            
            
            SURFACE.blit(TEXT,self.text_rect)
        
        
    def new_pb(self):
        self.text=""
        self.first_element=randint(1,5)
        self.d=randint(1,10)
        category=self.pb_list[randint(0,len(self.pb_list)-1)]
        self.percent=[1,MAP_SIZE[0]*MAP_SIZE[1]]
        
        # problem category
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
                    
        if category=="common difference":
            number=randint(3,6)
            v=self.first_element
            
            for i in range(number):
                self.text+=str(v)
                v+=self.d
                if i+1!=number:
                    self.text+=","
                    
            self.text+="\n"+"d : □"
                    
            self.answer=self.d
            
        if category=="nth value":
            number=randint(5,10)
            self.answer=self.first_element+self.d*(number-1)
            first_pd=randint(1,3)
            second_pd=randint(first_pd+1,4)
            
            self.text=f"a{first_pd} : {self.first_element+self.d*(first_pd-1)}, a{second_pd} : {self.first_element+self.d*(second_pd-1)} \n a{number} : □"
                  
class MOLE(pygame.sprite.Sprite):
    def __init__(self,pos,text):

        pygame.sprite.Sprite.__init__(self)
        self.pos=pos

        self.mole_pos=[self.pos[0],self.pos[1]+25]
        
        self.k=5.5
        #512/5.5 에 25
        
        self.ans=text
        
        
        self.POS=[0,0]
        
        #mole
        self.mole_image_Rect=IMAGE["mole.png"].get_rect()
        self.mole_image_Rect.center=self.mole_pos
        self.mole_vo=Virtual_Object([IMAGE["mole.png"],self.mole_image_Rect,MASK['mole.png']])
        
        #hide up
        self.mole_up_image_Rect=IMAGE['hide_up.png'].get_rect()
        self.mole_up_image_Rect.midbottom = (self.pos[0],self.pos[1])

        
        #hide down
        self.mole_down_image_Rect=IMAGE['hide_down.png'].get_rect()
        self.mole_down_image_Rect.midtop = (self.pos[0],self.pos[1]-1)

        
        #hole in
        self.hole_in_image_Rect=IMAGE['hole_in.png'].get_rect()
        self.hole_in_image_Rect.center = self.pos
        
        
        #text
        
        self.myFont = pygame.font.SysFont('/'.join([font_path,'fonts/arial.ttc']), 22, True, False) # 7자리 20, 6자리 22, 5자리 25, 4자리 30  | 최대 30
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
            if self.pos[1]-self.mole_pos[1]<up_distnace:
                self.mole_pos[1]-=up_distnace/50*self.v
        if self.up==-1:
            if self.pos[1]-self.mole_pos[1]>-up_distnace:
                self.mole_pos[1]+=up_distnace/50*self.v
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
        
        SURFACE.blit(IMAGE['hole_in.png'],self.hole_in_image_Rect) # mole
        SURFACE.blit(IMAGE['hide_up.png'],self.mole_up_image_Rect) # hide up
        SURFACE.blit(IMAGE['mole.png'],self.mole_image_Rect) # mole
        SURFACE.blit(TEXT,self.text_rect) # text
        SURFACE.blit(IMAGE['hide_down.png'],self.mole_down_image_Rect) # hide down
            
class MousePointer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos=(0,0)
        
        #hammer
        self.mousepointer_Rect=IMAGE['hammer.png'].get_rect()
        self.mousepointer_vo=Virtual_Object([IMAGE['hammer.png'],self.mousepointer_Rect,MASK['hammer.png']])
        
        #hammer crash
        self.mousepointer_crash_Rect=IMAGE['hammer_crash.png'].get_rect()
        self.mousepointer_crash_vo=Virtual_Object([IMAGE['hammer_crash.png'],self.mousepointer_crash_Rect,MASK['hammer_crash.png']])
        
        self.draw_image=0 # 0 : hammer 1 : hammer crash
        self.crash_delay=0.3
        self.crash_time=0
        
    def draw(self,pos):
        if self.draw_image==0:
            self.mousepointer_Rect.center=pos
            SURFACE.blit(IMAGE['hammer.png'],self.mousepointer_Rect)
        else:
            self.mousepointer_crash_Rect.center=pos
            SURFACE.blit(IMAGE['hammer_crash.png'],self.mousepointer_crash_Rect)
        
    def crash(self):
        self.draw_image=1
        self.crash_time=time.time()
        
    def crash_stop(self):
        self.draw_image=0

class ALARM():
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        #alarm
        self.Gamerule=0
        self.Gameclear=0
        
        #game start
        self.start_Rect=IMAGE["start.png"].get_rect()
        self.start_Rect.center=(size[0]/2, side_blank_space[1]*13)
        self.start_vo=Virtual_Object([IMAGE["start.png"],self.start_Rect,MASK['start.png']])
        
        #explanation
        self.gamerule_Rect=IMAGE["gamerule.png"].get_rect()
        self.gamerule_Rect.center=(size[0]/2, side_blank_space[1]*14 + start_size[1])
        self.gamerule_vo=Virtual_Object([IMAGE["gamerule.png"],self.gamerule_Rect,MASK['gamerule.png']])
        
        #game clear
        ## retry button
        self.re_b_Rect=IMAGE["re.png"].get_rect()
        self.re_b_Rect.center=(size[0]/2, side_blank_space[1]*8)
        self.re_b_vo=Virtual_Object([IMAGE["re.png"],self.re_b_Rect,MASK['re.png']])
        
        
        
        self.re_text_font = pygame.font.SysFont('/'.join([font_path,'fonts/malgungothic.ttc']), re_txt_size, True, False)
        self.re_text=\
        """
        """
        
        ##blurred effect
        self.blurred_effect_Rect=IMAGE['background_blurred_effect.png'].get_rect()
        
        #close button
        self.closebutton_Rect=IMAGE['closebutton.png'].get_rect()
        txt_size=15
        self.closebutton_Rect.center=(size[0]-side_blank_space[0]-side_blank_space[0]/4, side_blank_space[1]*3)
        self.close_button_vo=Virtual_Object([IMAGE['closebutton.png'],self.closebutton_Rect,MASK['closebutton.png']])
        
        self.text_font = pygame.font.SysFont('malgungothic', txt_size, True, False)
        
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
        SURFACE.blit(IMAGE['re.png'],self.re_b_Rect)
        
    def start_button(self):
        SURFACE.blit(IMAGE['start.png'],self.start_Rect)
        
    def gamerule_button(self):
        SURFACE.blit(IMAGE['gamerule.png'],self.gamerule_Rect)
        
    def blurred_effect(self):
        SURFACE.blit(IMAGE['background_blurred_effect.png'],self.blurred_effect_Rect)
        
    def close_button(self):
        SURFACE.blit(IMAGE['closebutton.png'],self.closebutton_Rect)
        
    def close_button_click(self):
        self.Gamerule=0

        
    def gamerule(self):
        self.blurred_effect()
        pygame.draw.rect(SURFACE,color["whitegray"],[side_blank_space[0]/2,side_blank_space[1]*2,size[0]-side_blank_space[0],size[1]-side_blank_space[1]*4])
        self.close_button()
        stack=self.text.split("\n")
        for i in range(len(stack)):
            #print(stack[i])
            text_Title=self.text_font.render(stack[i], True, color["black"])
            Rect=text_Title.get_rect()
            Rect.midtop=(size[0]/2,side_blank_space[1]*2.5+closebutton_size[1] + txt_size*i)
            SURFACE.blit(text_Title, Rect)
    
 
    def gameclear(self,SCORE): # time 은 남은 시간
        self.blurred_effect()
        self.Gameclear=2
        pygame.draw.rect(SURFACE,color["whitegray"],[side_blank_space[0]/2,side_blank_space[1]*2,size[0]-side_blank_space[0],size[1]-side_blank_space[1]*10])
        
        self.re_text=f"Game Finished!!\nYour Score is {SCORE}"
            
        self.retry_button()
        stack=self.re_text.split("\n")
        for i in range(len(stack)):
            text_Title=self.re_text_font.render(stack[i], True, color["black"])
            Rect=text_Title.get_rect()
            Rect.midtop=(size[0]/2,side_blank_space[1]*2+re_b_size[1] + re_txt_size*i)
            SURFACE.blit(text_Title, Rect)

class interface():
    def __init__(self,time_pos):
        pygame.sprite.Sprite.__init__(self)
        

        #time
        self.playtime=0
        self.start_time=0
        self.time_pos=time_pos
        self.time_size=40
        self.time_font = pygame.font.SysFont('/'.join([font_path,'fonts/malgungothic.ttc']), self.time_size, True, False)
        self.Time=0
        
        #score
        self.score_pos=(self.time_pos[0],self.time_pos[1]+self.time_size)
        self.score_size=30
        self.score_font = pygame.font.SysFont('/'.join([font_path,'fonts/malgungothic.ttc']), self.score_size, True, False)
        
            
        
    def time_draw(self):
        self.Time=self.playtime-(time.time()-self.start_time)
        text_Title=self.time_font.render(f"{int(self.Time//60)} : {round(self.Time%60,1)}", True, color["black"])
        Rect=text_Title.get_rect()
        Rect.x=self.time_pos[0]
        Rect.y=self.time_pos[1]
        SURFACE.blit(text_Title, Rect)
        
    def score_draw(self,score):
        text_Title=self.score_font.render(f"score : {score}", True, color["black"])
        Rect=text_Title.get_rect()
        Rect.x=self.score_pos[0]
        Rect.y=self.score_pos[1]
        SURFACE.blit(text_Title, Rect)
    
    def game_start(self):
        self.start_time=time.time()
        self.playtime=60

def new_mole(pos,p,ans):
    RD=randint(1,p[1]+1)
    if RD<=p[0]:
        #answer
        MAP[pos[1]][pos[0]]=MOLE([tile_left_up_pos[0]+mole_box_size[0]*pos[0]+mole_box_size[0]/2,
                                tile_left_up_pos[1]+mole_box_size[1]*pos[1]+mole_box_size[1]/2],ans)
        MAP[pos[1]][pos[0]].POS=pos
    
        return 1
    else:
        #not answer
        if randint(1,2)==1:
            wrong_ans=randint(ans-10,ans-1)
        else:
            wrong_ans=randint(ans+1,ans+10)
            
        MAP[pos[1]][pos[0]]=MOLE([tile_left_up_pos[0]+mole_box_size[0]*pos[0]+mole_box_size[0]/2,
                                tile_left_up_pos[1]+mole_box_size[1]*pos[1]+mole_box_size[1]/2],wrong_ans)
        MAP[pos[1]][pos[0]].POS=pos

        return 0

def GAMESTART():
    global MAP,mousepointer,alarm,INTERFACE,tile_left_up_pos,PROBLEM
    
    alarm.Gameclear=0

    
    tile_left_up_pos=[center[0]-(MAP_SIZE[0]/2)*mole_box_size[0],PROBLEM.board_pos[1]+board_size[1]+side_blank_space[1]/2]
    
    PROBLEM.new_pb()
    SCORE=0

    MAP=[[0 for i in range(MAP_SIZE[0])]for g in range(MAP_SIZE[1])]
        
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

                        if mousepointer.draw_image==0:
                            A=mousepointer.mousepointer_vo
                        else:
                            A=mousepointer.mousepointer_crash_vo
                            
                        A.rect.center=pygame.mouse.get_pos()
                        
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
                        
                            if mousepointer.draw_image==0:
                                A=mousepointer.mousepointer_vo
                            else:
                                A=mousepointer.mousepointer_crash_vo
                                
                            A.rect.center=pygame.mouse.get_pos()
                            B=MAP[mouse_pos_idx[1]][mouse_pos_idx[0]].mole_vo
                            B.rect.center=MAP[mouse_pos_idx[1]][mouse_pos_idx[0]].mole_pos
                            
                            """print((MAP[mouse_pos_idx[1]][mouse_pos_idx[0]].mole_image_Rect.centerx,
                                MAP[mouse_pos_idx[1]][mouse_pos_idx[0]].mole_image_Rect.centery),
                                mouse_pos)"""
                            
                            if pygame.sprite.collide_mask(A,B):
                                if mousepointer.draw_image==0:
                                    if MAP[mouse_pos_idx[1]][mouse_pos_idx[0]].up!=0:
                                        #print("!!!!")
                                        if PROBLEM.answer==MAP[mouse_pos_idx[1]][mouse_pos_idx[0]].ans:
                                            #print("-"*30)
                                            PROBLEM.new_pb()
                                            
                                            PROBLEM.percent=[1,MAP_SIZE[0]*MAP_SIZE[1]]
                                            PROBLEM.last_percent=[1,MAP_SIZE[0]*MAP_SIZE[1]]
                                            for i in range(MAP_SIZE[1]):
                                                for g in range(MAP_SIZE[0]):
                                                    if i==mouse_pos_idx[1] and g==mouse_pos_idx[0]:continue
                                                    if PROBLEM.answer==MAP[i][g].ans:
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
                        if MAP[i][g].ans==PROBLEM.answer:
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
    
K=size[0]/IMAGE["background.png"].get_width()
background_image_size=[IMAGE["background.png"].get_width()*K,IMAGE["background.png"].get_height()*K]
IMAGE["background.png"]=pygame.transform.scale(IMAGE["background.png"],background_image_size)
background_image_rect=IMAGE["background.png"].get_rect()
background_image_rect.topleft=(0,0)
    
PROBLEM=PB()
mousepointer=MousePointer()
alarm=ALARM()
tile_left_up_pos=[center[0]-(MAP_SIZE[0]/2)*mole_box_size[0],]
INTERFACE=interface([side_blank_space[0],PROBLEM.board_pos[1]+board_size[1]+side_blank_space[1]+mole_box_size[1]*MAP_SIZE[1]])

def GAME_LOBY():
    global SURFACE,alarm,mousepointer,INTERFACE 
    while 1:
        #print(pygame.time.Clock())
        SURFACE.fill(color["black"])
        SURFACE.blit(IMAGE["background.png"],background_image_rect)
        for EVENT in pygame.event.get():
            if EVENT.type==QUIT:pygame.quit();sys.exit()
                
            if EVENT.type==MOUSEBUTTONDOWN:
            
                if alarm.Gamerule==1:
                    if pygame.mouse.get_pressed()[0]:

                        if mousepointer.draw_image==0:
                            A=mousepointer.mousepointer_vo
                        else:
                            A=mousepointer.mousepointer_crash_vo
                            
                        A.rect.center=pygame.mouse.get_pos()
                        
                        if pygame.sprite.collide_mask(A,alarm.close_button_vo):
                            alarm.Gamerule=0
                
                if pygame.mouse.get_pressed()[0]:

                    if mousepointer.draw_image==0:
                        A=mousepointer.mousepointer_vo
                    else:
                        A=mousepointer.mousepointer_crash_vo
                        
                    A.rect.center=pygame.mouse.get_pos()
                    
                    
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
        
        
if __name__ == '__main__':
    GAME_LOBY()