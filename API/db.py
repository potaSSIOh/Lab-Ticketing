import pymysql

db = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="labticketing",
    autocommit=True,
    cursorclass=pymysql.cursors.DictCursor
)