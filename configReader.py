import os, ConfigParser

class ConfigReader(object):
    def __init__(self, path, debug = None):
        self.debug = debug
        self.debugMsg("opening config file and creating configParser")
        self.parser = ConfigParser.ConfigParser()
        cFile = open(os.path.join(path, "mai-bot.cfg"))
        self.debugMsg("config file open, checking config file")
        self.parser.readfp(cFile)
        if not self.parser.has_section("mai-bot-cfg"):
            raise ValueError("invalid config file")
        self.debugMsg("config file is valid, ready to read values")
        cFile.close()

    def getKey(self, key):
        return self.parser.get("mai-bot-cfg", key)
        
    def getMaxSpeed(self):
        if self.parser.has_option("mai-bot-cfg", "max-speed"):
            return self.parser.getint("mai-bot-cfg", "max-speed")
        else:
            return 255
  
    def getDistModifier(self):
        if self.parser.has_option("mai-bot-cfg", "dist-modifier"):
            return self.parser.getint("mai-bot-cfg", "dist-modifier")
        else:
            return 10
            
    def getDistModifierBegin(self):
        if self.parser.has_option("mai-bot-cfg", "dist-mod-begin"):
            return self.parser.getint("mai-bot-cfg", "dist-mod-begin")
        else:
            return 80
            
    def getCamResX(self):
        if self.parser.has_option("mai-bot-cfg", "cam-res-x"):
            return self.parser.getint("mai-bot-cfg", "cam-res-x")
        else:
            return 800
            
    def getCamResY(self):
        if self.parser.has_option("mai-bot-cfg", "cam-res-y"):
            return self.parser.getint("mai-bot-cfg", "cam-res-y")
        else:
            return 600
    
    def getMaxTries(self):
        if self.parser.has_option("mai-bot-cfg", "max-tries"):
            return self.parser.getint("mai-bot-cfg", "max-tries")
        else:
            return 2
    
    def getDirection(self):
        if self.parser.has_option("mai-bot-cfg", "direction"):
            return self.parser.get("mai-bot-cfg", "direction")
        else:
            return "left"
            
    def getCommands(self):
        if self.parser.has_option("mai-bot-cfg", "commands"):
            return str(self.parser.get("mai-bot-cfg", "commands")).split(",")
        else:
            return ["nearest", "middle-left", "far-left"]
    
    def getTokenOrder(self):
        if self.parser.has_option("mai-bot-cfg", "token-order"):
            return str(self.parser.get("mai-bot-cfg", "token-order")).split(",")
        else:
            return ["0","1","2","3","4","5"]
    
    def getDebug(self):
        if self.parser.has_option("mai-bot-cfg", "debug"):
            return self.parser.getboolean("mai-bot-cfg", "debug")
        else:
            return False
    #def getStart(self):
     #   if self.parser.has_option("mai-bot-cfg", "start"):
      #      return self.parser.get("mai-bot-cfg", "start")
       # else:
        #    return "nearest"
    
    #def getMaxHeight(self):
     #   if self.parser.has_option("mai-bot-cfg", "max-height"):
      #      return self.parser.getint("mai-bot-cfg", "max-height")
       # else:
        #    return 4
        
            
    def debugMsg(self, message):
        if self.debug != None:
            self.debug.printMsg(message, self)
    
    def __str__(self):
        return "ConfigReader"