#Characters Store

allMerchants = {}

class Merchant():
    def __init__(self, pos, color, personality, hasTalkedBefore, storedConvo = ""):
        self.color = color
        self.personality = personality
        self.storedConvo = storedConvo
        self.hasTalkedBefore = hasTalkedBefore
        self.pos = pos

    def getName(self):
        return self.name

    def getColor(self):
        return self.color

    def getPersona(self):
        return self.personality

    def getStoredConvo(self):
        return self.storedConvo

    def talkedBefore(self):
        return self.hasTalkedBefore

        
