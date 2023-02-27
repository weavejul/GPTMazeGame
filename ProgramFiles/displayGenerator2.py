#Display Generator

import mazeGenerator as mg
import random, time, pygame, math
import gpt, text
import characterStore as charStr

"""fonts = pygame.font.get_fonts()
print(len(fonts))
for f in fonts:
    print(f)"""


#Modes
textMode = False
scrollEnd = False
isScrolling = True
canEnterText = False
shownText = "Testing"
textResponse = ""


personalities = ["joyful", "pensive", "intellectual", "rowdy", "meek"]

#Generate Maze/Cells

worldDimensions = [30, 20]
world = mg.WorldGeneration(worldDimensions[0], worldDimensions[1], 25)
world.generateMaze()
world.generateRooms(["small"])
#world.printMaze()

gameCells = [[world.allCellsAndHalls[int(j / 5)][int(i / 5)] for i in range(len(world.allCellsAndHalls[0]) * 5)]
             for j in range(len(world.allCellsAndHalls) * 5)]

tempGameCells = [[world.allCellsAndHalls[int(j / 5)][int(i / 5)] for i in range(len(world.allCellsAndHalls[0]) * 5)]
             for j in range(len(world.allCellsAndHalls) * 5)]
for y in range(len(gameCells)):
    for x in range(len(gameCells[0])):
        if gameCells[y][x] == 1:
            if x >= 1 and x <= len(gameCells[0]) and y >= 1 and y <= len(gameCells):
                if gameCells[y - 1][x] == 0:
                    tempGameCells[y][x] = 2
                elif gameCells[y + 1][x] == 0:
                    tempGameCells[y][x] = 2
                elif gameCells[y][x + 1] == 0:
                    tempGameCells[y][x] = 2
                elif gameCells[y][x - 1] == 0:
                    tempGameCells[y][x] = 2

gameCells = tempGameCells

#Movement variables
move = "none"
animationTick = 0
walkingLeft = False


#Fonts
globalFonts = ["script.ttf", "cambria.ttf"]
img_char1 = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\char1.png")
img_char1 = pygame.transform.scale(img_char1, (500, 500))
img_char2 = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\merchantChar.png")
img_char2 = pygame.transform.scale(img_char2, (500, 500))
globalPictures = [None, img_char1, img_char2]

#Init Pygame
pygame.init()
win = pygame.display.set_mode((0, 0))#, pygame.FULLSCREEN)
winSize = pygame.display.get_surface().get_size()
pygame.display.set_caption("The Maze")

zoomFactor = 100
posDeterminerX = int((winSize[0]/2)/zoomFactor)
posDeterminerY = int((winSize[1]/2)/zoomFactor)

#Images
image_cobblestone = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\cobblestone.png")
image_cobblestone = pygame.transform.scale(image_cobblestone, (zoomFactor, zoomFactor))
cobblestoneCopy = image_cobblestone.copy()
image_blackstone = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\blackstone.png")
image_blackstone = pygame.transform.scale(image_blackstone, (zoomFactor, zoomFactor))
blackstoneCopy = image_blackstone.copy()
image_gravel = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\gravel.jpg")
image_gravel = pygame.transform.scale(image_gravel, (zoomFactor, zoomFactor))
gravel_copy = image_gravel.copy()
floorType = [image_blackstone, image_cobblestone, image_gravel, cobblestoneCopy, gravel_copy]

image_vingette = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\vingette.jpg")
image_vingette = pygame.transform.scale(image_vingette, winSize)
image_biggerVingette = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\biggervingette.png")
image_biggerVingette = pygame.transform.scale(image_biggerVingette, winSize)

image_blackSquare = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\blackSquare.jpg")
image_blackSquare = pygame.transform.scale(image_blackSquare, (zoomFactor, zoomFactor))

walking_man = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\TinyAdventurer\walking_sheet.png")
walking_man = pygame.transform.scale(walking_man, (zoomFactor * 6, zoomFactor))
idle_man = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\TinyAdventurer\idle_sheet.png")
idle_man = pygame.transform.scale(idle_man, (zoomFactor * 5, zoomFactor))

