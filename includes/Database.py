import mysql.connector as mysql

class Database:
    def __init__(self, database_name):
        self.__database_name = database_name

    # ------------------------------------------
    @property
    def server(self, server):
        return self.__server

    @server.setter
    def server(self, server):
        self.__server = server

    # ------------------------------------------
    @property
    def username(self, username):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    # ------------------------------------------
    @property
    def password(self, password):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    # ------------------------------------------
    @property
    def table_name(self, table_name):
        return self.__table_name

    @table_name.setter
    def table_name(self, table_name):
        self.__table_name = table_name

    # ------------------------------------------
    def create_database(self):
        db = mysql.connect(
            host = self.__server,
            user = self.__username,
            password = self.__password
            )

        cursor = db.cursor()
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS `{self.__database_name}`')

        return f'Database {self.__database_name} has been created'

    # ------------------------------------------
    def __create_connection(self):
        db = mysql.connect(
            host = self.__server,
            user = self.__username,
            password = self.__password,
            database = self.__database_name
            )

        self.__db = db

    # ------------------------------------------
    def create_table_fields(self, fields):
        self.__create_connection()
        cursor = self.__db.cursor()

        query = f'CREATE TABLE IF NOT EXISTS `{self.__table_name}` ('
        for column_name, data_type in fields.items():
            query += f'`{column_name}` {data_type},'
        query = query.rstrip(',')
        query += ')'

        cursor.execute(query)

        return f'Table {self.__table_name} has been created'

    # ------------------------------------------
    def show_all_databases(self):
        cursor = self.__db.cursor()
        cursor.execute('SHOW DATABASES')
        databases = cursor.fetchall()

        return databases

    # ------------------------------------------
    def show_current_database_tables(self):
        cursor = self.__db.cursor()
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()

        return tables

    # ------------------------------------------
    def show_current_table_fields(self):
        cursor = self.__db.cursor()
        cursor.execute(f'DESC `{self.__table_name}`')
        fields = cursor.fetchall()

        return fields

    # ------------------------------------------
    def show_current_table_fields_desc(self):
        cursor = self.__db.cursor()
        cursor.execute(f'SELECT * FROM `{self.__table_name}`')

        return cursor.description


def main():
    pass
    # db = Database('python_crud_oop')
    # db.server = 'localhost'
    # db.username = 'root'
    # db.password = 'root'
    # db.create_database()

    # db.table_name = 'customer1'
    # db.create_table_fields({
    #     'first_name' : 'VARCHAR(255)',
    #     'last_name' : 'VARCHAR(255)',
    #     'zipcode' : 'INT(10)',
    #     'price_paid' : 'DECIMAL(10, 2)',
    #     'user_id' : 'INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY'
    #     })

    # print(db.show_all_databases())
    # print(db.show_current_database_tables())
    # print(db.show_current_table_fields())
    # print(db.show_current_table_fields_desc())

if __name__ == '__main__':
    main()
