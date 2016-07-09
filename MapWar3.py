# Import some necessary libraries.
import socket
import random
import pygame
import time
from operator import attrgetter

pygame.init()
screen = pygame.display.set_mode((1024,768),pygame.RESIZABLE)
pygame.display.set_caption('Map War 3') # Window title
screen = pygame.display.get_surface() # Setting up the screen
clock = pygame.time.Clock()
tpsMax = 30 # Max tps

# Color definitions
white = (255,255,255)
gray = (128,128,128)
black = (0,0,0)
red = (255,0,0)
orange = (255,128,0)
yellow = (255,255,0)
green = (0,255,0)
cyan = (0,255,255)
brightblue = (0,128,255)
blue = (0,0,255)
purple = (128,0,255)
magenta = (255,0,255)
pink = (255,128,192)
darkred = (128,0,0)
brown = (128,64,0)
spring = (192,255,64)
darkgreen = (0,128,0)
darkcyan = (0,128,96)
darkpurple = (96,0,128)
plum = (128,0,64)
playerColors = [white,pink,red,orange,yellow,green,cyan,brightblue,blue,purple,magenta,darkred,brown,spring,darkgreen,darkcyan,darkpurple,plum]
nationNames = ["Unclaimed","Kolsebistan","Blaist Blaland","Darvincia","Ethanthova","Auspikitan","Solea","Aeridani","Bielosia","Lyintaria","Czallisto","Bongatar","Dotruga","Aahrus","Kaeshar","Kaktoland","Quontia","Ampluterra"]
rulerNames = ["Missingno","Seb Castro","Bla","Kalassak","Darvince","Matthias","Fiah","vh","Blotz","Tuto","Yqt","Naru","TheMooCows","Jorster","Quontex","Mikkel Sikkel","Stowaway","Mudkipz"]

# Font definitions
xyfont = pygame.font.SysFont("century", 20,20) # Font of coordinate display
buttonFont = pygame.font.SysFont("verdana", 20,20) # Font for buttons
buttonFontSmall = pygame.font.SysFont("verdana", 12,12) # Small font for buttons

class squareZoneObj:
    def __init__(self,x,y):
        self.owner = 0 # 0: Empty, 1: Player, 2+: AIs
        self.x = x
        self.y = y

    def isAdjacent(self,Zones,own,xMap,yMap):
        claimTheZone = False
        for pxZone in range(0,xMap):
            for pyZone in range (0,yMap):
                if Zones[pxZone*yMap+pyZone].owner == own:
                    if self.x == Zones[pxZone*yMap+pyZone].x and self.y == Zones[pxZone*yMap+pyZone].y: # If the two zones checked are the same, return they are not adjacent
                        claimTheZone = False
                    elif self.x == Zones[pxZone*yMap+pyZone].x or self.y == Zones[pxZone*yMap+pyZone].y: # If the zones have either identical x or y coords
                        if abs(self.y - Zones[pxZone*yMap+pyZone].y) <= 1 and abs(self.x - Zones[pxZone*yMap+pyZone].x) <= 1:
                            claimTheZone = True
                        elif self.x == 0 and Zones[pxZone*yMap+pyZone].x == xMap-1 and abs(self.y - Zones[pxZone*yMap+pyZone].y) <= 1:
                            claimTheZone = True
                        elif self.x == xMap-1 and Zones[pxZone*yMap+pyZone].x == 0 and abs(self.y - Zones[pxZone*yMap+pyZone].y) <= 1:
                            claimTheZone = True
        if claimTheZone == True:
            return True

class player:
    def __init__(self,owner):
        self.owner = owner
        self.zones = long(0)
        self.resources = long(5)
        self.production = long(0)
        self.techrate = 0.05
        self.technology = long(0)
        self.spentOnTech = long(0)
        self.trade = long(0)
        self.overspent = long(0)
        self.color = (0,255,255)
        self.dead = False
        self.deathAnnounced = False
        self.nationName = "Kolsebistan"
        self.rulerName = "Sebastian Castro"

def textObjects(text, font, color): # Text object function for e.g. button text
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,font=buttonFont,frame=5,action=None,fillColor=black): # Button function: Message, position (x,y), width, height, inactive color, highlight color, font, frame width, action, fill color
    mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
    mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
    if x+w > mousePos[0] > x and y+h > mousePos[1] > y: # Mouse is over button
        pygame.draw.rect(screen,ac,(x,y,w,h))
        pygame.draw.rect(screen,fillColor,(x+frame,y+frame,w-2*frame,h-2*frame))
        textSurf, textRect = textObjects(msg,font,ac) # Button text
        if mouseClick[0] ==  1:
            pass
            #print("button clicked, function!!!")
        if mouseClick[0] ==  1 and action != None:
            #print("button clicked, function, action!!!")
            if action == "lmb": # Left mouse button
                return 1
            if action == "rmb": # Right mouse button
                return 2
    else: # Mouse is not over button
        pygame.draw.rect(screen,ic,(x,y,w,h))
        pygame.draw.rect(screen,fillColor,(x+frame,y+frame,w-2*frame,h-2*frame))
        textSurf, textRect = textObjects(msg,font,ic) # Button text
    textRect.center = (x+w/2,y+h/2) # Center point of button
    screen.blit(textSurf, textRect) # Render button text