image_redMerchant = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\merchantRed.png")
image_redMerchant = pygame.transform.scale(image_redMerchant, (zoomFactor * 5, zoomFactor * 5))
image_blueMerchant = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\merchantBlue.png")
image_blueMerchant = pygame.transform.scale(image_blueMerchant, (zoomFactor * 5, zoomFactor * 5))
image_greenMerchant = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\merchantGreen.png")
image_greenMerchant = pygame.transform.scale(image_greenMerchant, (zoomFactor * 5, zoomFactor * 5))
image_yellowMerchant = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\merchantYellow.png")
image_yellowMerchant = pygame.transform.scale(image_yellowMerchant, (zoomFactor * 5, zoomFactor * 5))

merchants = [image_redMerchant, image_blueMerchant, image_greenMerchant, image_yellowMerchant]

image_merchantChar = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\merchant.png")
image_merchantChar = pygame.transform.scale(image_merchantChar, (zoomFactor, zoomFactor))

#Positions of Characters
characterBlocks = charStr.allMerchants.keys()
#print(list(charStr.allMerchants.keys())[0])
accurateMerchantPos = [(int(keys.split(" ")[0]) * 5 + 2, int(keys.split(" ")[1]) * 5 + 5) for keys in list(charStr.allMerchants.keys())]

def drawCurrentScreen(pos):
        cellPos = [int(pos[0]/zoomFactor), int(pos[1]/zoomFactor)]
        xModulo = -(pos[0] % zoomFactor)
        yModulo = -(pos[1] % zoomFactor)
        #print(floorType)
        #print()
        merchantXModifier = 0
        merchantYModifier = 0
        merchantPos = []
        for y in range(int(posDeterminerY*2)):
            for x in range(int(posDeterminerX*2)):
                if x >= 0 and y >= 0 and x < len(gameCells[0]) and y < len(gameCells):

                    if cellPos[1] - y >= 0 and cellPos[0] - x >= 0:
                        if gameCells[cellPos[1] - y][cellPos[0] - x] != None:
                            win.blit(floorType[gameCells[cellPos[1] - y][cellPos[0] - x] + 1], (winSize[0]/2 + xModulo - zoomFactor*x, winSize[1]/2 + yModulo - zoomFactor*y, zoomFactor, zoomFactor))
                            #pygame.draw.rect(win, (255, 255, 255), (winSize[0]/2 + xModulo - zoomFactor*x, winSize[1]/2 + yModulo - zoomFactor*y, zoomFactor, zoomFactor))
                        else:
                             win.blit(floorType[0], (winSize[0]/2 + xModulo - zoomFactor*x, winSize[1]/2 + yModulo - zoomFactor*y, zoomFactor, zoomFactor))
                    else:
                        win.blit(floorType[0], (winSize[0]/2 + xModulo - zoomFactor*x, winSize[1]/2 + yModulo - zoomFactor*y, zoomFactor, zoomFactor))

                    if cellPos[1] - y >= 0 and cellPos[0] + x < len(gameCells[0]):
                        if gameCells[cellPos[1] - y][cellPos[0] + x] != None:
                            win.blit(floorType[gameCells[cellPos[1] - y][cellPos[0] + x] + 1], (winSize[0]/2 + xModulo + zoomFactor*x, winSize[1]/2 + yModulo - zoomFactor*y, zoomFactor, zoomFactor))
                            #pygame.draw.rect(win, (255, 255, 255), (winSize[0]/2 + xModulo + zoomFactor*x, winSize[1]/2 + yModulo - zoomFactor*y, zoomFactor, zoomFactor))
                        else:
                            win.blit(floorType[0], (winSize[0]/2 + xModulo + zoomFactor*x, winSize[1]/2 + yModulo - zoomFactor*y, zoomFactor, zoomFactor))
                    else:
                        win.blit(floorType[0], (winSize[0]/2 + xModulo + zoomFactor*x, winSize[1]/2 + yModulo - zoomFactor*y, zoomFactor, zoomFactor))
                    if cellPos[1] + y < len(gameCells) and cellPos[0] - x >= 0:
                        if gameCells[cellPos[1] + y][cellPos[0] - x] != None:
                            win.blit(floorType[gameCells[cellPos[1] + y][cellPos[0] - x] + 1], (winSize[0]/2 + xModulo - zoomFactor*x, winSize[1]/2 + yModulo + zoomFactor*y, zoomFactor, zoomFactor))
                            #pygame.draw.rect(win, (255, 255, 255), (winSize[0]/2 + xModulo - zoomFactor*x, winSize[1]/2 + yModulo + zoomFactor*y, zoomFactor, zoomFactor))
                        else:
                            win.blit(floorType[0], (winSize[0]/2 + xModulo - zoomFactor*x, winSize[1]/2 + yModulo + zoomFactor*y, zoomFactor, zoomFactor))
                    else:
                        win.blit(floorType[0], (winSize[0]/2 + xModulo - zoomFactor*x, winSize[1]/2 + yModulo + zoomFactor*y, zoomFactor, zoomFactor))
                    if cellPos[1] + y < len(gameCells) and cellPos[0] + x < len(gameCells[0]):
                        if gameCells[cellPos[1] + y][cellPos[0] + x] != None:
                            win.blit(floorType[gameCells[cellPos[1] + y][cellPos[0] + x] + 1], (winSize[0]/2 + xModulo + zoomFactor*x, winSize[1]/2 + yModulo + zoomFactor*y, zoomFactor, zoomFactor))
                            #pygame.draw.rect(win, (255, 255, 255), (winSize[0]/2 + xModulo + zoomFactor*x, winSize[1]/2 + yModulo + zoomFactor*y, zoomFactor, zoomFactor))
                        else:
                            win.blit(floorType[0], (winSize[0]/2 + xModulo + zoomFactor*x, winSize[1]/2 + yModulo + zoomFactor*y, zoomFactor, zoomFactor))
                    else:
                        win.blit(floorType[0], (winSize[0]/2 + xModulo + zoomFactor*x, winSize[1]/2 + yModulo + zoomFactor*y, zoomFactor, zoomFactor))




                        
