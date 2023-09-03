from flask import session
import sqlite3
class Db(object):
    def connect_db(self):
        path = "/home/gopi/Documents/Flask/project_1/Database_1/db_1"
        connect = sqlite3.connect(path)
        cursor = connect.cursor()
        return cursor,connect
    
    def create_registration_table(self):
        cursor,connection = self.connect_db()
        query = f""" CREATE TABLE "Users Registration"(
                            sid	TEXT,
                            name TEXT,
                            email TEXT UNIQUE,
                            phone TEXT,
                            password TEXT,
                            role TEXT,
                            PRIMARY KEY(sid)
                        )"""
        cursor.execute(query)
        connection.close()
    
    def get_log_query(self,msg,error):
        query = f""" INSERT INTO Log(message,error)  
                            VALUES('{msg}','{error}') """
        return query
    
    def create_log_table(self):
        cursor,connection = self.connect_db()
        query = f""" CREATE TABLE "Log" (
                            "sid" INT AUTO_INCREMENT,
                            "message" TEXT,
                            "error"	TEXT
                        )"""
        cursor.execute(query)
        connection.close()
