import pygame
import time
import random
import math

pygame.init()

#Colour palette 
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
blue = (0,0,255)

#Window dimensions; resolution
display_width = 1200
display_height = 800

winMode = pygame.DOUBLEBUF | pygame.HWSURFACE #| pygame.FULLSCREEN #Enable hardware acceleration, remove first comment for fullscreen

#fullscreenToggle = input("Fullscreen? Y/N")
#if fullscreenToggle=="Y" or fullscreenToggle=="y":
        #winMode = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN

gameDisplay = pygame.display.set_mode((display_width, display_height),winMode) #Initialise pygame window

#Title and caption
pygame.display.set_caption("C4 ALL Project 2")

#Time Variables, initialise FPS clock
FPS = 100 #One frame = Ten milliseconds
clock = pygame.time.Clock()

#Universe stores all object information, inMemory determines what to load
universe = []
inMemory = []
memLimit = 50 #How many objects to leave in memory

texX = 0 #Player X position variable for text, for controlled updating
texY = 0 #Player Y position for text
texSpeed = 0 #Player speed for text

class Ship:
        """This class deals with player controlled movement"""

        def __init__(self, display_width, display_height):

            Ship = pygame.image.load("spaceship.png") #Load the sprite image
            
            self.dir = 0 #Direction of ship in degrees, taken from a north bearing
            self.rot = 0 #Current rotation amount
            self.posX = 0 #X position of player on map
            self.posY = 0 #Y position of player on map
            self.accX = 0 #X acceleration of player
            self.accY = 0 #Y acceleration of player
            self.dW = display_width #Screen width
            self.dH = display_height #Screen height

            self.adv = False #Is ship accelerating?
            

            #store ship image dimensions
            self.sW, self.sH = Ship.get_size()

            #centre ship by subtracting half ship size from given dimensions
            gameDisplay.blit(Ship, (self.dW/2-self.sW*0.5,self.dH/2-self.sH*0.5))

        def update(self):
            global display_height, display_width

            #Modulo on direction to prevent direction exeeding 360 degrees
            self.dir = self.dir % 360
            #Increment direction by rotation amount
            self.dir += self.rot
            
            if self.adv == True:
                
                self.accX += -math.sin(math.radians(self.dir))*0.01 #Sine rule to find change in player X acceleration
                self.accY += -math.sin(math.radians(90-self.dir))*0.01 #Sine rule to find change in player Y acceleration

            #Rotate ship to current direction
            Ship = pygame.transform.rotate(pygame.image.load("spaceship.png"),self.dir)

            spriteW, spriteH = Ship.get_size()

            gameDisplay.blit(Ship, (display_width/2-spriteW*0.5,display_height/2-spriteH*0.5))

            self.posX +=self.accX
            self.posY +=self.accY

        def rotL(self):
            self.rot = 1 #Rotate anticlockwise 1 degree per frame
        def rotR(self):
            self.rot = -1 #Rotate clockwise 1 degree per frame
            
        def fwd(self):
            self.adv = True

        """def reload(self):
            Ship = pygame.image.load("spaceship.png") #Load the sprite image
            self.dW = display_width #Screen width
            self.dH = display_height #Screen height
            
            #centre ship by subtracting half ship size from given dimensions
            gameDisplay.blit(Ship, (self.dW/2-self.sW*0.5,self.dH/2-self.sH*0.5))"""

            
            
        

class NotAShip:
    """Placeholder class used for objects that are not the player, i.e. ones that need scrolling"""

    def __init__(self, posX, posY, img, GM):

        global universe, inMemory

        Object = pygame.image.load(img) #This time, we take an image as a string as a parameter too

        self.sW, self.sH = Object.get_size()

        self.posX = posX
        self.posY = posY
        self.disX = posX + 5*self.sW/6 #Centering only affects an object's initial screen position so this is done before the blit, multipliers to compensate for pygame's bad centering
        self.disY = posY + 2*self.sH/3
        self.img = img #We maintain the image path as an attribute so it need only be provided once
        self.GM = GM*2000 #Gravitational constant
        self.inMem = True #Planet starts in memory

        gameDisplay.blit(Object, (self.disX,self.disY))

        universe.append(self)
        inMemory.append(self)

    
    def update(self):

        self.disX += -player.accX #Evaluate difference in object to player position on the screen
        self.disY += -player.accY

        Object = pygame.image.load(self.img)

        self.dxPlayer = -(self.disX - 5*self.sW/6) #X difference in player/object position
        self.dyPlayer = self.disY - 2*self.sH/3 #Y difference in player/object position
        self.disPlayer = math.sqrt(self.dxPlayer**2+self.dyPlayer**2) #Pythagoras Theorem used to calculate distance between object and player

        #Gravity constraints to prevent unnecssary calculations or to prevent ship getting trapped on planet
        if self.disPlayer > 0.25*self.sW and self.disPlayer < 1000*self.sW:

                if self.dxPlayer < 0: #Is X distance to object negative?
                        self.negX = True
                else:
                        self.negX = False
                        
                if self.dyPlayer < 0: #Is Y distance to object negative?
                        self.negY = True
                else:
                        self.negY = False

                """Here we need to establish the bearing from the object to the ship, to do this, we find which quadrant around the object the ship is in, and
                   use the necessary parameters to find the angle using trig"""
                
                if not (self.negX or self.negY): #In First Quadrant?
                        m = 1
                        c = 0
                        a = self.dyPlayer
                        
                elif not(self.negY): #In Second or Third Quadrant?
                        m = -1
                        c = 2 * math.pi
                        a = self.dyPlayer
                        
                else: #If none of the above, must be fourth quadrant
                        m = 1
                        c = 0.5 * math.pi
                        a = self.dxPlayer
                        
                
                self.dirPlayer = c + m*((math.acos(a/self.disPlayer)) % (2*math.pi)) #Arcosine with quadrant parameters to find player direction from object, modulo to get bearing

                deltaD = self.GM/self.disPlayer**2 #Simplified gravity inverse square law, we take force as change in distance, since change in time is handled already

                player.accX += -deltaD*math.sin(self.dirPlayer) #Sine rule to find X acceleration change
                player.accY += deltaD*math.sin(0.5*math.pi-self.dirPlayer) #Sine rule to find Y acceleration change

        gameDisplay.blit(Object, (math.floor(self.disX),math.floor(self.disY))) #We use floor division as we cannot have fractional pixels
        


