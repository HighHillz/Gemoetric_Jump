#1. Import requiered libraries
import pygame
from pygame.locals import *
import sys
import math
import random

pygame.init() #Initialize pygame modules

#2. Drawing sprites
class Rectangle(pygame.sprite.Sprite) :
    def __init__(self, colour, width, height) :
        super().__init__()
        self.surf = pygame.Surface((width,height)) #Create object
        self.surf.fill(colour) #Add colour
        self.rect = self.surf.get_rect() #Return rectangle

#3. Create screen
screen = pygame.display.set_mode((800,500)) #Create screen .i.e. window
background = pygame.image.load("project 11bg.jpg").convert()
background = pygame.transform.scale(background, (800,500))
screen.blit(background, (0,0))

pygame.display.set_caption("Ninjump") #Window title

#4. Draw objects
width = 50 #Used to draw and position our objects

#Draw box
x, y = 50, screen.get_size()[1]-60 #Position of player (box)

box = Rectangle((0,0,0), width, width) #Create box
screen.blit(box.surf, (x, y)) #Draw box on the screen

#Draw borders
wall = pygame.image.load("walls.jpg").convert() #Create buildings (walls)
wall = pygame.transform.scale(wall, (50,500))
walls_y = 0 #Y position of wall
screen.blit(wall, (0,walls_y))
screen.blit(wall, (screen.get_size()[0]-50,walls_y))

#Draw bridge
bridge = pygame.image.load("Rope.png").convert_alpha()
bridge = pygame.transform.scale(bridge, (screen.get_size()[0], 100))

#Draw data panel
panel = Rectangle((0,0,0), screen.get_size()[0], 60)
screen.blit(panel.surf, (0,0))

pygame.display.flip() #Update window

#5. Powerups
#Temporary Evolution
evo_count = 0
collected_evo = False #Check whether powerup count has increased
evo_active = False #If powerup is active (For nothing to work while evolve)
evo_spawn = random.choice([True, False]) #Choose whether to spawn powerup or not

evo_dim = [25,25]
evo = pygame.image.load("collection.png").convert_alpha()
evo = pygame.transform.scale(evo, (30,30))
evo_pos = [random.randint(50,screen.get_size()[1]-50),0] #Position of powerup - bridge

#6. Obstacles - Spikes
spike_dim = [100,30]
spike_pos = [50,0]
spike_vis = False
spike = pygame.image.load("spike.png").convert_alpha()
spike = pygame.transform.scale(spike, (100,50))

#7. Write data
#Score
score = 0
font_score = pygame.font.Font("freesansbold.ttf", 32) #Load a font from pygame
text_score = font_score.render(str(int(score)), True, (255,255,255))
textRectScore = text_score.get_rect() #Get it as a rectangle so it would be easy to position it
textRectScore.center = (15, 20) #Centre position of text
screen.blit(text_score, textRectScore)

#8. Gameplay
#Player
right = True
evo_right = random.choice([True, False])

#Components of a parabola
#Formula: R = 2*u*sin(theta)*u*cos(theta) / g
gravity = 0.003 #g
init_velocity = 1 #u
angle = math.pi/6 #theta
y_velocity = init_velocity * math.sin(angle) #u*sin(theta)
x_velocity = ((screen.get_size()[0]-2*width - width)*gravity) / (2*y_velocity) #u*cos(theta) = R*g / 2*u*sin(theta)

#Other components
bridge_stat = [False, 0, .5] #Visibility, Y position, Y increment

gameState = "Start"

#Start message
font_size = 45
start_text = pygame.font.Font("freesansbold.ttf", font_size) #Load a font from pygame
start_text = start_text.render("Press space to start!", True, (30,30,30))
startRect = start_text.get_rect()
startRect.center = (screen.get_size()[0]/2, 145)
screen.blit(start_text, startRect)

