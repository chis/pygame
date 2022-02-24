import pygame, sys, random
from pygame.locals import *



# constants representing colours
BLACK = (0,   0,   0  )
BROWN = (153, 76,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)
GREY  = (128, 128, 128)
RED   = (255, 0,   0  )
WHITE = (255, 255, 255)


# constants representing the different resources
DIRT    = 0
GRASS   = 1
WATER   = 2
COAL    = 3
ROCK    = 4
DIAMOND = 5
CLOUD   = 6
WOOD    = 7
SAND    = 8
BRICK   = 9
GLASS   = 10
FIRE    = 11
CLOUD2  = 12

# a dictionary linking resources to textures
textures = {
            DIRT    : pygame.image.load('dirt.png'),
            GRASS   : pygame.image.load('grass.png'),
            WATER   : pygame.image.load('water.png'),
            COAL    : pygame.image.load('coal.png'),
            ROCK    : pygame.image.load('rock.png'),
            DIAMOND : pygame.image.load('diamond.png'),
            CLOUD   : pygame.image.load('cloud.png'),
            CLOUD2  : pygame.image.load('cloud2.png'),
            WOOD    : pygame.image.load('wood.png'),
            BRICK   : pygame.image.load('brick.png'),
            SAND    : pygame.image.load('sand.png'),
            GLASS   : pygame.image.load('glass.png'),
            FIRE    : pygame.image.load('fire.png'),

}

inventory = {
            DIRT    : 0,
            GRASS   : 0,
            WATER   : 0,
            COAL    : 0,
            DIAMOND : 0,
            ROCK    : 0,
            WOOD    : 0,
            BRICK   : 0,
            SAND    : 0,
            FIRE    : 0,
            GLASS   : 0
}

# maps each resource to the EVENT key used to place/craft it
controls = {
            DIRT : 49,
            COAL : 50,
            WOOD : 51,
            ROCK : 52,
            BRICK: 53,
            FIRE:  54,
            GLASS: 55,
            SAND : 56
}



craft = {
        FIRE    : { WOOD: 2, ROCK : 2},
        GLASS   : { FIRE: 1, SAND : 2},
        DIAMOND : { WOOD: 2, COAL : 3},
        BRICK   : { ROCK: 2, FIRE : 1},
        SAND    : { ROCK: 2          }
}




# useful game dimensions
TILESIZE =  20
MAPWIDTH =  45
MAPHEIGHT = 30


# a list of resources
resources = [DIRT, GRASS, WATER, COAL, ROCK, DIAMOND, WOOD, BRICK, GLASS, SAND, FIRE]
# use list comprehension to create our tilemap
tilemap = [ [DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT) ]

animation = {
            CLOUD  :  { "cloudx" :  random.randint(-300, 1),  "cloudy": random.randint(0,MAPHEIGHT*TILESIZE), "speed" : random.randint(24,1000)},
            CLOUD2 :  { "cloudx"  : random.randint(-100, 1),  "cloudy": random.randint(0,MAPHEIGHT*TILESIZE), "speed" : random.randint(24,1000)}
}

# set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE + 58))

pygame.display.set_caption('M I N E C R A F T -- 2 D')
pygame.display.set_icon(pygame.image.load('player.png'))

# the player image
PLAYER = pygame.image.load('player.png').convert_alpha()
# the position of the player [x,y]
playerPos = [0,0]
# add a font for our inventory
INVFONT = pygame.font.Font('data/fonts/Hack-Regular.ttf', 18)

for rw in range(MAPHEIGHT):
    # loop through each column in that row
    for cl in range(MAPWIDTH):
        # pick a random number between 0 and 15
        randomNumber = random.randint(0,25)
        diamondNumber = random.randint(0,60)
        # if a zero, then the tile is coal
        if randomNumber == 0:
            tile = COAL
        # water if the random number is a 1 or a 2
        elif randomNumber == 1 or randomNumber == 2:
            tile = WATER
        elif randomNumber >= 3 and randomNumber <= 15:
            tile = GRASS
        elif randomNumber >= 16 and randomNumber <= 20:
            tile = ROCK
        elif randomNumber >= 21 and randomNumber <= 25:
            tile = WOOD
        elif diamondNumber == 1:
            tile = DIAMOND
        else:
            tile = DIRT
        # set the position in the tilemap to the randomly chosen tile
        tilemap[rw][cl] = tile


