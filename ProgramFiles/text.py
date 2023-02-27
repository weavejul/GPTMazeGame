#Text
import pygame, gpt, time
import characterStore as charStr

pygame.init()
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
winSize = pygame.display.get_surface().get_size()
pygame.display.set_caption("The Maze")


globalFonts = [(r"C:\Users\mrwum\Desktop\MazeProgram\Fonts\calibri.ttf", 72), (r"C:\Users\mrwum\Desktop\MazeProgram\Fonts\cour.ttf", 63), (r"C:\Users\mrwum\Desktop\MazeProgram\Fonts\arial.ttf", 64)]
img_char1 = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\char1.png")
img_char1 = pygame.transform.scale(img_char1, (450, 450))
img_char2 = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\merchantChar.png")
img_char2 = pygame.transform.scale(img_char2, (450, 450))

img_monster = pygame.image.load(r"C:\Users\mrwum\Desktop\MazeProgram\Images\monster.png")
img_monster = pygame.transform.scale(img_monster, (450, 450))
globalPictures = [None, img_char1, img_char2]


#TEST
#fontScript = pygame.font.Font(r"C:\Users\mrwum\Desktop\MazeProgram\Fonts\cour.ttf", 63)
#textImg = fontScript.render("1", True, (255, 255, 255))
#print(textImg.get_size())
#TEST

textMode = True
scrollEnd = True
isScrolling = True
canEnterText = False
shownText = "Testing"
textResponse = ""


def drawText(text, pos, font, scroll):
    textImg = font.render(text, True, (255, 255, 255))
    textSize = textImg.get_size()
    textPos = pos
    if textPos[0] + textSize[0] > winSize[0] - 30 and not scroll:
        textPos = (textPos[0] - ((textPos[0] + textSize[0]) - winSize[0] + 30), textPos[1])
    win.blit(textImg, textPos)
    if time.time() % 1 > 0.5:
        pygame.draw.rect(win, (255, 255, 255), (textPos[0] + textSize[0], textPos[1], 3, textSize[1]))
        pygame.display.update()

def drawConversation(text):
    fontScript = pygame.font.Font(r"C:\Users\mrwum\Desktop\MazeProgram\Fonts\calibri.ttf", 72)
    textImg = fontScript.render("1", True, (255, 255, 255))
    textSize = textImg.get_size()
    pygame.draw.rect(win, (255, 255, 255), (0, winSize[1] - winSize[1]/3, winSize[0], winSize[1]/3))
    borderSize = 4
    pygame.draw.rect(win, (0, 0, 0), (borderSize, winSize[1] - winSize[1]/3 + borderSize, winSize[0] - borderSize*2, winSize[1]/3 - borderSize*2))
    drawText(text, (20, (winSize[1] * (5/6)) - textSize[1]/2), fontScript, False)

def scrollConversation(text, character):
    xSpeed = .5
    #print(text)
    global scrollEnd, isScrolling
    fontScript = pygame.font.Font(globalFonts[character][0], globalFonts[character][1])
    #print(globalFonts[character])
    textImg = fontScript.render(text, True, (255, 255, 255))
    xPos = 20
    textSize = textImg.get_size()
    #print(scrollEnd)
    while not scrollEnd:
        pygame.draw.rect(win, (255, 255, 255), (0, winSize[1] - winSize[1]/3, winSize[0], winSize[1]/3))
        borderSize = 4
        pygame.draw.rect(win, (0, 0, 0), (borderSize, winSize[1] - winSize[1]/3 + borderSize, winSize[0] - borderSize*2, winSize[1]/3 - borderSize*2))
        drawText(text, (xPos, (winSize[1] * (5/6)) - textSize[1]/2), fontScript, True)
        pygame.display.update()
        #print(xPos + textSize[0])
        if xPos + textSize[0] < winSize[0] - 30:
            scrollEnd = True
            isScrolling = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scrollEnd = True
                elif event.key == pygame.K_RETURN:
                    scrollEnd = True
                    xPos = winSize[0] - 30 - textSize[0]
                elif event.key == pygame.K_s:
                    xSpeed += 3
        xPos -= xSpeed

    quitLoop = False
    textPos = [xPos, winSize[1] * (5/6)]
    while not quitLoop:
        #if time.time() % 1 > 0.5:
        pygame.draw.rect(win, (255, 255, 255), (0, winSize[1] - winSize[1]/3, winSize[0], winSize[1]/3))
        borderSize = 4
        pygame.draw.rect(win, (0, 0, 0), (borderSize, winSize[1] - winSize[1]/3 + borderSize, winSize[0] - borderSize*2, winSize[1]/3 - borderSize*2))
        drawText(text, (xPos, (winSize[1] * (5/6)) - textSize[1]/2), fontScript, True)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scrollEnd = True
                    quitLoop = True
                if event.key == pygame.K_RETURN:
                    scrollEnd = True
                    quitLoop = True