#Game states
gameExit = False
gameOver = False

#Screen position variables: DO NOT CONFUSE WITH PLAYER POSITION
scrPos_x = display_width/2
scrPos_y = display_height/2

#init player
player = Ship(scrPos_x, scrPos_y)

Object1 = NotAShip(250,250,"earth.jpg",0.4) #Places an Earth object
Object2 = NotAShip(1200,1200,"moon.jpg",0.05) #Places a Moon object
Object3 = NotAShip(-500,-500,"mars.jpg",0.3) #Places a Mars object

fullscreenStat = False

while not gameExit:
    
    if gameOver == True:

        #Finishes the game by printing to the console and ending the loop
        print("GameOver")
        gameExit = True
        

    #Obtain all user events as a sequence and put them in a for loop
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN: #When key is down
                
            
            if event.key == pygame.K_a: #A button turns ship left
                    player.rotL()
            if event.key == pygame.K_d: #D button turns ship right
                    player.rotR()
            if event.key == pygame.K_w: #W accelerates the ship
                    player.fwd()
            if event.key == pygame.K_q: #Quit (useful for fullscreen)
                    gameOver = True
            if event.key == pygame.K_p: #P for fullscreen lol
                    if fullscreenStat == True:
                            winMode = pygame.DOUBLEBUF | pygame.HWSURFACE
                            display_width = 1200
                            display_height = 800
                            gameDisplay = pygame.display.set_mode((display_width, display_height),winMode)
                            fullscreenStat = False
                    else:
                            winMode = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN #Set display variable to include fullscreen
                            display_width = 1920
                            display_height = 1080
                            gameDisplay = pygame.display.set_mode((display_width, display_height),winMode) #Generate new display fullscreen
                            #player.reload()
                            fullscreenStat = True
        
        if event.type == pygame.KEYUP: #When key is released
            if event.key == pygame.K_a or event.key == pygame.K_d: #Stop rotation if A or D was released
                    player.rot = 0
            if event.key == pygame.K_w: #Stop accelerating if W is released
                    player.adv = False
        

        #Allows a user to close the window using the close button
        if event.type == pygame.QUIT:
                gameOver = True
                
       
    
    #Undraw objects with black, call all update methods for objects
    gameDisplay.fill(black)

    if len(inMemory) > memLimit: #Check if memory limit exceeded, removed earliest entry in memory list if so
                inMemory[0].inMem = False
                inMemory[0].remove()

    for planet in inMemory: #Update all objects in memory
            planet.update()

    for planet in universe: #Display any unloaded planet if within distance criteria and is not already in memory
            if planet.disX < display_width*1.5 and planet.disX < display_width*-1.5 and planet.disY > display_height*1.5 and planet.disY < display_height*-1.5 and planet.inMem == False:
                    planet.inMem = True
                    inMemory += planet

    player.update() #Update player object

    font = pygame.font.Font("trench.otf", 36) #Defines sci-fi font from external file


    #Intentionally slow down text updates, it is very distracting and hard to read when they are updated once per frame
    if pygame.time.get_ticks() % 4 == 0:
            texY = player.posY
            texX = player.posX
            texSpeed = round(40*math.sqrt((player.accX)**2+(player.accY)**2),1)
            
    statBar = pygame.Surface((display_width,36)) #Create a stats GUI bar as a surface
    statBar.set_alpha(200) #Make bar partly transparent                
    statBar.fill((20,50,150)) #Colour bar blue           
    gameDisplay.blit(statBar, (0,display_height-36)) #Render GUI bar at bottom of screen   
    
    text = font.render("X: " + str(math.floor(texX)) + "        Y: " + str(math.floor(texY)) + "        SPEED: " + str(texSpeed) + "km/s" , 1, (100, 200, 255)) #Render GUI text, floor division used for variables for readability
    textRect = text.get_rect()
    textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
    textRect.centery = (math.floor(display_height-18))
    gameDisplay.blit(text, textRect)

    #Update display
    pygame.display.update()

    #Clock ticks to run at FPS
    clock.tick(FPS)



#Close window, end game
pygame.quit()



                
            
    
    