while True:

    DISPLAYSURF.fill(BLUE)

    # get all the user events
    for event in pygame.event.get():
        # if the user wants to quit
        if event.type == QUIT:
            # end the game and close the window
            pygame.quit()
            sys.exit()
        # if a key is pressed
        elif event.type == KEYDOWN:
            # if the right arrow is pressed
            if (event.key == K_RIGHT) and playerPos[0] < MAPWIDTH -1:
                # change the player's x position
                playerPos[0] += 1
            if (event.key == K_LEFT) and playerPos[0] > 0:
                playerPos[0] -= 1
            if (event.key == K_DOWN) and playerPos[1] < MAPHEIGHT -1:
                playerPos[1] += 1
            if (event.key == K_UP) and playerPos[1] > 0:
                playerPos[1] -= 1
            if event.key == K_SPACE:
                # what resource is the player standing on?
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                # player now has 1 more of this resource
                inventory[currentTile] += 1
                # the player is now standing on dirt
                tilemap[playerPos[1]][playerPos[0]] = DIRT

            for key in controls:

                # if this key was pressed
                if (event.key == controls[key]):

                    # CRAFT if the mouse is also pressed
                    if pygame.mouse.get_pressed()[0]:

                        #if the item can be crafted
                        if key in craft:

                            # keep track of whether we have the resources
                            # to craft this item
                            canBeMade = True
                            # for each item needed to craft...
                            for i in craft[key]:
                                # if we don't have enough
                                if craft[key][i] > inventory[i]:
                                    # we can't craft it!
                                    canBeMade = False
                                    break
                            #if we can craft it (we have all needed resources)
                            if canBeMade == True:
                                # take each item from the inventory
                                for i in craft[key]:
                                    inventory[i] -= craft[key][i]
                                # add the crafted item to the inventory
                                inventory[key] += 1

                     #PLACE if the mouse wasn't pressed
                    else:

                        # get the tile the player is standing on
                        currentTile = tilemap[playerPos[1]][playerPos[0]]
                        # if we have the item to place
                        if inventory[key] > 0:
                             # take it from the inventory
                             inventory[key] -= 1
                             # swap it with the tile we are standing on
                             inventory[currentTile] += 1
                             # place the item
                             tilemap[playerPos[1]][playerPos[0]] = key

            


    # loop through each row
    for row in range(MAPHEIGHT):
        # loop through each column in the row
        for column in range(MAPWIDTH):
            DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE,row*TILESIZE))
    
    # display the player at the correct position
    DISPLAYSURF.blit(PLAYER,(playerPos[0]*TILESIZE, playerPos[1]*TILESIZE))

    
    # TODO: MAKE MORE CLOUDS
   # fpsClock = pygame.time.Clock()
    #display the cloud
  #  DISPLAYSURF.blit(textures[CLOUD].convert_alpha(), (cloudx,cloudy))
    # move the cloud to the left slightly
  #  cloudx+=1
    # if the cloud has moved past the map
  #  if cloudx > MAPWIDTH*TILESIZE:
        # pick a new position to place the cloud
  #      cloudy = random.randint(0,MAPHEIGHT*TILESIZE)
  #      cloudx = -200

 #   fpsClock.tick(1000)


    for clouds in animation:
        fpsClock = pygame.time.Clock()
        DISPLAYSURF.blit(textures[clouds].convert_alpha(), (animation[clouds]["cloudx"],animation[clouds]["cloudy"]))
        animation[clouds]["cloudx"]+=1
        fpsClock.tick(animation[clouds]["speed"])


    # display the inventory, starting 10 pixels in
    placePosition = 10
    for item in resources:
        # add the image
        DISPLAYSURF.blit(textures[item],(placePosition,MAPHEIGHT*TILESIZE+20))
        placePosition += 40
        # add the text showing the amount in the inventory
        textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAYSURF.blit(textObj,(placePosition,MAPHEIGHT*TILESIZE+35))
        placePosition +=40

    
    # update the display
    pygame.display.update()
 