def squareZone(msg,x,y,w,h,ic,ac,fc,action=None): # Square zone function: Message, position (x,y), width, height, inactive color, highlight color, fill color, action
    mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
    mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
    if x+w > mousePos[0] > x and y+h > mousePos[1] > y: # Mouse is over button
        pygame.draw.rect(screen,ac,(x,y,w,h))
        pygame.draw.rect(screen,fc,(x+2,y+2,w-4,h-4))
        textSurf, textRect = textObjects(msg,buttonFont,ac) # Button text
        if mouseClick[0] ==  1:
            pass
            #print("button clicked, function!!!")
        if mouseClick[0] ==  1 and action != None:
            #print("button clicked, function, action!!!")
            if action == "claim":
                #print("claimed!!!")
                return 1
    else: # Mouse is not over button
        pygame.draw.rect(screen,ic,(x,y,w,h))
        pygame.draw.rect(screen,fc,(x+2,y+2,w-4,h-4))
        textSurf, textRect = textObjects(msg,buttonFont,ic) # Button text
    textRect.center = (x+w/2,y+h/2) # Center point of button
    screen.blit(textSurf, textRect) # Render button text

screen_id = 0 # Enables us to have an intro screen.
intro = pygame.image.load("menuPic.png").convert() # Intro screen image.
while True:
    # Putting the initial screen up
    screen.blit(intro, (0, 0))
    mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
    pygame.display.flip()
    while(screen_id == 0): # Initial screen
        pressed = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
        mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
        if button("Set up game!",25,693,200,50,red,green,buttonFont,5,"lmb") == 1: # Start button
            screen_id = 1
            #print screen_id
        if button("Quit",250,693,200,50,red,green,buttonFont,5,"lmb") == 1: # Quit button
            pygame.quit()
            quit()
        
        if (pygame.key.get_pressed()[pygame.K_t]):
            pass
            #print "t!" # Print t if the user types t on keyboard. Test.
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get(): # Keyboard/mouse event queue
            if event.type == pygame.KEYDOWN:
            
                # determine if a letter key was pressed 
                if event.key == pygame.K_r:
                    #print "r!"
                    pass
                elif event.key == pygame.K_g:
                    #print "g!"
                    pass
                elif event.key == pygame.K_b:
                    #print "b!"
                    pass
                                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    #print "lmb!"
                    pass
                elif event.button == 3: # Right mouse button
                    #print "rmb!"
                    pass
            
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
    xMap = 8 # Map width in zones
    yMap = 6 # Map height in zones
    nPlayers = 4 # Number of players
    turnDelay = 0.2
    turnWait = True
    typedNationName = nationNames[1]
    typedRulerName = rulerNames[1]
    nPickedColor = 1
    typingNationName = True
    typingRulerName = False
    specMode = False # Spectator mode
    # Position of interface elements:
    mapSizeUIx = 25
    mapSizeUIy = 100
    nPlayerUIx = 25
    nPlayerUIy = 175
    delayUIx = 25
    delayUIy = 250
    natNameUIx = 150
    natNameUIy = 325
    colorUIx = 25
    colorUIy = 325
    time.sleep(0.5) # Pause 0.5 s
    for event in pygame.event.get(): pass # Keyboard/mouse event queue

    while (screen_id == 1): # SETTINGS screen
        screen.blit(intro2, (0,0))
        pressed = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
        mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
        if button("Start game!",25,693,200,50,red,green,buttonFont,5,"lmb") == 1: # Start game button
            screen_id = 2
            #print screen_id
        if button("Quit",250,693,200,50,red,green,buttonFont,5,"lmb") == 1: # Quit button
            pygame.quit()
            quit()
        if yMap < 30:
            if button("Height +",mapSizeUIx+100,mapSizeUIy,100,26,red,green,buttonFontSmall,2,"lmb") == 1: # Map size setting
                yMap = yMap + 1
                #print(yMap)
                time.sleep(0.1)
        else: button("Max Height",mapSizeUIx+100,mapSizeUIy,100,26,red,red,buttonFontSmall,2,"None")
        if yMap > 2 and xMap*(yMap-1) >= nPlayers: # Cannot have map with fewer zones than the number of players
            if button("Height -",mapSizeUIx+100,mapSizeUIy+25,100,25,red,green,buttonFontSmall,2,"lmb") == 1: # Map size setting
                yMap = yMap - 1
                #print(yMap)
                time.sleep(0.1)
        else: button("Min Height",mapSizeUIx+100,mapSizeUIy+25,100,25,red,red,buttonFontSmall,2,"None")
        if xMap < 32:
            if button("Width +",mapSizeUIx,mapSizeUIy,100,25,red,green,buttonFontSmall,2,"lmb") == 1: # Map size setting
                xMap = xMap + 1
                #print(xMap)
                time.sleep(0.1)
        else: button("Max Width",mapSizeUIx,mapSizeUIy,100,25,red,red,buttonFontSmall,2,"None")
        if xMap > 2 and (xMap-1)*yMap >= nPlayers: # Cannot have map with fewer zones than the number of players
            if button("Width -",mapSizeUIx,mapSizeUIy+25,100,25,red,green,buttonFontSmall,2,"lmb") == 1: # Map size setting
                xMap = xMap - 1
                #print(xMap)
                time.sleep(0.1)
        else: button("Min Width",mapSizeUIx,mapSizeUIy+25,100,25,red,red,buttonFontSmall,2,"None")
        mapSizeTextSurf, mapSizeTextRect = textObjects("Map Size: "+str(xMap)+"x"+str(yMap),buttonFont,red) # Map size info text
        mapSizeTextRect.topleft = (mapSizeUIx+225,mapSizeUIy+12) # Center point of map size info text
        screen.blit(mapSizeTextSurf, mapSizeTextRect) # Render map size info text
        
        if nPlayers < len(playerColors)-1 and nPlayers < xMap*yMap: # Cannot have more players than there are available player colors and zones on the map
            if button("Players +",nPlayerUIx,nPlayerUIy,100,25,red,green,buttonFontSmall,2,"lmb") == 1: # Number of players setting
                nPlayers = nPlayers + 1
                #print(nPlayers)
                time.sleep(0.1)
        else: button("Max Players",nPlayerUIx,nPlayerUIy,100,25,red,red,buttonFontSmall,2,"None")
        if nPlayers > 2:
            if button("Players -",nPlayerUIx,nPlayerUIy+25,100,25,red,green,buttonFontSmall,2,"lmb") == 1: # Number of players setting
                nPlayers = nPlayers - 1
                #print(nPlayers)
                time.sleep(0.1)
        else: button("Min Players",nPlayerUIx,nPlayerUIy+25,100,25,red,red,buttonFontSmall,2,"None")
        playersTextSurf, playersTextRect = textObjects("Players: "+str(nPlayers),buttonFont,red) # Player number info text
        playersTextRect.topleft = (nPlayerUIx+225,nPlayerUIy+12) # Center point of player number info text
        screen.blit(playersTextSurf, playersTextRect) # Render player number info text

        if turnDelay < 4.95: # Max setting for turn delay time
            if button("Turn Delay +",delayUIx,delayUIy,100,25,red,green,buttonFontSmall,2,"lmb") == 1: # Turn delay setting
                turnDelay = turnDelay + 0.05
                time.sleep(0.1)
        else: button("Max Delay",delayUIx,delayUIy,100,25,red,red,buttonFontSmall,2,"None")
        if turnDelay > 0.05: # Min turn delay time
            if button("Turn Delay -",delayUIx,delayUIy+25,100,25,red,green,buttonFontSmall,2,"lmb") == 1: # Turn delay setting
                turnDelay = turnDelay - 0.05
                time.sleep(0.1)
        else: button("Min Delay",delayUIx,delayUIy+25,100,25,red,red,buttonFontSmall,2,"None")
        if turnWait == True:
            if button("Autogo: OFF",delayUIx+100,delayUIy,100,50,red,green,buttonFontSmall,2,"lmb") == 1: # Auto advance turn setting
                turnWait = False
                time.sleep(0.1)
        else:
            if button("Autogo: ON",delayUIx+100,delayUIy,100,50,green,red,buttonFontSmall,2,"lmb") == 1: # Auto advance turn setting
                turnWait = True
                time.sleep(0.1)
        delayTextSurf, delayTextRect = textObjects("Turn Delay: "+str("{:.2f}".format(turnDelay)),buttonFont,red) # Turn delay info text
        delayTextRect.topleft = (delayUIx+225,delayUIy+12) # Center point of turn delay info text
        screen.blit(delayTextSurf, delayTextRect) # Render turn delay info text

        if nPickedColor < len(playerColors)-1: # Player color picker
            if button("Color",colorUIx,colorUIy,100,50,black,black,buttonFont,0,"lmb",playerColors[nPickedColor]) == 1:
                nPickedColor = nPickedColor + 1
                time.sleep(0.1)
        else:
            if button("Color",colorUIx,colorUIy,100,50,black,black,buttonFont,0,"lmb",playerColors[nPickedColor]) == 1:
                nPickedColor = 1
                time.sleep(0.1)

        if typingNationName == True: # Buttons for picking whether to type nation or ruler name
            button("Type",natNameUIx,natNameUIy,50,25,green,green,buttonFontSmall,2,"lmb")
            if button("Edit",natNameUIx,natNameUIy+25,50,25,red,green,buttonFontSmall,2,"lmb") == 1:
                typingNationName = False
                typingRulerName = True
                time.sleep(0.1)
        elif typingRulerName == True:
            button("Type",natNameUIx,natNameUIy+25,50,25,green,green,buttonFontSmall,2,"lmb")
            if button("Edit",natNameUIx,natNameUIy,50,25,red,green,buttonFontSmall,2,"lmb") == 1:
                typingNationName = True
                typingRulerName = False
                time.sleep(0.1)
        if specMode == False: # Spectator mode button
            if button("Conquest Mode",natNameUIx+400,natNameUIy,250,50,red,green,buttonFont,4,"lmb") == 1:
                specMode = True
                time.sleep(0.1)
        else:
            if button("Spectator Mode",natNameUIx+400,natNameUIy,250,50,yellow,green,buttonFont,4,"lmb") == 1:
                specMode = False
                time.sleep(0.1)
        natNameTextSurf, natNameTextRect = textObjects("Nation Name: "+typedNationName,buttonFont,red) # Nation name info text
        natNameTextRect.topleft = (natNameUIx+60,natNameUIy) # Center point of nation name info text
        screen.blit(natNameTextSurf, natNameTextRect) # Render nation name info text
        rulNameTextSurf, rulNameTextRect = textObjects("Ruler Name: "+typedRulerName,buttonFont,red) # Nation name info text
        rulNameTextRect.topleft = (natNameUIx+60,natNameUIy+25) # Center point of nation name info text
        screen.blit(rulNameTextSurf, rulNameTextRect) # Render nation name info text

        for event in pygame.event.get(): # Keyboard/mouse event queue
            if event.type == pygame.KEYDOWN:
                shift_held = pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]
                
                if event.key == pygame.K_BACKSPACE:
                    if typingNationName == True and len(typedNationName) > 0:
                        typedNationName = typedNationName[0:-1]
                    elif typingRulerName == True and len(typedRulerName) > 0:
                        typedRulerName = typedRulerName[0:-1]
                elif event.key == pygame.K_MINUS:
                    if typingNationName == True and len(typedNationName) < 15:
                        typedNationName = typedNationName+"-"
                    elif typingRulerName == True and len(typedRulerName) < 15:
                        typedRulerName = typedRulerName+"-"
                elif event.key == pygame.K_RETURN: # Press return to swap between typing nation and ruler name
                    if typingNationName == True:
                        typingNationName = False
                        typingRulerName = True
                    elif typingRulerName == True:
                        typingNationName = True
                        typingRulerName = False
                elif event.key <= 127 and shift_held == False:
                    if typingNationName == True and len(typedNationName) < 15:
                        typedNationName = typedNationName+chr(event.key)
                    elif typingRulerName == True and len(typedRulerName) < 15:
                        typedRulerName = typedRulerName+chr(event.key)
                elif event.key <= 127 and shift_held == True:
                    if typingNationName == True and len(typedNationName) < 15:
                        typedNationName = typedNationName+chr(event.key).upper()
                    elif typingRulerName == True and len(typedRulerName) < 15:
                        typedRulerName = typedRulerName+chr(event.key).upper()
                                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    #print "lmb!"
                    pass
                elif event.button == 3: # Right mouse button
                    #print "rmb!"
                    pass
            
            if event.type == pygame.MOUSEMOTION:
                # if mouse moved, add point to list 
                            #very messy hack to display coordinates at to left corner, fix later
                            #works by displaying the coordinates, then adding another intro picture, repeat, etc.
                #screen.blit(intro, (0,0))
                #mouseposDisp = xyfont.render(str(pygame.mouse.get_pos()[0])+", "+str(pygame.mouse.get_pos()[1]), 0, (255,255,0))
                #screen.blit(mouseposDisp, (0, 0))
                #print "Moved!"
                pass
            
        pygame.display.flip()
        clock.tick(tpsMax) # Max ticks per second

    screen.fill((0, 0, 0)) # Black screen
    #intro3  = pygame.image.load("2ndscreen.png").convert()
    #screen.blit(intro3, (0,0))
    pygame.display.flip()
    pressedEnter = 0
    Round = 0 # Round variable
    Turn = 1 # Turn variable
    totZones = xMap*yMap # Total number of zones on map
    Players = [] # Generate player objects
    # Positions of interface elements:
    roundUIx = 25
    roundUIy = 640
    statsUIx = 25
    statsUIy = 670
    scoreUIx = 680
    scoreUIy = 680-12*nPlayers
    scoreUIspacing = 60
    zoneSize = 75
    if xMap > 8 or yMap > 8:
        zoneSize = 50
        if xMap > 12 or yMap > 12:
            zoneSize = 40
            if xMap > 15 or yMap > 15:
                zoneSize = 30
                if xMap > 20 or yMap > 20:
                    zoneSize = 20
    print("Generating player objects")
    for nPlayer in range(0,nPlayers+1):
        currPlayer = player(nPlayer)
        Players.append(currPlayer)
        if nPlayer == 1:
            Players[nPlayer].color = playerColors[nPickedColor]
            Players[nPlayer].nationName = typedNationName
            Players[nPlayer].rulerName = rulerNames[nPlayer]
        else:
            Players[nPlayer].color = playerColors[nPlayer]
            Players[nPlayer].nationName = nationNames[nPlayer]
            Players[nPlayer].rulerName = rulerNames[nPlayer]
            if nPlayer > 1:
                while Players[nPlayer].nationName == Players[1].nationName:
                    Players[nPlayer].nationName = "Kolsebistan"
                while Players[nPlayer].rulerName == Players[1].rulerName:
                    Players[nPlayer].nationName = "Seb Castro"
                while Players[nPlayer].color == Players[1].color:
                    Players[nPlayer].color = pink
        #print(Players[nPlayer].owner)
        #print(Players[nPlayer].color)
    Players[0].dead == True # Set unclaimed player to dead
    if specMode == True: # If spectator mode was chosen, set the player to dead
        Players[1].dead = True
    print("Generating zone objects")
    Zones = [] # Generate zone objects    
    for xZone in range(0,xMap):
        for yZone in range(0,yMap):
            currZone = squareZoneObj(xZone,yZone)
            Zones.append(currZone)
            #print(Zones[xZone*yMap+yZone].x)
            #print(Zones[xZone*yMap+yZone].y)
            #print(Zones[xZone*yMap+yZone].owner)
    nUnclaimedZones = len([t.owner for t in Zones if t.owner == 0]) # Number of unclaimed zones
    time.sleep(0.5)
    for event in pygame.event.get(): pass # Keyboard/mouse event queue

    while (screen_id == 2): # IN-GAME screen
        screen.fill((0, 0, 0)) # Black screen
        pressed = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
        mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
        pygame.draw.rect(screen,gray,(25,25,zoneSize*xMap+10,zoneSize*yMap+10)) # Map frame
        roundTextSurf, roundTextRect = textObjects("R"+str(Round)+"T"+str(Turn),buttonFont,red) # Round info text
        roundTextRect.topleft = (roundUIx,roundUIy) # Top left point of round info text
        screen.blit(roundTextSurf, roundTextRect) # Render round info text
        statsTextSurf, statsTextRect = textObjects("Zones: "+str(Players[1].zones)+" Production: "+str(Players[1].production)+" Technology: "+str(Players[1].technology)+" Tech Rate: "+str(100*Players[1].techrate)+"% Trade: "+str(Players[1].trade)+" Resources: "+str(Players[1].resources),buttonFontSmall,red) # Round info text
        statsTextRect.topleft = (statsUIx,statsUIy) # Top left point of round info text
        screen.blit(statsTextSurf, statsTextRect) # Render round info text

        if button("Statistics",scoreUIx,scoreUIy,200,50,red,green,buttonFont,5,"lmb") == 1: # Statistics button
            #print("Stats!")
            pass
        # Render scoreboard info text
        nTS, nTR = textObjects("Nation",buttonFontSmall,red)
        nTR.topleft = (scoreUIx,scoreUIy+50)
        screen.blit(nTS, nTR)
        zTS, zTR = textObjects("Zones",buttonFontSmall,red)
        zTR.topleft = (scoreUIx+100,scoreUIy+50)
        screen.blit(zTS, zTR)
        pTS, pTR = textObjects("Prod",buttonFontSmall,red)
        pTR.topleft = (scoreUIx+scoreUIspacing+100,scoreUIy+50)
        screen.blit(pTS, pTR)
        tTS, tTR = textObjects("Tech",buttonFontSmall,red)
        tTR.topleft = (scoreUIx+2*scoreUIspacing+100,scoreUIy+50)
        screen.blit(tTS, tTR)
        rTS, rTR = textObjects("Res",buttonFontSmall,red)
        rTR.topleft = (scoreUIx+3*scoreUIspacing+100,scoreUIy+50)
        screen.blit(rTS, rTR)
        if Round == 0:
            sortedPlayers = Players[1:nPlayers+1]
        else:
            sortedPlayers = sorted(Players[1:nPlayers+1], key=attrgetter('zones'), reverse=True)
        for n in range(0,nPlayers): # Render scoreboard stats
            if sortedPlayers[n].dead == False:
                sbcolor = sortedPlayers[n].color
            else:
                sbcolor = gray
            nTS, nTR = textObjects(str(sortedPlayers[n].nationName),buttonFontSmall,sbcolor)
            nTR.topleft = (scoreUIx,scoreUIy+12*n+62)
            screen.blit(nTS, nTR)
            zTS, zTR = textObjects(str(sortedPlayers[n].zones),buttonFontSmall,sbcolor)
            zTR.topleft = (scoreUIx+100,scoreUIy+12*n+62)
            screen.blit(zTS, zTR)
            pTS, pTR = textObjects(str(sortedPlayers[n].production),buttonFontSmall,sbcolor)
            pTR.topleft = (scoreUIx+scoreUIspacing+100,scoreUIy+12*n+62)
            screen.blit(pTS, pTR)
            if sortedPlayers[n].technology < 1000: # Formatting tech value depending on how large the number is
                tTS, tTR = textObjects(str('{0:g}'.format(sortedPlayers[n].technology)),buttonFontSmall,sbcolor)
            elif sortedPlayers[n].technology < 10000:
                tTS, tTR = textObjects(str('{:3.2f}'.format(0.001*sortedPlayers[n].technology))+"k",buttonFontSmall,sbcolor)
            elif sortedPlayers[n].technology < 100000:
                tTS, tTR = textObjects(str('{:3.1f}'.format(0.001*sortedPlayers[n].technology))+"k",buttonFontSmall,sbcolor)
            elif sortedPlayers[n].technology < 1000000:
                tTS, tTR = textObjects(str('{0:g}'.format(round(0.001*sortedPlayers[n].technology)))+"k",buttonFontSmall,sbcolor)
            else:
                tTS, tTR = textObjects(str('{:3.2f}'.format(0.000001*sortedPlayers[n].technology))+"M",buttonFontSmall,sbcolor)
            tTR.topleft = (scoreUIx+2*scoreUIspacing+100,scoreUIy+12*n+62)
            screen.blit(tTS, tTR)
            if sortedPlayers[n].resources < 1000: # Formatting tech value depending on how large the number is
                rTS, rTR = textObjects(str('{0:g}'.format(sortedPlayers[n].resources)),buttonFontSmall,sbcolor)
            elif sortedPlayers[n].resources < 10000:
                rTS, rTR = textObjects(str('{:3.2f}'.format(0.001*sortedPlayers[n].resources))+"k",buttonFontSmall,sbcolor)
            elif sortedPlayers[n].resources < 100000:
                rTS, rTR = textObjects(str('{:3.1f}'.format(0.001*sortedPlayers[n].resources))+"k",buttonFontSmall,sbcolor)
            elif sortedPlayers[n].resources < 1000000:
                rTS, rTR = textObjects(str('{0:g}'.format(round(0.001*sortedPlayers[n].resources)))+"k",buttonFontSmall,sbcolor)
            else:
                rTS, rTR = textObjects(str('{:3.2f}'.format(0.000001*sortedPlayers[n].resources))+"M",buttonFontSmall,sbcolor)
            rTR.topleft = (scoreUIx+3*scoreUIspacing+100,scoreUIy+12*n+62)
            screen.blit(rTS, rTR)
        
        for xZone in range(0,xMap): # Make zone "button"
            for yZone in range(0,yMap):
                if Players[1].dead == False: # If the player is not dead, let it interact with the zones
                    if Zones[xZone*yMap+yZone].owner == 0: # If the zone is unclaimed
                        if squareZone("",30+xZone*zoneSize,30+yZone*zoneSize,zoneSize,zoneSize,gray,Players[1].color,white,"claim") == 1: # If the zone is clicked
                            if Players[1].resources >= 5: # If the player can afford to claim it
                                if Players[1].zones == 0: # If the player has no zones on the map, it can claim any unclaimed zone
                                    #print("The zone has been claimed!")
                                    Zones[xZone*yMap+yZone].owner = 1 # Update the owner of the zone object
                                    Players[1].zones = Players[1].zones + 1 # Update player's zone stat
                                    Players[1].resources = Players[1].resources - 5 # Update player's resource stat
                                elif Zones[xZone*yMap+yZone].isAdjacent(Zones,1,xMap,yMap) == True: # If the player has zones on the map, check if they're adjacent to the one it tries to claim
                                    #print("The zone has been claimed!")
                                    Zones[xZone*yMap+yZone].owner = 1 # Update the owner of the zone object
                                    Players[1].zones = Players[1].zones + 1 # Update player's zone stat
                                    Players[1].resources = Players[1].resources - 5 # Update player's resource stat
                                else:
                                    print("The zones are not adjacent!")
                            else:
                                print("You do not have enough resources to claim the zone!")
                    elif Zones[xZone*yMap+yZone].owner > 1: # If the zone is owned by enemy player
                        if squareZone("",30+xZone*zoneSize,30+yZone*zoneSize,zoneSize,zoneSize,gray,Players[1].color,Players[Zones[xZone*yMap+yZone].owner].color,"claim") == 1: # If the zone is clicked
                            if Players[1].resources >= 10:
                                if Zones[xZone*yMap+yZone].isAdjacent(Zones,1,xMap,yMap) == True:
                                    #print("The zone has been conquered!")
                                    Players[Zones[xZone*yMap+yZone].owner].zones = Players[Zones[xZone*yMap+yZone].owner].zones - 1 # Update enemy player's zone stat
                                    if Players[Zones[xZone*yMap+yZone].owner].zones == 0: # If the other player lost all their zones
                                        Players[Zones[xZone*yMap+yZone].owner].dead = True # They are dead
                                    Zones[xZone*yMap+yZone].owner = 1 # Update the owner of the zone object
                                    Players[1].zones = Players[1].zones + 1 # Update player's zone stat
                                    Players[1].resources = Players[1].resources - 10 # Update player's resource stat
                                else:
                                    pass
                                    #print("The zones are not adjacent!")
                            else:
                                pass
                                #print("You do not have enough resources to claim the zone!")
                    elif Zones[xZone*yMap+yZone].owner == 1: # If the zone is owned by the player
                        if squareZone("",30+xZone*zoneSize,30+yZone*zoneSize,zoneSize,zoneSize,gray,Players[1].color,Players[1].color,"claim") == 1: # If the zone is clicked
                            pass
                            #print("The zone is already yours!")
                else: # If the player is dead, just draw the zones, all owned by the AIs
                    squareZone("",30+xZone*zoneSize,30+yZone*zoneSize,zoneSize,zoneSize,gray,Players[1].color,Players[Zones[xZone*yMap+yZone].owner].color,"None")
        
        if button("Quit",250,693,200,50,red,green,buttonFont,5,"lmb") == 1: # Quit button
            pygame.quit()
            quit()
        if button("End Turn",25,693,200,50,red,green,buttonFont,5,"lmb") == 1 or pressedEnter == 1 or (turnWait == False and Players[1].dead == True): # End turn button
            pressedEnter = 0
            #print("Turn 1 has ended.")
            for Turn in range(2,nPlayers+1): # AI players take their turns here.
                pygame.draw.rect(screen,black,(roundUIx,roundUIy,100,25)) # Overwrite round/turn info text
                roundTextSurf, roundTextRect = textObjects("R"+str(Round)+"T"+str(Turn),buttonFont,red) # Round info text
                roundTextRect.topleft = (roundUIx,roundUIy) # Center point of round info text
                screen.blit(roundTextSurf, roundTextRect) # Render round info text
                button("Processing",25,693,200,50,green,green,buttonFont,5,"None")
                attempt = 0
                while Players[Turn].resources >= 5 and nUnclaimedZones >= 1: # When the player has >= 5 resources and there are unclaimed zones. Problem: If the player is surrounded, this loop can be infinite!
                    if attempt > 5*xMap*yMap: # To avoid infinite loop if the player is surrounded, it gets a max number of attempts.
                        break
                    attempt = attempt + 1
                    pickedZone = random.choice(Zones)
                    if pickedZone.owner == 0: # If the zone is unclaimed
                        if Players[Turn].zones == 0:
                            pickedZone.owner = Turn # Change ownership of the zone
                            Players[Turn].zones = Players[Turn].zones + 1 # Update player's zone stat
                            Players[Turn].resources = Players[Turn].resources - 5 # Update player's resource stat
                        elif pickedZone.isAdjacent(Zones,Turn,xMap,yMap) == True:
                            pickedZone.owner = Turn # Change ownership of the zone
                            Players[Turn].zones = Players[Turn].zones + 1 # Update player's zone stat
                            Players[Turn].resources = Players[Turn].resources - 5 # Update player's resource stat
                    elif pickedZone.owner != Turn and Players[Turn].resources >= 10 and pickedZone.isAdjacent(Zones,Turn,xMap,yMap) == True: # If the zone is owned by another player than this AI
                        Players[pickedZone.owner].zones = Players[pickedZone.owner].zones - 1 # Update other player's zone stat
                        if Players[pickedZone.owner].zones == 0: # If the other player lost all their zones
                            Players[pickedZone.owner].dead = True # They are dead
                        pickedZone.owner = Turn # Change ownership of the zone
                        Players[Turn].zones = Players[Turn].zones + 1 # Update player's zone stat
                        Players[Turn].resources = Players[Turn].resources - 10 # Update player's resource stat
                    nUnclaimedZones = len([t.owner for t in Zones if t.owner == 0]) # Number of unclaimed zones
                while Players[Turn].resources >= 10 and Players[Turn].zones < totZones and Players[Turn].dead == False: # When the player has >= 10 resources, doesn't own all zones and is alive
                    pickedZone = random.choice(Zones)
                    if pickedZone.owner != Turn and pickedZone.owner != 0 and pickedZone.isAdjacent(Zones,Turn,xMap,yMap) == True: # If the zone is not owned by the player or unclaimed
                        Players[pickedZone.owner].zones = Players[pickedZone.owner].zones - 1 # Update other player's zone stat
                        if Players[pickedZone.owner].zones == 0: # If the other player lost all their zones
                            Players[pickedZone.owner].dead = True # They are dead
                        pickedZone.owner = Turn # Change ownership of the zone
                        Players[Turn].zones = Players[Turn].zones + 1 # Update player's zone stat
                        Players[Turn].resources = Players[Turn].resources - 10 # Update player's resource stat
                for xZone in range(0,xMap): # Make zone "button"
                    for yZone in range(0,yMap):
                        if Zones[xZone*yMap+yZone].owner == 0: # If the zone is unclaimed
                            squareZone("",30+xZone*zoneSize,30+yZone*zoneSize,zoneSize,zoneSize,gray,Players[1].color,white,"None")
                        elif Zones[xZone*yMap+yZone].owner > 1: # If the zone is owned by enemy player
                            squareZone("",30+xZone*zoneSize,30+yZone*zoneSize,zoneSize,zoneSize,gray,Players[1].color,Players[Zones[xZone*yMap+yZone].owner].color,"None")
                        elif Zones[xZone*yMap+yZone].owner == 1: # If the zone is owned by the player
                            squareZone("",30+xZone*zoneSize,30+yZone*zoneSize,zoneSize,zoneSize,gray,Players[1].color,Players[1].color,"None")
                pygame.display.flip()
                if Players[Turn].dead == False: # Pause if the player isn't dead
                    time.sleep(turnDelay)
            for nPlayer in range(1,nPlayers+1): # Check if a player has won or been eliminated
                if Players[nPlayer].zones == totZones: # If the player owns all the zones
                    if nPlayer == 1: # If the player is not an AI
                        #print("You won!")
                        time.sleep(3)
                        screen_id = 3
                    else: # If the player is an AI
                        #print("You lost!")
                        time.sleep(3)
                        if specMode == False:
                            screen_id = 4
                        else:
                            screen_id = 5
                elif Players[nPlayer].zones == 0 and nUnclaimedZones == 0 and Players[nPlayer].deathAnnounced == False: # If the player has no zones on the map, there are no unclaimed zones and it is not dead
                    Players[nPlayer].deathAnnounced= True
                    Players[nPlayer].dead = True # Set the player to dead
                    if nPlayer != 1: # If the player is an AI
                        print("Round "+str(Round)+": "+Players[nPlayer].nationName+" has been defeated!")
                    if nPlayer == 1 and specMode == False: # If the player is not an AI
                        print("Round "+str(Round)+": You lost!")
            for nPlayer in range(0,nPlayers+1): # After all turns are taken, update stats.
                if Players[nPlayer].dead == False: # If the player is dead, skip updating their stats
                    Players[nPlayer].production = Players[nPlayer].zones  # Update player's production stat
                    Players[nPlayer].resources = 5 + Players[nPlayer].production + Players[nPlayer].resources + round(0.1*(Players[nPlayer].technology+Players[nPlayer].trade) - 0.001*Players[nPlayer].resources*Players[nPlayer].resources - 0.2*Players[nPlayer].overspent) # Update player's resource stat
                    Players[nPlayer].spentOnTech = round(Players[nPlayer].techrate*Players[nPlayer].resources) # Amount spent on tech this round by the player
                    Players[nPlayer].technology = Players[nPlayer].technology + Players[nPlayer].spentOnTech # Update player's technology stat
                    Players[nPlayer].resources = Players[nPlayer].resources - Players[nPlayer].spentOnTech # Update the player's resource stat
            Round = Round + 1
            Turn = 1

        for event in pygame.event.get(): # Keyboard/mouse event queue. This loop is apparently necessary to make the quit button work.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Pressing enter acts like clicking the end turn button
                    #print "Enter!"
                    pressedEnter = 1
                    
        pygame.display.flip()
        clock.tick(tpsMax) # Max ticks per second

    if screen_id == 3: # WIN screen
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
        if button("Back",25,693,200,50,red,green,buttonFont,5,"lmb") == 1: # Back button
            screen_id = 0
        if button("Quit",250,693,200,50,red,green,buttonFont,5,"lmb") == 1: # Quit button
            pygame.quit()
            quit()

        for event in pygame.event.get(): # Keyboard/mouse event queue
            pass # This loop is apparently necessary to make the quit button work.
            
        pygame.display.flip()
        clock.tick(tpsMax) # Max ticks per second

    if screen_id == 4: # LOSE screen
        screen.fill((0, 0, 0)) # Black screen
        intro5  = pygame.image.load("lose.png").convert()
        screen.blit(intro5, (0,0))
        pygame.display.flip()
        time.sleep(0.5)
        for event in pygame.event.get(): pass # Keyboard/mouse event queue

    while (screen_id == 4):
        pressed = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
        mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
        if button("Back",25,693,200,50,red,green,buttonFont,5,"lmb") == 1: # Back button
            screen_id = 0
        if button("Quit",250,693,200,50,red,green,buttonFont,5,"lmb") == 1: # Quit button
            pygame.quit()
            quit()

        for event in pygame.event.get(): # Keyboard/mouse event queue
            pass # This loop is apparently necessary to make the quit button work.
            
        pygame.display.flip()
        clock.tick(tpsMax) # Max ticks per second

    if screen_id == 5: # SPECTATED screen
        screen.fill((0, 0, 0)) # Black screen
        intro6  = pygame.image.load("spec.png").convert()
        screen.blit(intro6, (0,0))
        pygame.display.flip()
        time.sleep(0.5)
        for event in pygame.event.get(): pass # Keyboard/mouse event queue

    while (screen_id == 5):
        pressed = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
        mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
        if button("Back",25,693,200,50,red,green,buttonFont,5,"lmb") == 1: # Back button
            screen_id = 0
        if button("Quit",250,693,200,50,red,green,buttonFont,5,"lmb") == 1: # Quit button
            pygame.quit()
            quit()

        for event in pygame.event.get(): # Keyboard/mouse event queue
            pass # This loop is apparently necessary to make the quit button work.
            
        pygame.display.flip()
        clock.tick(tpsMax) # Max ticks per second

    time.sleep(0.5) # Pause 0.5 s
    for event in pygame.event.get(): pass # Keyboard/mouse event queue
