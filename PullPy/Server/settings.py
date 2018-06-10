''' File ove inserire tutte le info di settaggio utili '''
''' File where insert all the infos for the settings '''

import os
from binascii import hexlify

DB_PATH = os.getcwd()+"\\DBs\\"
DB_NAME = 'db.db'

USER = '@Gorate'
PASSWD = hexlify(USER.encode()).decode() #40476f72617465

PORT = 8080

PATH_API = os.getcwd()+"\\API\\"
PATH_CC = os.getcwd()+"\\C&C\\"

SQL_KEYWORDS = ['SELECT', 'FROM', 'UNION', ';', '-- -', '#', 'SLEEP', '\'', '\"']