"""database functions

Adds database functions for the server to use

This library adds easy to use functions to store message
data in a database for (somewhat) persistent data storage.
"""

import sqlite3
import dataclasses
from time import time

@dataclasses.dataclass(frozen=True)
class Database:
    """
    This class serves as a de facto database providing functions
    for simple access to the database.
    """
    db : str


    def __dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def init_db(self):
        """
        Initalizes the database

        Checks if all the needed tables exist or creates them if not.
        """

        #sql = "CREATE TABLE IF NOT EXISTS ? ?"
        sql = "CREATE TABLE IF NOT EXISTS message_history (message text, author text, receipient text, date integer)"

        try:
            con = sqlite3.connect(self.db)
            cur = con.cursor()

            #cur.execute(sql, ("message_history", "(message text, author text, receipient text, date integer)"))
            cur.execute(sql)
            con.commit()

        finally:
            con.close()


    def write_message(self, message, author, receipient, date):
        """
        Writes the current message to the message history
        """
        
        sql = "INSERT INTO message_history VALUES (?,?,?,?)"

        try:
            con = sqlite3.connect(self.db)
            cur = con.cursor()

            cur.execute(sql, (message, author, receipient, date))
            con.commit()

        finally:
            con.close()

    def get_message(self):
        """
        Gets the messages from the database
        """
        
        sql = "SELECT *FROM message_history ORDER BY date(date) DESC"
        
        try:
            con = sqlite3.connect(self.db)
            con.row_factory = self.__dict_factory
            cur = con.cursor()

            cur.execute(sql)

            result = cur.fetchall()

        finally:
            con.close()
            return result
    


