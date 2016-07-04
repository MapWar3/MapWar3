# Import some necessary libraries.
import socket
import random
import pygame

pygame.init()
screen = pygame.display.set_mode((1024,768),pygame.RESIZABLE)
pygame.display.set_caption('Map War 3') # Window title
screen = pygame.display.get_surface() # Setting up the screen
screen_id = 0 # Enables us to have an intro screen.
intro = pygame.image.load("menuPic.png").convert() # Intro screen image.
clock = pygame.time.Clock()

# Color definitions
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

# Font definitions
xyfont = pygame.font.SysFont("century", 20,20) # Font of coordinate display
buttonFont = pygame.font.SysFont("verdana", 20,20) # Font for buttons

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
            if action == "startGame":
                print("Action!!!")
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

# Putting the initial screen up
screen.blit(intro, (0, 0))
mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
pygame.display.flip()
while(screen_id == 0): # Initial screen
    pressed = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
    mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
    if button("Start!",25,693,200,50,red,green,"startGame") == 1: # Start button
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
    clock.tick(30) # Max ticks per second
	
intro2  = pygame.image.load("2ndscreen.png").convert()
screen.blit(intro2, (0,0))
pygame.display.flip()
while (screen_id == 1):
    pressed = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
    mouseClick = pygame.mouse.get_pressed() # (l,c,r), 0 or 1 for left, center or right mouse button clicked
    print "test"
    if button("Quit",250,693,200,50,red,green,"quit") == 1: # Quit button
        pygame.quit()
        quit()

    pygame.display.flip()
    clock.tick(30) # Max ticks per second