def drawCharacterModels(animation):
    if move == "none":
        if walkingLeft:
            win.blit(pygame.transform.flip(idle_man, True, False), (winSize[0]/2 - zoomFactor/2, winSize[1]/2 - zoomFactor/2), (zoomFactor*(int((pygame.time.get_ticks() - animationTick)/1000)%5), 0, zoomFactor, zoomFactor))
        else:
            win.blit(idle_man, (winSize[0]/2 - zoomFactor/2, winSize[1]/2 - zoomFactor/2), (zoomFactor*(int((pygame.time.get_ticks() - animationTick)/1000)%5), 0, zoomFactor, zoomFactor))
    else:
        if walkingLeft:
            win.blit(pygame.transform.flip(walking_man, True, False), (winSize[0]/2 - zoomFactor/2, winSize[1]/2 - zoomFactor/2), (zoomFactor*(int((pygame.time.get_ticks() - animationTick)/200)%5), 0, zoomFactor, zoomFactor))
        else:
            win.blit(walking_man, (winSize[0]/2 - zoomFactor/2, winSize[1]/2 - zoomFactor/2), (zoomFactor*(int((pygame.time.get_ticks() - animationTick)/200)%5), 0, zoomFactor, zoomFactor))

def drawEntities():
    cellPos = [int(pos[0]/zoomFactor), int(pos[1]/zoomFactor)]
    xModulo = -(pos[0] % zoomFactor)
    yModulo = -(pos[1] % zoomFactor)
    for y in range(int(posDeterminerY*2)):
        for x in range(int(posDeterminerX*2)):
            if x >= 0 and y >= 0 and x < len(gameCells[0]) and y < len(gameCells):
                #TODO Make this NOT overflow on th edges
                if cellPos[1] - y >= 0 and cellPos[0] - x >= 0 and gameCells[cellPos[1] - y][cellPos[0] - x] != None and gameCells[cellPos[1] - y][cellPos[0] - x] + 1 == 4:
                        #print(gameCells[cellPos[1] - y - 1][cellPos[0] - x])
                        #sprint(gameCells[cellPos[1] - y][cellPos[0] - x - 1])
                        if gameCells[cellPos[1] - y - 1][cellPos[0] - x] == 1 and gameCells[cellPos[1] - y][cellPos[0] - x - 1] == 1:
                            #print(str(int((cellPos[0] - x)/5)) + " " + str(int((cellPos[1] - y)/5)))
                            #print(charStr.allMerchants.keys())
                            win.blit(merchants[charStr.allMerchants.get("" + str(int((cellPos[0] - x)/5)) + " " + str(int((cellPos[1] - y)/5))).color], (winSize[0]/2 + xModulo - zoomFactor*x, winSize[1]/2 + yModulo - zoomFactor*y, zoomFactor*5, zoomFactor*5))
                            win.blit(image_merchantChar, (winSize[0]/2 + xModulo - zoomFactor*(x-2), winSize[1]/2 + yModulo - zoomFactor*(y-5), zoomFactor, zoomFactor))
                            
                if cellPos[1] - y >= 0 and cellPos[0] + x < len(gameCells[0]) and gameCells[cellPos[1] - y][cellPos[0] + x] != None and gameCells[cellPos[1] - y][cellPos[0] + x] + 1 == 4:
                        #print(gameCells[cellPos[1] - y - 1][cellPos[0] - x])
                        #sprint(gameCells[cellPos[1] - y][cellPos[0] - x - 1])
                        if gameCells[cellPos[1] - y - 1][cellPos[0] + x] == 1 and gameCells[cellPos[1] - y][cellPos[0] + x - 1] == 1:
                            #print(str(int((cellPos[0] - x)/5)) + " " + str(int((cellPos[1] - y)/5)))
                            #print(charStr.allMerchants.keys())
                            win.blit(merchants[charStr.allMerchants.get("" + str(int((cellPos[0] + x)/5)) + " " + str(int((cellPos[1] - y)/5))).color], (winSize[0]/2 + xModulo + zoomFactor*x, winSize[1]/2 + yModulo - zoomFactor*y, zoomFactor*5, zoomFactor*5))
                            win.blit(image_merchantChar, (winSize[0]/2 + xModulo + zoomFactor*(x+2), winSize[1]/2 + yModulo - zoomFactor*(y-5), zoomFactor, zoomFactor))

                if cellPos[1] + y < len(gameCells) and cellPos[0] - x >= 0 and gameCells[cellPos[1] + y][cellPos[0] - x] != None and gameCells[cellPos[1] + y][cellPos[0] - x] + 1 == 4:
                        #print(gameCells[cellPos[1] - y - 1][cellPos[0] - x])
                        #sprint(gameCells[cellPos[1] - y][cellPos[0] - x - 1])
                        if gameCells[cellPos[1] + y - 1][cellPos[0] - x] == 1 and gameCells[cellPos[1] + y][cellPos[0] - x - 1] == 1:
                            #print(str(int((cellPos[0] - x)/5)) + " " + str(int((cellPos[1] - y)/5)))
                            #print(charStr.allMerchants.keys())
                            win.blit(merchants[charStr.allMerchants.get("" + str(int((cellPos[0] - x)/5)) + " " + str(int((cellPos[1] + y)/5))).color], (winSize[0]/2 + xModulo - zoomFactor*x, winSize[1]/2 + yModulo + zoomFactor*y, zoomFactor*5, zoomFactor*5))
                            win.blit(image_merchantChar, (winSize[0]/2 + xModulo - zoomFactor*(x-2), winSize[1]/2 + yModulo + zoomFactor*(y+5), zoomFactor, zoomFactor))

                if cellPos[1] + y < len(gameCells) and cellPos[0] + x < len(gameCells[0]) and gameCells[cellPos[1] + y][cellPos[0] + x] != None and gameCells[cellPos[1] + y][cellPos[0] + x] + 1 == 4:
                        #print(gameCells[cellPos[1] - y - 1][cellPos[0] - x])
                        #sprint(gameCells[cellPos[1] - y][cellPos[0] - x - 1])
                        if gameCells[cellPos[1] + y - 1][cellPos[0] + x] == 1 and gameCells[cellPos[1] + y][cellPos[0] + x - 1] == 1:
                            #print(str(int((cellPos[0] - x)/5)) + " " + str(int((cellPos[1] - y)/5)))
                            #print(charStr.allMerchants.keys())
                            win.blit(merchants[charStr.allMerchants.get("" + str(int((cellPos[0] + x)/5)) + " " + str(int((cellPos[1] + y)/5))).color], (winSize[0]/2 + xModulo + zoomFactor*x, winSize[1]/2 + yModulo + zoomFactor*y, zoomFactor*5, zoomFactor*5))
                            win.blit(image_merchantChar, (winSize[0]/2 + xModulo + zoomFactor*(x+2), winSize[1]/2 + yModulo + zoomFactor*(y+5), zoomFactor, zoomFactor))