def questionResponse(text):
    scrollConversation(text, 0)
    shownText = ""
    while True:
        fontScript = pygame.font.Font(globalFonts[0][0], 72)
        
        isScrolling = True
        canEnterText = False
        scrollEnd = False
        drawConversation(":: " + shownText)
        canEnterText = True
        scrollEnd = True
        isScrolling = False
    
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    isScrolling = False
                    canEnterText = False
                    return shownText
                elif event.key == pygame.K_ESCAPE:
                    isScrolling = False
                    canEnterText = False
                    return None
                elif event.key == pygame.K_BACKSPACE:
                    shownText = shownText[:-1]
                elif event.key != pygame.K_TAB:
                    shownText += event.unicode

                isScrolling = False
                canEnterText = False
    

def gptConvo(charData, startingText, character, startLogs):
    global scrollEnd, isScrolling, canEnterText
    textMode = True
    totalLogs = startLogs
    shownText = startingText
    while textMode:
        #print("\n\n\nTOTAL LOGS:\n" + totalLogs)
        pygame.display.update()
        canEnterText = False
        isScrolling = True
        scrollEnd = False
        scrollConversation(":: " + shownText, character)
        scrollEnd = True
        canEnterText = True
        shownText = ""
        entered = False
        isScrolling = False
        while not entered:
            fontScript = pygame.font.Font(globalFonts[0][0], 72)
            
            isScrolling = True
            canEnterText = False
            scrollEnd = False
            drawConversation(":: " + shownText)
            canEnterText = True
            scrollEnd = True
            isScrolling = False
        
            win.blit(globalPictures[character], ((winSize[0] / 2) - (globalPictures[character].get_size()[0] / 2), 20))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        entered = True
                        totalLogs += "\n\nYou: " + shownText + "\n\nCharacter:"
                        #print("\n\n\nTotalLogsINPROGRAM\n" + totalLogs)
                        returnedText = ""
                        while returnedText == "":
                            returnedText = gpt.ask(totalLogs, totalLogs)
                        totalLogs += " " + returnedText
                        shownText = returnedText
                        #print("ShownText = " + shownText)
                    elif event.key == pygame.K_ESCAPE:
                        scrollEnd = True
                        isScrolling = False
                        canEnterText = False
                        entered = True
                        textMode = False
                        if charData != None:
                            charData.storedConvo = totalLogs + "\n\nYou leave, and decide to go elsewhere. Eventually, after a while, you return.\n\n"
                    elif event.key == pygame.K_BACKSPACE:
                        shownText = shownText[:-1]
                    elif event.key != pygame.K_TAB:
                        shownText += event.unicode

                    isScrolling = False
                    canEnterText = False

