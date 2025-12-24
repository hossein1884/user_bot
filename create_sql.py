import sqlite3
cn=sqlite3.connect("data.db")
cur=cn.cursor()
sql="""CREATE TABLE users (
id varchar(20),
name varchar(50),
username varchar(50));"""
cur.execute(sql)
