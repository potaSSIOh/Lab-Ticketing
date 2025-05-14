import pymysql

try:
    db = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="labticketing",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Connection successful")
except pymysql.MySQLError as e:
    print(f"Error connecting to MySQL Platform: {e}")