def fightInstance(difficulty):
    hasEnded = False
    fightBarSize = 750
    barPos = 0
    forwards = True
    pygame.draw.rect(win, (0, 0, 0), (0, 0, winSize[0], winSize[1]))
    win.blit(img_monster, ((winSize[0] / 2) - (img_monster.get_size()[0] / 2), 20))
    while not hasEnded:
        pygame.draw.rect(win, (255, 255, 255), (0, winSize[1] - winSize[1]/3, winSize[0], winSize[1]/3))
        borderSize = 4
        pygame.draw.rect(win, (0, 0, 0), (borderSize, winSize[1] - winSize[1]/3 + borderSize, winSize[0] - borderSize*2, winSize[1]/3 - borderSize*2))
        pygame.draw.rect(win, (255, 255, 255), ((winSize[0] - fightBarSize)/2, winSize[1] * (2/3) + ((winSize[1] * (1/3) - 100) / 2), fightBarSize, 100))
        pygame.draw.rect(win, (0, 255, 0), ((winSize[0] - fightBarSize / 4)/2, winSize[1] * (2/3) + ((winSize[1] * (1/3) - 100) / 2), fightBarSize/4, 100))
        pygame.draw.rect(win, (255, 140, 0), ((winSize[0] - fightBarSize / 8)/2, winSize[1] * (2/3) + ((winSize[1] * (1/3) - 100) / 2), fightBarSize/8, 100))
        pygame.draw.rect(win, (255, 0, 0), ((winSize[0] - fightBarSize / 16)/2, winSize[1] * (2/3) + ((winSize[1] * (1/3) - 100) / 2), fightBarSize/16, 100))
        pygame.draw.rect(win, (0, 0, 0), ((winSize[0] - fightBarSize)/2 + barPos, winSize[1] * (2/3) + ((winSize[1] * (1/3) - 100) / 2), fightBarSize/128, 100))
        #print(barPos)

        if barPos + difficulty < fightBarSize and forwards:
            barPos += difficulty
        elif barPos + difficulty >= fightBarSize and forwards:
            barPos -= difficulty
            forwards = False
        elif barPos - difficulty > 0 and not forwards:
            barPos -= difficulty
        elif barPos - difficulty <= 0 and not forwards:
            barPos += difficulty
            forwards = True

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if barPos >= fightBarSize / 2 - fightBarSize / 32 and barPos <= fightBarSize / 2 + fightBarSize / 32:
                        return True
                    else:
                        return False
                    
def fight(difficultySpeed, difficultyDamage, healthMonster, healthPlayer, damage):
    totalDamageOnM = 0
    totalDamageOnH = 0
    justEncountered = True
    while totalDamageOnM < healthMonster and totalDamageOnH < healthPlayer:
        #win.blit(img_monster, ((winSize[0] / 2) - (img_monster.get_size()[0] / 2), 20))
        if justEncountered:
            scrollConversation(":: " + "You encounter a monster!", 0)
            justEncountered = False
        else:
            scrollConversation(":: " + "You gear up for another round of blows!", 0)
            
        if fightInstance(difficultySpeed):
            scrollConversation(":: " + "You dealt " + str(damage) + " damage!", 0)
            totalDamageOnM += damage
            if totalDamageOnM >= healthMonster:
                break
        else:    
            scrollConversation(":: " + "You missed!", 0)

        scrollConversation(":: " + "The monster takes its turn...", 0)
        scrollConversation(":: " + "The monster deals " + str(difficultyDamage) + " damage to you!", 0)
        totalDamageOnH += difficultyDamage

    if totalDamageOnM >= healthMonster:
        scrollConversation(":: " + "The monster has been vanquished!", 0)
        scrollConversation(":: " + "You earned " + str(difficultyDamage * 5) + " gold!", 0)
        return True
    
    scrollConversation(":: " + "The monster has defeated you!", 0)
    scrollConversation(":: " + "You perished in the dungeons...", 0)
    return False
    

#print(questionResponse("do you good?"))
#fight(1, 5, 10, 10, 5)
#gptConvo(0)
#pygame.quit()
