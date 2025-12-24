import sqlite3
cn=sqlite3.connect("data.db")
cur=cn.cursor()
# cur.execute("CREATE TABLE users")
# cn.commit()