def drawUI():
    fontScript = pygame.font.Font(r"C:\Users\mrwum\Desktop\MazeProgram\Fonts\calibri.ttf", 18)
    textImg = fontScript.render("Money: " + str(money), True, (255, 255, 255))
    win.blit(textImg, (10, 10))
    textImg = fontScript.render("Lvl (" + str(armorLevel) + ") Armor (Health = " + str(armorHealth) + ")", True, (255, 255, 255))
    win.blit(textImg, (winSize[0] - textImg.get_size()[0] - 10, 10))
    textImg = fontScript.render("Lvl (" + str(weaponLevel) + ") Sword (Damage = " + str(weaponDamage) + ")", True, (255, 255, 255))
    win.blit(textImg, (winSize[0] - textImg.get_size()[0] - 10, textImg.get_size()[1] + 10))
    pygame.display.update()
    
def isCornerSafe(pos):
    if gameCells[math.floor((pos[1])/zoomFactor)][math.floor((pos[0])/zoomFactor)] in [None, 3]:
        return False
    return True


def canMove(pos, direction, speed):
    pos = [int(pos[0] - zoomFactor/2), int(pos[1] - zoomFactor/2)]
    if direction == "Up":
        totalMovement = 0
        for pixel in range(pos[1] - 1, pos[1] - speed - 1, -1):
            if isCornerSafe([pos[0], pixel]) and isCornerSafe([pos[0] + zoomFactor - 1, pixel]) and pixel >= 0:
                totalMovement += 1
            else:
                break
        return -1 * totalMovement
    if direction == "Left":
        totalMovement = 0
        for pixel in range(pos[0] - 1, pos[0] - speed - 1, -1):
            if isCornerSafe([pixel, pos[1]]) and isCornerSafe([pixel, pos[1] + zoomFactor - 1]) and pixel >= 0:
                totalMovement += 1
            else:
                break
        return -1 * totalMovement
    if direction == "Down":
        totalMovement = 0
        for pixel in range(pos[1] + zoomFactor, pos[1] + speed + zoomFactor):
            if pixel < len(gameCells)*zoomFactor and isCornerSafe([pos[0] + zoomFactor - 1, pixel]) and isCornerSafe([pos[0], pixel]):
                totalMovement += 1
            else:
                break
        return totalMovement
    if direction == "Right":
        totalMovement = 0
        for pixel in range(pos[0] + zoomFactor, int(pos[0] + speed + zoomFactor)):

            if pixel < len(gameCells[0])*zoomFactor and isCornerSafe([pixel, pos[1] + zoomFactor - 1]) and isCornerSafe([pixel, pos[1]]):
                totalMovement += 1
            else:
                break
        return totalMovement

