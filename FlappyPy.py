#FlappyPy
#Gavriel Feuer
#3/5/14
#--------------------Notes--------------------------------------------------------
#My version of the popular flappy bird game
#--------Import Libraries-------------------------------------------------------
import pygame, random
#-------------Color Pallet------------------------
black = (0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)

#-------------Initializations-----------------------
pygame.init()
screensize_x=500
screensize_y=600
screensize=[screensize_x,screensize_y]
screen_color=black
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption("FlappyPy")
font = pygame.font.SysFont("Arial", 36)
background = pygame.Surface(screen.get_size())
clock=pygame.time.Clock()
bird_width=10
bird_height=10
gap=200
wallpoint=0
#--------------Player Sprite-------------------
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):        
        pygame.sprite.Sprite.__init__(self)
        self.width=bird_width
        self.height=bird_height
        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(white)        
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.speed_x=0
        self.speed_y=10        
    def move(self):
        self.rect.y+=self.speed_y
        self.speed_y+=1
    def collide(self):
        if self.rect.y<0:
            self.rect.y=0
        if self.rect.y>screensize_y-self.height:
            self.rect.y=screensize_y-self.height
    def gameover(self):
        if self.rect.y<0 or self.rect.y>screensize_y-self.height:
            return True
        else:
            return False
#-------------wall Sprite--------------------------
class upperWall(pygame.sprite.Sprite):
    def __init__(self,x,y,h):
        pygame.sprite.Sprite.__init__(self)
        self.width=60
        self.height=h
        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(white)
        self.rect=self.image.get_rect()        
        self.rect.x=x
        self.rect.y=y
    def move(self):
        self.speed_x=-5
        self.rect.x+=self.speed_x

class lowerWall(pygame.sprite.Sprite):
    def __init__(self,x,y,h):
        pygame.sprite.Sprite.__init__(self)
        self.width=60
        self.height=h
        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(white)
        self.rect=self.image.get_rect()        
        self.rect.x=x
        self.rect.y=y

    def move(self):
        self.speed_x=-5
        self.rect.x+=self.speed_x
def addwall(x):
    wall_upper=upperWall(x,0,random.randint(0,screensize_y-gap))
    wall_lower=lowerWall(x,wall_upper.height+gap,screensize_y-wall_upper.height-gap)

    return wall_upper, wall_lower

#------------Sprite initialization----------------
number_of_walls=2
wallspacing=(screensize_x+60)/number_of_walls
[wall_upper1, wall_lower1]=addwall(screensize_x) #
[wall_upper2, wall_lower2]=addwall(screensize_x+wallspacing)
wallgroup=pygame.sprite.Group()
wallgroup.add(wall_upper1,wall_lower1,wall_upper2,wall_lower2)


bird=Player(100,100)
birdgroup = pygame.sprite.Group()
birdgroup.add(bird)
#-----------Game Initialization------------------
rungame=True
gameover=False
#-----------Main Program Loop---------------------
while rungame:
    screen.fill(screen_color)
    #----------Events-----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rungame=False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                bird.speed_y=-10

            if event.key == pygame.K_SPACE:
                gameover=False
                bird.rect.y=screensize_y/2
                wall_upper1.rect.x=screensize_x
                wall_lower1.rect.x=screensize_x
                wall_upper2.rect.x=screensize_x+wallspacing
                wall_lower2.rect.x=screensize_x+wallspacing

            if event.key == pygame.K_g:
                screen_color=green
    #---------Game Logic-----------------------------
    if not gameover:            
        bird.move()
        bird.collide()
        gameover=bird.gameover()

        for wall in wallgroup:
            wall.move()

        for wall in wallgroup:
            if wall.rect.x<-60:
                wall.rect.x=screensize_x
        
    if gameover:
        text=font.render("Game Over: Press Space",True,white)
        text_position=text.get_rect(centerx=background.get_width()/2)
        text_position.top=250
        screen.blit(text,text_position)          
    if pygame.sprite.spritecollide(bird,wallgroup,False):
        gameover=True

    #------------Update Drawings-------------------------
    birdgroup.draw(screen)
    wallgroup.draw(screen)
    pygame.display.flip()
    clock.tick(40)

pygame.quit()        


