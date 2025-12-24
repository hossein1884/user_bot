import sqlite3
cn=sqlite3.connect("data.db")
cur=cn.cursor()
result=cn.execute("select 1 from users where id=?",(176095541,)).fetchone())
# print(cn.execute("select * from users").fetchone())