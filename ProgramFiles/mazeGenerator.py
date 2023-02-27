#Maze Generator

import random, time
import characterStore as charStr

personalities = ["joyful", "brash", "bored", "tired", "upset", "pessemistic", "insane", "regal", "whimsical"]


class Stack():
    def __init__(self, initialList):
        self.stack = []
        if len(initialList) != 0:
            for item in initialList:
                self.stack.append(item)

    def add(self, item):
        self.stack.append(item)

    def popStack(self):
        self.stack.pop(-1)

    def getStack(self):
        return self.stack

class WorldGeneration():
    def __init__(self, width, height, roomFrequency):
        self.width = width # Should be odd, as well as height
        self.height = height
        self.roomFrequency = roomFrequency
        self.allCellsAndHalls = [[None for i in range(self.width * 2 - 1)] for j in range(self.height * 2 - 1)]# Y, X
        self.visitedCells = []

    def isSurrounded(self, cell, roomsVisited):
        cellsToGoTo = []
        if not(cell[0] - 1 < 0) and not((cell[0] - 1, cell[1]) in roomsVisited.getStack()):
            cellsToGoTo.append((-1, 0))
        if not(cell[0] + 1 >= self.height) and not((cell[0] + 1, cell[1]) in roomsVisited.getStack()):
            cellsToGoTo.append((1, 0))
        if not(cell[1] - 1 < 0) and not((cell[0], cell[1] - 1) in roomsVisited.getStack()):
            cellsToGoTo.append((0, -1))
        if not(cell[1] + 1 >= self.width) and not((cell[0], cell[1] + 1) in roomsVisited.getStack()):
            cellsToGoTo.append((0, 1))

        return cellsToGoTo

    def generateMaze(self): # Y, X
        initialCells = [[None for i in range(self.width)]for j in range(self.height)] # Y, X
        roomsVisited = Stack([(0, 0)])
        trueCellsVisited = Stack([(0, 0)])

        self.allCellsAndHalls[0][0] = 0

        while len(roomsVisited.getStack()) > 0:
            #self.printMaze()
            #print(len(roomsVisited.getStack()))
            placesToGo = self.isSurrounded(roomsVisited.getStack()[-1], trueCellsVisited)
            if len(placesToGo) == 0:
                roomsVisited.popStack()
            else:
                newCell = placesToGo[random.randrange(len(placesToGo))]
                self.allCellsAndHalls[roomsVisited.getStack()[-1][0]* 2 + newCell[0] * 2][roomsVisited.getStack()[-1][1]* 2 + newCell[1] * 2] = 0
                self.allCellsAndHalls[roomsVisited.getStack()[-1][0]* 2 + newCell[0]][roomsVisited.getStack()[-1][1]* 2 + newCell[1]] = 0
                trueCellsVisited.add((roomsVisited.getStack()[-1][0] + newCell[0], roomsVisited.getStack()[-1][1] + newCell[1]))
                roomsVisited.add((roomsVisited.getStack()[-1][0] + newCell[0], roomsVisited.getStack()[-1][1] + newCell[1]))
                #self.allCellsAndHalls[roomsVisited.getStack()[-1][0]* 2 + newCell[0] * -1][roomsVisited.getStack()[-1][1]* 2 + newCell[1] * -1] = 0

    def generateRooms(self, possibleRoomTypes):
        roomsLeft = self.roomFrequency
            
        while roomsLeft > 0:
            roomY = random.randrange(len(self.allCellsAndHalls))
            roomX = random.randrange(len(self.allCellsAndHalls[0]))
            canRoomWork = True
            roomType = possibleRoomTypes[random.randrange(len(possibleRoomTypes))]
            
            if roomType == "small": #SMALL ROOMS
                if roomY - 1 > 0 and roomX - 1 > 0 and roomY + 5 < len(self.allCellsAndHalls) and roomX + 5 < len(self.allCellsAndHalls[0]):
                    for y in range(roomY, roomY + 6):
                        for x in range(roomX, roomX + 6):
                            if self.allCellsAndHalls[y][x] == 1:
                                canRoomWork = False
                                break
                else:
                    canRoomWork = False

                if canRoomWork:
                    roomsLeft -=1
                    for y in range(roomY, roomY + 5):
                        for x in range(roomX, roomX + 5):
                            if x - roomX in [1, 3] and y - roomY in [1, 3]:
                                self.allCellsAndHalls[y][x] = 3
                                charStr.allMerchants.update({"" + str(x) + " " + str(y): charStr.Merchant((x, y), random.randrange(0, 4), personalities[random.randrange(len(personalities))], False)})
                            else:
                                self.allCellsAndHalls[y][x] = 1
                            
            elif roomType == "medium": # MEDIUM ROOMS
                if roomY - 1 > 0 and roomX - 1 > 0 and roomY + 5 < len(self.allCellsAndHalls) and roomX + 5 < len(self.allCellsAndHalls[0]):
                    for y in range(roomY - 1, roomY + 6):
                        for x in range(roomX - 1, roomX + 6):
                            if self.allCellsAndHalls[y][x] == 1:
                                canRoomWork = False
                                break
                else:
                    canRoomWork = False
                    
                if canRoomWork:
                    roomsLeft -=1
                    for y in range(roomY, roomY + 5):
                        for x in range(roomX, roomX + 5):
                            self.allCellsAndHalls[y][x] = 1
                            
            elif roomType == "large": #LARGE ROOMS
                if roomY - 1 > 0 and roomX - 1 > 0 and roomY + 7 < len(self.allCellsAndHalls) and roomX + 7 < len(self.allCellsAndHalls[0]):
                    for y in range(roomY - 1, roomY + 8):
                        for x in range(roomX - 1, roomX + 8):
                            if self.allCellsAndHalls[y][x] == 1:
                                canRoomWork = False
                                break
                else:
                    canRoomWork = False
                    
                if canRoomWork:
                    roomsLeft -=1
                    for y in range(roomY, roomY + 7):
                        for x in range(roomX, roomX + 7):
                            self.allCellsAndHalls[y][x] = 1
                
    
    def printMaze(self):
        for row in self.allCellsAndHalls:
            for item in row:
                if item != None:
                    if item == 0:
                        print("██", end = "")
                    if item == 1:
                        print("▒▒", end = "")
                else:
                    print("  ", end = "")
            print()
                    
#world = WorldGeneration(30, 20, 15)
#world.generateMaze()
#world.generateRooms(["small"])
#for row in world.allCellsAndHalls:
#    for item in row:
#        if item == None:
#            print("N", end = " ")
#        else:
            #print(item, end=" ")
    #print()

#world = WorldGeneration(30, 20, 15)
#world.generateMaze()
#world.generateRooms(["small"])
#world.printMaze()
#time.sleep(10000)
