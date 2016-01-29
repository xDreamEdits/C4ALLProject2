import pygame
import time
import random

pygame.init()

#colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

display_width = 1200
display_height = 800

gameDisplay = pygame.display.set_mode((display_width, display_height))

#Title
pygame.display.set_caption("Whatever its called")

#Time Variables
FPS = 30
clock = pygame.time.Clock()

def gameLoop():

    #Game states
    gameExit = False
    gameOver = False

    #Position variables
    lead_x = display_width/2
    lead_y = display_height/2

    while not gameExit:
        while gameOver == True:
            print("GameOver")
            gameDisplay.fill(black)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.K_q:
                    gameExit = True
                    gameOver = False
                elif event.type == pygame.K_c:
                    gameLoop()


    gameDisplay.fill(black)

    pygame.display.update()



    #Un-Init Game
    pygame.quit()
    #Quit Python
    quit()
    
                    
            
    
    