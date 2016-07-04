# Import some necessary libraries.
import socket
import random
import pygame
import time

pygame.init()
screen = pygame.display.set_mode((1024,768),pygame.RESIZABLE)
pygame.display.set_caption('Map War 3') # Window title
screen = pygame.display.get_surface() # Setting up the screen
screen_id = 0 # Enables us to have an intro screen.
intro = pygame.image.load("menuPic.png").convert() # Intro screen image.
clock = pygame.time.Clock()
tpsMax = 30 # Max tps

# Color definitions
white = (255,255,255)
gray = (128,128,128)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)
green = (0,255,0)
cyan = (0,255,255)
blue = (0,0,255)
magenta = (255,0,255)
playerColors = [white,red,yellow,green,cyan,blue,magenta]

# Font definitions
xyfont = pygame.font.SysFont("century", 20,20) # Font of coordinate display
buttonFont = pygame.font.SysFont("verdana", 20,20) # Font for buttons

class squareZoneObj:
    def __init__(self,x,y):
        self.owner = 0 # 0: Empty, 1: Player, 2+: AIs
        self.x = x
        self.y = y

class player:
    def __init__(self,owner):
        self.owner = owner
        self.zones = 0
        self.resources = 5
        self.production = 0
        self.techrate = 0.05
        self.technology = 0
        self.trade = 0
        self.overspent = 0
        self.color = (0,255,255)

def textObjects(text, font, color): # Text object function for e.g. button text
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None): # Button function: Message, position (x,y), width, height, inactive color, highlight color, action
    mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
    mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
    if x+w > mousePos[0] > x and y+h > mousePos[1] > y: # Mouse is over button
        pygame.draw.rect(screen,ac,(x,y,w,h))
        pygame.draw.rect(screen,black,(x+5,y+5,w-10,h-10))
        textSurf, textRect = textObjects(msg,buttonFont,ac) # Button text
        if mouseClick[0] ==  1:
            print("button clicked, function!!!")
        if mouseClick[0] ==  1 and action != None:
            print("button clicked, function, action!!!")
            if action == "setUpGame":
                print("Action!!!")
                return 1
            if action == "startGame":
                print("Action!!!")
                return 1
            if action == "endTurn":
                print("ending turn!!")
                return 1
            elif action == "quit":
                pygame.quit()
                quit()
    else: # Mouse is not over button
        pygame.draw.rect(screen,ic,(x,y,w,h))
        pygame.draw.rect(screen,black,(x+5,y+5,w-10,h-10))
        textSurf, textRect = textObjects(msg,buttonFont,ic) # Button text
    textRect.center = (x+w/2,y+h/2) # Center point of button
    screen.blit(textSurf, textRect) # Render button text

def squareZone(msg,x,y,w,h,ic,ac,fc,action=None): # Square zone function: Message, position (x,y), width, height, inactive color, highlight color, fill color, action
    mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
    mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
    if x+w > mousePos[0] > x and y+h > mousePos[1] > y: # Mouse is over button
        pygame.draw.rect(screen,ac,(x,y,w,h))
        pygame.draw.rect(screen,fc,(x+5,y+5,w-10,h-10))
        textSurf, textRect = textObjects(msg,buttonFont,ac) # Button text
        if mouseClick[0] ==  1:
            print("button clicked, function!!!")
        if mouseClick[0] ==  1 and action != None:
            print("button clicked, function, action!!!")
            if action == "claim":
                print("claimed!!!")
                return 1
    else: # Mouse is not over button
        pygame.draw.rect(screen,ic,(x,y,w,h))
        pygame.draw.rect(screen,fc,(x+5,y+5,w-10,h-10))
        textSurf, textRect = textObjects(msg,buttonFont,ic) # Button text
    textRect.center = (x+w/2,y+h/2) # Center point of button
    screen.blit(textSurf, textRect) # Render button text

# Putting the initial screen up
screen.blit(intro, (0, 0))
mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
pygame.display.flip()
while(screen_id == 0): # Initial screen
    pressed = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
    mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
    if button("Set up game!",25,693,200,50,red,green,"setUpGame") == 1: # Start button
        screen_id = 1
        print screen_id
    if button("Quit",250,693,200,50,red,green,"quit") == 1: # Quit button
        pygame.quit()
        quit()
    
    if (pygame.key.get_pressed()[pygame.K_t]):
        print "t!" # Print t if the user types t on keyboard. Test.
    
    alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
    ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
    
    for event in pygame.event.get(): # Keyboard/mouse event queue
        if event.type == pygame.KEYDOWN:
        
            # determine if a letter key was pressed 
            if event.key == pygame.K_r:
                print "r!"
            elif event.key == pygame.K_g:
                print "g!"
            elif event.key == pygame.K_b:
                print "b!"
				
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                print "lmb!"
            elif event.button == 3: # Right mouse button
                print "rmb!"
        
        if event.type == pygame.MOUSEMOTION:
            # if mouse moved, add point to list 
			#very messy hack to display coordinates at to left corner, fix later
			#works by displaying the coordinates, then adding another intro picture, repeat, etc.
            #screen.blit(intro, (0,0))
            #mouseposDisp = xyfont.render(str(pygame.mouse.get_pos()[0])+", "+str(pygame.mouse.get_pos()[1]), 0, (255,255,0))
            #screen.blit(mouseposDisp, (0, 0))
            #print "Moved!"
            pass
			
    #screen.fill((0, 0, 0)) # Black screen
    pygame.display.flip()
    #pygame.display.update()
    clock.tick(tpsMax) # Max ticks per second
	
intro2  = pygame.image.load("2ndscreen.png").convert()
screen.blit(intro2, (0,0))
pygame.display.flip()
time.sleep(0.5)
for event in pygame.event.get(): pass # Keyboard/mouse event queue

