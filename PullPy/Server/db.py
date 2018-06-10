''' File per la gestione e la visualizzazione del db '''
''' File for management and visualization of the db '''

import sqlite3
import sys
from settings import *

def main():
    option = sys.argv[1]
    if option == "init":
        init()
    elif option == "help":
        help()
    elif option == "del":
        delete()
    elif option == "show":
        show()
    else:
        print("\nCommand not found. Type `help` for see the aviable options")
        
def help():
    print("\n{0} usage: {0} <option>".format(sys.argv[0]))
    print("\t- help: show this help message")
    print("\t- show: show the content of the db")
    print("\t- init: initizlaize the db")
    print("\t- del: delete the db")
    
def init():
    with sqlite3.connect(DB_PATH+DB_NAME) as DB_CONN: 
        DB_EXE = DB_CONN.cursor()
        DB_EXE.execute("CREATE TABLE IF NOT EXISTS Bots (Key TEXT, User TEXT, Ip TEXT, Os TEXT, Enum TEXT, Geo TEXT)")
        DB_EXE.execute("CREATE TABLE IF NOT EXISTS Creds (Key TEXT, User TEXT, Passwd TEXT, Url TEXT)")
        DB_EXE.execute("CREATE TABLE IF NOT EXISTS Keys (Key TEXT, String TEXT)")
        DB_CONN.commit()
        DB_EXE.close()
        
def delete():
    with sqlite3.connect(DB_PATH+DB_NAME) as DB_CONN: 
        DB_EXE = DB_CONN.cursor()
        DB_EXE.execute("DROP TABLE IF EXISTS Bots")
        DB_EXE.execute("DROP TABLE IF EXISTS Creds")
        DB_EXE.execute("DROP TABLE IF EXISTS Keys")
        DB_CONN.commit()
        DB_EXE.close()
    
def show():
    with sqlite3.connect(DB_PATH+DB_NAME) as DB_CONN: 
        DB_EXE = DB_CONN.cursor()
        try:
            bots_content = DB_EXE.execute("SELECT * FROM Bots").fetchall()
            creds_content = DB_EXE.execute("SELECT * FROM Creds").fetchall()
            keys_content = DB_EXE.execute("SELECT * FROM Keys").fetchall()
            print("\nBots:\n")
            print(bots_content)
            print("\nCredentials:\n")
            print(creds_content)
            print("\nKeys:\n")
            print(keys_content)
        except sqlite3.DatabaseError:
            print("Impossible find the tables")
        finally:
            DB_CONN.commit()
            DB_EXE.close()
        
if __name__ == "__main__":
    main()