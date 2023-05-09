import mysql.connector
import unittest
from enum import Emun

#singleton design
class DBUtils:
    __instance = None

    @staticmethod
    def getInstance():

        if DBUtils.__instance == None:
            DBUtils()
        return DBUtils.__instance


    def __init__(self):

        if DBUtils.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DBUtils.__instance = self
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1123581321",
                database="Library"
            )

    
    
    def executeQuery(self, queryType, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        if queryType == "fetch":
            return cursor.fetchall()
        elif queryType == "update":
            self.connection.commit()
            return

    

class TestGetInstance(unittest.TestCase):
    def runTest(self):
        instance1 = DBUtils.getInstance()
        with self.assertRaises(Exception):
            instance2 = DBUtils()

if __name__ == '__main__':
    unittest.main()


























# def executeUpdateQuery(self, query):
    #     cursor = self.connection.cursor()
    #     cursor.execute(query)
    #     self.connection.commit()
    #     return


    # def executeFetchQuery(self, query):
    #     cursor = self.connection.cursor()
    #     cursor.execute(query)
    #     return cursor.fetchall()



# dbConn = MySQLDatabase.getInstance()
# # result = LBCatelogDB.executeQuery("SELECT * FROM mytable")
# # print(result)

# # make the instane a global variable so that any file in the program can access it
# import sys
# sys.module[__name__].dbConn = dbConn

