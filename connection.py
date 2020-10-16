import pyodbc

class Connection:
    def __init__(self,conn,query):
        self.conn = conn
        self.query = query

    @staticmethod    
    def read (conn,query):
        cursor = conn.cursor()
        cursor.execute(query)
        return list(cursor.fetchall())
    
    @staticmethod
    def add (conn,query):
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()