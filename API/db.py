import pymysql

def get_db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="labticketing",
        autocommit=False,
        cursorclass=pymysql.cursors.DictCursor
    )