while (screen_id == 1):
    pressed = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
    mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
    if button("Start game!",25,693,200,50,red,green,"startGame") == 1: # Start game button
        screen_id = 2
        print screen_id
    if button("Quit",250,693,200,50,red,green,"quit") == 1: # Quit button
        pygame.quit()
        quit()

    for event in pygame.event.get(): # Keyboard/mouse event queue
        pass # This loop is apparently necessary to make the quit button work.
        
    pygame.display.flip()
    clock.tick(tpsMax) # Max ticks per second

screen.fill((0, 0, 0)) # Black screen
#intro3  = pygame.image.load("2ndscreen.png").convert()
#screen.blit(intro3, (0,0))
pygame.display.flip()
pressedEnter = 0
Round = 0 # Round variable
Turn = 1 # Turn variable
xMap = 8 # Map width in zones
yMap = 6 # Map height in zones
totZones = xMap*yMap # Total number of zones on map
nPlayers = 5 # Number of players
Players = [] # Generate player objects
print("Generating player objects")
for nPlayer in range(0,nPlayers+1):
    currPlayer = player(nPlayer)
    Players.append(currPlayer)
    Players[nPlayer].color = playerColors[nPlayer]
    print(Players[nPlayer].owner)
    print(Players[nPlayer].color)
print("Generating zone objects")
Zones = [] # Generate zone objects    
for xZone in range(0,xMap):
    for yZone in range(0,yMap):
        currZone = squareZoneObj(xZone,yZone)
        Zones.append(currZone)
        print(Zones[xZone*yMap+yZone].x)
        print(Zones[xZone*yMap+yZone].y)
        print(Zones[xZone*yMap+yZone].owner)
time.sleep(0.5)
for event in pygame.event.get(): pass # Keyboard/mouse event queue

while (screen_id == 2):
    pressed = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
    mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
    pygame.draw.rect(screen,gray,(25,25,80*xMap+10,80*yMap+10))
    for xZone in range(0,xMap): # Make zone "button"
        for yZone in range(0,yMap):
            if Zones[xZone*yMap+yZone].owner == 0: # If the zone is not owned by the player
                if squareZone("",30+xZone*80,30+yZone*80,80,80,gray,Players[1].color,white,"claim") == 1: # If the zone is clicked
                    if Players[1].resources >= 5:
                        print("The zone has been claimed!")
                        Zones[xZone*yMap+yZone].owner = 1 # Update the owner of the zone object
                        Players[1].zones = Players[1].zones + 1 # Update player's zone stat
                        Players[1].resources = Players[1].resources - 5 # Update player's resource stat
                    else:
                        print("You do not have enough resources to claim the zone!")
            elif Zones[xZone*yMap+yZone].owner == 1: # If the zone is owned by the player
                if squareZone("",30+xZone*80,30+yZone*80,80,80,gray,Players[1].color,Players[1].color,"claim") == 1: # If the zone is clicked
                    print("The zone is already yours!")
    
    if button("Quit",250,693,200,50,red,green,"quit") == 1: # Quit button
        pygame.quit()
        quit()
    if button("End Turn",25,693,200,50,red,green,"endTurn") == 1 or pressedEnter == 1: # End turn button
        pressedEnter = 0
        print("Turn 1 has ended.")
        for Turn in range(2,nPlayers+1): # AI players take their turns here.
            print("Turn:")
            print(Turn)
            time.sleep(0.5)
        for nPlayer in range(0,nPlayers+1): # After all turns are taken, update stats.
            Players[nPlayer].production = Players[nPlayer].zones  # Update player's production stat
            Players[nPlayer].resources = int(round(5 + Players[nPlayer].production + (Players[nPlayer].technology+Players[nPlayer].trade)/10 + Players[nPlayer].resources - pow(Players[nPlayer].resources,2)/1000 - Players[nPlayer].overspent/5)) # Update player's resource stat
            spentOnTech = int(round(Players[nPlayer].techrate*Players[nPlayer].resources)) # Amount spent on tech this round by the player
            Players[nPlayer].technology = Players[nPlayer].technology + spentOnTech # Update player's technology stat
            Players[nPlayer].resources = Players[nPlayer].resources - spentOnTech # Update the player's resource stat
        Round = Round + 1
        print("Round:")
        print(Round)
        print("Player 1 zones:")
        print(Players[1].zones)
        print("Player 1 production:")
        print(Players[1].production)
        print("Player 1 technology:")
        print(Players[1].technology)
        print("Player 1 resources:")
        print(Players[1].resources)
        if Players[1].zones == totZones: # If the player has all the zones on the map
            print("You won!")
            screen_id = 3

    for event in pygame.event.get(): # Keyboard/mouse event queue. This loop is apparently necessary to make the quit button work.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: # Pressing enter acts like clicking the end turn button
                print "Enter!"
                pressedEnter = 1
                
    pygame.display.flip()
    clock.tick(tpsMax) # Max ticks per second

screen.fill((0, 0, 0)) # Black screen
intro4  = pygame.image.load("sebcastro.png").convert()
screen.blit(intro4, (0,0))
pygame.display.flip()
time.sleep(0.5)
for event in pygame.event.get(): pass # Keyboard/mouse event queue

while (screen_id == 3):
    pressed = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
    mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
    if button("Quit",250,693,200,50,red,green,"quit") == 1: # Quit button
        pygame.quit()
        quit()

    for event in pygame.event.get(): # Keyboard/mouse event queue
        pass # This loop is apparently necessary to make the quit button work.
        
    pygame.display.flip()
    clock.tick(tpsMax) # Max ticks per second
