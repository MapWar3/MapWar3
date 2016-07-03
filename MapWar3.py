# Import some necessary libraries.
import socket
import random
import pygame

pygame.init()
screen = pygame.display.set_mode((1024,768),pygame.RESIZABLE)
pygame.display.set_caption('Map War 3') # Window title
screen = pygame.display.get_surface() #Setting up the screen
screen_id = 0 #Enables us to have an intro screen.
intro = pygame.image.load("menuPic.png").convert() #Intro screen image.
clock = pygame.time.Clock()

#Putting the initial screen up.
screen.blit(intro, (0, 0))
pygame.display.flip()

#font used to display xy coordinates of mouse
xyfont = pygame.font.SysFont("century", 20,20)

while(screen_id == 0): # Initial screen
    pressed = pygame.key.get_pressed()
    #print "Test"
    if (pygame.key.get_pressed()[pygame.K_t]):
        print "t!"
    
    alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
    ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
    
    for event in pygame.event.get():
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
                #mousePos = pygame.mouse.get_pos() # (x,y) of cursor relative to top left of display
                #if mousePos[1] > 100 &
            elif event.button == 3: # Right mouse button
                print "rmb!"
        
        if event.type == pygame.MOUSEMOTION:
            # if mouse moved, add point to list 
			#very messy hack to display coordinates at to left corner, fix later
			#works by displaying the coordinates, then adding another intro picture, repeat, etc.
			screen.blit(intro, (0,0))
			mousepos = xyfont.render(str(pygame.mouse.get_pos()[0])+", "+str(pygame.mouse.get_pos()[1]), 0, (255,255,0))
			screen.blit(mousepos, (0, 0))
			print "Moved!"
            
    #screen.fill((0, 0, 0)) # Black screen
    pygame.display.flip()
    clock.tick(60) # Max 60 ticks per second
