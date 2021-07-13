import mysql.connector


class Database:

    def __init__(self):
        # Create a connection
        self.__conn = mysql.connector.connect(
            user='user', password='userpass', host='127.0.0.1', database='app_db'
        )
        # Create a cursor object
        self.__cursor = self.__conn.cursor()

    def execute(self, query, data):
        try:
            # Execute the SQL
            self.__cursor.execute(query, data)

            # Retrieve result
            result = self.__result(query)

            # Commit changes in the database
            self.__conn.commit()

            return result

        except:
            # Roll back in case of error
            self.__conn.rollback()

    def __result(self, query):
        if query.startswith('SELECT'):
            return self.__cursor.fetchall()
        elif query.startswith('INSERT INTO'):
            return self.__cursor.rowcount
        else:
            return ''

    def __del__(self):
        self.__conn.close()
