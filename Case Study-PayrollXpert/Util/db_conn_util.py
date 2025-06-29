import mysql.connector
from configparser import ConfigParser

def get_connection():
    config = ConfigParser()
    config.read('db_config.ini')
    db = config['mysql']

    return mysql.connector.connect(
        host=db['host'],
        port=int(db['port']),
        user=db['user'],
        password=db['password'],
        database=db['database']
    )