def printMap(currentCell):
    size = 15
    initPos = [int((winSize[0] - size*(worldDimensions[0]*2-1)) / 2), int((winSize[1] - size*(worldDimensions[1]*2-1)) / 2)]
    pygame.draw.rect(win, (0, 0, 0), (0, 0, winSize[0], winSize[1]))
    for cell in visitedCells:
        pygame.draw.rect(win, (255, 255, 255), (initPos[0] + size*cell[0], initPos[1] + size*cell[1], size, size))
        if cell == currentCell:
            pygame.draw.rect(win, (255, 0, 0), (initPos[0] + size*cell[0] + 3, initPos[1] + size*cell[1] + 3, size - 6, size - 6))
        pygame.display.update()
    end = False
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    end = True
                    break
                if event.key == pygame.K_ESCAPE:
                    end = True
        

global pos
pos = [38 + 150,38 + 150]
visitedCells = []
merchantInteract = False

difficultySpeed = .5
difficultyDamage = 1
healthMonster = 5

armorLevel = 1
weaponLevel = 1
armorHealth = 10
weaponDamage = 3

money = 0

clock = pygame.time.Clock()


previousSavedCell = []
while 1:
    clock.tick(60)
    currentCell = [math.floor((pos[0]/zoomFactor)/5), math.floor((pos[1]/zoomFactor)/5)]
    if currentCell not in visitedCells:
        visitedCells.append(currentCell)
    if previousSavedCell != currentCell and random.randrange(30) == 10 and not gameCells[int(pos[1]/zoomFactor)][int(pos[0]/zoomFactor)] in [1, 3]:
        move = "none"
        if text.fight(difficultySpeed, difficultyDamage, healthMonster, armorHealth, weaponDamage):
            money += difficultyDamage * 5

    previousSavedCell = currentCell.copy()
    merchantInteract = False
    if (int(pos[0]/zoomFactor), int(pos[1]/zoomFactor)) in accurateMerchantPos:
        merchantInteract = True
    
    pygame.draw.rect(win, (0, 0, 0), (0, 0, winSize[0], winSize[1]))
    if not textMode:
        if gameCells[int(pos[1]/zoomFactor)][int(pos[0]/zoomFactor)] in [0, 2]:
            floorType = [blackstoneCopy, cobblestoneCopy, image_gravel, cobblestoneCopy, gravel_copy]
            drawCurrentScreen(pos)
            drawCharacterModels(0)
            drawEntities()
            filter = pygame.surface.Surface(winSize)
            filter.fill(pygame.color.Color('Black'))
            filter.blit(image_vingette, (0, 0))
            win.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            drawUI()
        elif gameCells[int(pos[1]/zoomFactor)][int(pos[0]/zoomFactor)] == 1:
            image_blackstone = image_blackSquare
            image_cobblestone = image_blackSquare
            floorType = [image_blackstone, image_cobblestone, image_gravel, cobblestoneCopy, gravel_copy]
            drawCurrentScreen(pos)
            drawCharacterModels(0)
            drawEntities()
            drawUI()
    else:
        if merchantInteract:
            #print(str(int((pos[0]/zoomFactor)/5)) + " " + str(int((pos[1]/zoomFactor)/5) - 1))
            #print(list(charStr.allMerchants.keys()))
            currentCharacterInteract = charStr.allMerchants.get(str(int((pos[0]/zoomFactor)/5)) + " " + str(int((pos[1]/zoomFactor)/5) - 1))
            response = text.questionResponse("Talk (T) or upgrade (U)?")
            if response in ["u", "U"]:
                entered = False
                while not entered:
                    response2 = text.questionResponse("Armor (A) or Weapon (W)?")
                    if response2 in ["w", "W"]:
                        text.scrollConversation("You have upgraded your weapon for 5 gold.", 0)
                        money -= 5
                        weaponLevel += 1
                        weaponDamage += 2
                        difficultyDamage += 1
                        entered = True
                    elif response2 in ["a", "A"]:
                        text.scrollConversation("You have upgraded your armor for 10 gold.", 0)
                        money -= 10
                        armorLevel += 1
                        armorHealth += 5
                        difficultyHealth += 2 
                        entered = True
                    else:
                        text.scrollConversation("Not understood. Please try again.", 0)
            elif response in ["t", "T"]:
                if currentCharacterInteract.getStoredConvo() == "":
                    text.gptConvo(currentCharacterInteract, "You walk up to a merchant. 'Greetings, traveller! How may I assist you today? Perhaps you would look at my wares?'", 2, '''You are an adventurer who has been exploring a gargantuan maze-like dungeon for a long, long time. You have recently stopped at a large room in the dungeon, with merchants and other adventurers bustling about. You decide to interact with one of the many merchants here. The merchants sell everything availiable to them in the dungeons, from weapons to potions. The merchant you walk up to is wearing a typical brown leathered merchant's suit, and a tie.

You: *Walks up to him*

Character: Greetings, traveller! How may I assist you today? Perhaps you would look at my wares?''')
                else:
                    text.gptConvo(currentCharacterInteract, "You walk up to a merchant you've talked to before.", 2, currentCharacterInteract.getStoredConvo())
        else:
            personality = personalities[random.randrange(len(personalities))]
            text.gptConvo(None, """You walk up to a """ + personality + """"-seeming person you find in the dungeon. You decide to begin a conversation.""", 1, '''You are an adventurer who has been exploring a gargantuan maze-like dungeon for a long, long time. You have recently stopped at a large room in the dungeon, with merchants and other adventurers bustling about. You decide to interact with one of the many adventurers here. He seems very ''' + personality + '''.

You: Hello.

Character: Hello.''')

        textMode = False

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            break
        elif event.type == pygame.KEYDOWN and not textMode:
            if event.key == pygame.K_s:
                move = "Down"
                animationTick = pygame.time.get_ticks()
                #pos = [pos[0], pos[1] + 50]
            if event.key == pygame.K_a:
                move = "Left"
                walkingLeft = True
                animationTick = pygame.time.get_ticks()
                #pos = [pos[0] - 50, pos[1]]
            if event.key == pygame.K_d:
                move = "Right"
                walkingLeft = False
                animationTick = pygame.time.get_ticks()
                #pos = [pos[0] + 50, pos[1]]
            if event.key == pygame.K_w:
                #pos = [pos[0], pos[1] - 50]
                move = "Up"
                animationTick = pygame.time.get_ticks()
            if event.key == pygame.K_n:
                print(pos)
            if event.key == pygame.K_m:
                printMap(currentCell)
            if event.key == pygame.K_ESCAPE:
                run = False
                pygame.quit()
                break
            if event.key == pygame.K_SPACE:# and merchantInteract:
                if merchantInteract:
                    textMode = True
                    canEnterText = True
                    shownText = "You walk up to a merchant."
                else:
                    textMode = True
                    canEnterText = True
                    shownText = "You walk up to a person in the dungeons."
        elif event.type == pygame.KEYDOWN and textMode:
            if canEnterText:
                if event.key == pygame.K_BACKSPACE:
                    shownText = shownText[:-1]
                elif event.key != pygame.K_TAB:
                    shownText += event.unicode
            if event.key == pygame.K_RETURN:
                shownText = ""
                canEnterText = True
                if canEnterText:
                    textResponse = shownText.copy()
            elif event.key == pygame.K_ESCAPE:
                textMode = False
            

        elif event.type == pygame.KEYUP and not textMode:
            if event.key == pygame.K_s:
                if move == "Down":
                    move = "none"
                    
            if event.key == pygame.K_a:
                if move == "Left":
                    move = "none"
            if event.key == pygame.K_d:
                if move == "Right":
                    move = "none"
            if event.key == pygame.K_w:
                if move == "Up":
                    move = "none"

    speed = 10
    if move != "none":
        if move == "Up":
            pos = [pos[0], pos[1] + canMove(pos, "Up", speed)]
        if move == "Down":
            pos = [pos[0], pos[1] + canMove(pos, "Down", speed)]
        if move == "Left":
            pos = [pos[0] + canMove(pos, "Left", speed), pos[1]]
        if move == "Right":
            pos = [pos[0] + canMove(pos, "Right", speed), pos[1]]

pygame.quit()