#Processing
while True :
    
    for event in pygame.event.get() : #Go through every type of event that exists
        if event.type == KEYDOWN :
            
            if x >= screen.get_size()[0]-2*width or x <= width : #If box is climbing the wall
                
                if event.key == K_SPACE :
                    if gameState == "Start" or gameState == "Play": #Initiate game only when score is 0
                        right = not right #Switch between True and False so that the box jumps from one wall to the other
                        gameState = "Play" #Spacebar initiates the game
                        y_velocity = .5
                    else :
                        #Reset Stats
                        gameState = "Start"
                        walls_y = score = evo_count = bridge_stat[1] = spike_pos[1] = evo_pos[1] = 0
                        spike_vis = bridge_stat[0] = False
                        right = True
                        x, y = 50, screen.get_size()[1]-60
                        spike_dim = [100,30]
                        
                        text_score = font_score.render(str(int(score)), True, (255,255,255)) #Update score

                        #Erase whatever is on the screen
                        screen.blit(background, (0,0))
                        screen.blit(wall, (0,walls_y))
                        screen.blit(wall, (screen.get_size()[0]-50,walls_y))
                        screen.blit(box.surf, (x, y))
                        screen.blit(panel.surf, (0,0))
                        screen.blit(text_score, textRectScore)
                                        
        elif event.type == QUIT : #If event type is quit, then close the program
            pygame.quit()
            sys.exit()

    if gameState == "Play" : #If the passed gamestate variable says that the game started...
        if right : #Jumping of box to either sides
            x += x_velocity
        else :
            x -= x_velocity
            
        if x <= 50 or x >= screen.get_size()[0]-100 : #Make the box stick to the wall
            if x <= 50 :  #Check wall position
                x = 50
            else :
                x = (screen.get_size()[0]-100)
            
            if y < screen.get_size()[1]-60 : #Move box down until it reaches it's original position
                y += 1
            else :
                evo_active = False
            
            box = Rectangle((0,0,0), width, width) #Change object type

            #Reset box speed properties
            angle = math.pi/6 
            y_velocity = init_velocity * math.sin(angle)
            x_velocity = ((screen.get_size()[0]-2*width - width)*gravity) / (2*y_velocity)
        else :
            if not evo_active : #If box is not under the effect of powerup
                y -= y_velocity
                y_velocity -= gravity #Gravitational force is acting on the box
                
                if y > screen.get_size()[1] : #Activate powerup
                    evo_active = True

                    #Make the box shoot upwards
                    angle = (math.pi/4) #pi/4 rad = 45 deg
                    y_velocity = 3 * math.sin(angle)
                    x_velocity = ((screen.get_size()[0]-2*width - width)*gravity) / (2*y_velocity)
                    box = pygame.image.load("powerup.png").convert_alpha()
                    box = pygame.transform.scale(box, (75,75))

                if y < 0 :
                    evo_active = False
                    box = Rectangle((0,0,0), width, width)
            else :
                y -= y_velocity
                y_velocity -= gravity

        if not evo_active :
            score += .04 #Increase score
        else :
            score += .6 #If powerup is active, score increases by 15 times the usual amount
        
        text_score = font_score.render(str(int(score)), True, (255,255,255)) #Update score

        if bridge_stat[1] > screen.get_size()[1] :
            evo_spawn = random.choice([True, False]) #Choose whether to spawn powerup or not
            bridge_stat[1] = 0
            evo_pos[0], evo_pos[1] = random.randint(50,screen.get_size()[1]-50), 0 #Reset position for a new bridge and powerup to spawn
            bridge_stat[0] = False #Old bridge is not visible
            collected_evo = False #So that a new powerup can be collected_evo
            evo_right = random.choice([True, False]) #Randomise direction of new powerup

        if spike_pos[1] > screen.get_size()[1] : #If spike goes out of screen
            spike_pos[1] = 0
            spike_pos[0] = random.choice([50,screen.get_size()[0]-150])
            spike_vis = False

        #Powerup collision
        if (not collected_evo) and ((evo_pos[0] >= x and evo_pos[0] <= (x+width) and evo_pos[1] >= y and evo_pos[1] <= (y+width)) or \
           (evo_pos[0]+evo_dim[0] >= x and evo_pos[0]+evo_dim[0] <= (x+width)) and (evo_pos[1]+evo_dim[1] >= y and \
                                                                                    evo_pos[1]+evo_dim[1] <= (y+width))):
            evo_count += 1
            collected_evo = True #Prevent multiple collecting

            if evo_count == 3 :
                evo_count = 0
                x_velocity = 0
                
        #Update board
        screen.blit(background, (0,0))

        #Working of score ball
        if (int(score) > 0 and int(score)%100 == 0 or bridge_stat[0]) and (not evo_active) : #If score has crossed an interval of 100 a bridge is visible
            bridge_stat[0] = True #Keep bridge visibility true if it is false so as to keep it on screen
            screen.blit(bridge, (0,bridge_stat[1]))
            
            if not collected_evo and evo_spawn : #Display powerup only if it is not collected
                screen.blit(evo, (evo_pos[0],evo_pos[1]))
                evo_pos[1] = bridge_stat[1] - 25 #Place powerup over the bridge
            
            bridge_stat[1] += bridge_stat[2] #Change position of rod

            if evo_pos[0] >= screen.get_size()[0]-50 : #Make the powerup bounce back
                evo_pos[0] = (screen.get_size()[0]-50.25)
                evo_right = False
            elif evo_pos[0] <= 30 :
                evo_pos[0] = 30.2
                evo_right = True
            else :
                if evo_right :
                    evo_pos[0] += 0.25
                else :
                    evo_pos[0] -= 0.25

        #Obstacle spawn and collision detection
        if (int(score) > 0 and int(score)%30 == 0 or spike_vis) and (not evo_active):
            screen.blit(spike, (spike_pos[0],spike_pos[1]))
                            
            spike_pos[1] += bridge_stat[2]
            spike_vis = True #Say that spike is present on screen

            #Collision
            if ((spike_pos[0] <= x and spike_pos[0]+spike_dim[0] >= x and spike_pos[1] <= y and spike_pos[1]+spike_dim[1] >= y) or #Single
               (spike_pos[0] <= x+width and spike_pos[0]+spike_dim[0] >= x+width and spike_pos[1] <= y and spike_pos[1]+spike_dim[1] >= y) or 
               (spike_pos[0] <= x and spike_pos[0]+spike_dim[0] >= x and spike_pos[1] <= y+width and spike_pos[1]+spike_dim[1] >= y+width) or 
               (spike_pos[0] <= x+width and spike_pos[0]+spike_dim[0] >= x+width and spike_pos[1] <= y+width and spike_pos[1]+spike_dim[1] >= y+width)):
                gameState = "Reset" #Stop running the program if box touches the spike
                
        #Movement of walls
        if evo_active :
            walls_y += bridge_stat[2] * 10 #Because score increments 10 times faster
        else :
            walls_y += bridge_stat[2] #Move wall by the same amount as a bridge
        
        if walls_y >= 500 :
            walls_y = 0
            
        #Update game components
        if walls_y > 0 : #Spawn a new wall frame
            screen.blit(wall, (0, walls_y-500))
            screen.blit(wall, (screen.get_size()[0]-50, walls_y-500))
        screen.blit(wall, (0,walls_y))
        screen.blit(wall, (screen.get_size()[0]-50,walls_y))
        
        if evo_active and (x > 50 and x < screen.get_size()[0]-100) :
            screen.blit(box, (x, y))
        else :
            screen.blit(box.surf, (x, y))
            
        screen.blit(panel.surf, (0,0))
        screen.blit(text_score, textRectScore)
        for m in range(evo_count) :
            screen.blit(evo, (screen.get_size()[0]-(m*40+40), 20))
    
    pygame.display.flip() #Update window
