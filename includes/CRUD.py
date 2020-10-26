import mysql.connector as mysql

class CRUD:
    """refers to the four functions that are considered necessary to implement a persistent storage application."""
    def __init__(self, server, username, password, database_name, table_name, table_id):
        self.__server = server
        self.__username = username
        self.__password = password
        self.__database_name = database_name
        self.__table_name = table_name
        self.__table_id = table_id
        self.__create_connection()

    # ------------------------------------------
    def __create_connection(self):
        """Start by creating a connection to the database."""
        db = mysql.connect(
            host = self.__server,
            user = self.__username,
            password   = self.__password,
            database = self.__database_name
            )

        self.__db = db

    # ------------------------------------------
    def __query(self, sql, parameters=[]):
        cursor = self.__db.cursor(prepared=True,)
        cursor.execute(sql, parameters)
        self.__db.commit()

        return cursor.rowcount

    def find_all(self):
        """This method allows users to search and retrieve all records in the table."""
        cursor = self.__db.cursor(dictionary=True)
        cursor.execute(f'SELECT * FROM `{self.__table_name}`')
        rows = cursor.fetchall()

        return rows

    def find_all_by_order(self, field_name, order='ASC'):
        cursor = self.__db.cursor(dictionary=True)
        cursor.execute(f'SELECT * FROM `{self.__table_name}` ORDER BY `{field_name}` {order}')
        rows = cursor.fetchall()

        return rows

    def find_by_id(self, id):
        cursor = self.__db.cursor(dictionary=True)
        query = f'SELECT * FROM `{self.__table_name}` WHERE `{self.__table_id}` = %s'
        value = (id,)
        cursor.execute(query, value)
        row = cursor.fetchone()

        return row

    def total(self):
        cursor = self.__db.cursor(dictionary=True)
        cursor.execute(f'SELECT COUNT(*) FROM `{self.__table_name}`')
        total = cursor.fetchone()

        return total[0]

    def search_v1(self, column, keyword):
        query = f'SELECT * FROM `{self.__table_name}` WHERE `{column}` LIKE "%{keyword}%"'

        cursor = self.__db.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()

        return rows

    def search_by_order(self, column, field, keyword, order='ASC'):
        query = f'SELECT * FROM `{self.__table_name}` WHERE `{column}` LIKE "%{keyword}%" ORDER BY `{field}` {order}'

        cursor = self.__db.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()

        return rows

    # ------------------------------------------
    def delete(self, id):
        """This method allows users to remove records from a database that is no longer needed."""
        query = f'DELETE FROM `{self.__table_name}` WHERE `{self.__table_id}` = %s'
        value = (id,)

        return f'{self.__query(query, value)} record deleted'

     # ------------------------------------------
    def __create(self, record):
        """This method allows users to create a new record in the database."""
        placeholders = ['%s' for key in record.keys()]

        query = f'INSERT INTO `{self.__table_name}` ('
        for field in record.keys():
            query += f'`{field}`,'
        query = query.rstrip(',')
        query += ') VALUES ('
        for placeholder in placeholders:
            query += f'{placeholder},'
        query = query.rstrip(',')
        query += ')'

        values = []
        for value in record.values():
            values.append(value)

        return f'{self.__query(query, values)} record inserted'

    # ------------------------------------------
    def __update(self, record):
        """This method is used to modify existing records that exist in the database."""
        placeholders = ['%s' for key in record.keys()]
        fields = zip(record.keys(), placeholders)

        query = f'UPDATE `{self.__table_name}` SET '
        for field, placeholder, in fields:
            query += f'`{field}` = {placeholder},'
        query = query.rstrip(',')
        query += f' WHERE `{self.__table_id}` = %s'

        record['primary_key'] = record[self.__table_id]

        values = []
        for value in record.values():
            values.append(value)

        return f'{self.__query(query, values)} record updated'

    # ------------------------------------------
    def save(self, record):
        try:
            if record[self.__table_id] == '':
                record[self.__table_id] = None

            return self.__create(record)

        except Exception as error:
            return self.__update(record)


def main():
    crud = CRUD('localhost', 'root', 'root', 'python_crud_oop', 'customer1', 'user_id')

    # print(crud.save({
    #     'user_id' : '',
    #     'first_name' : 'test11',
    #     'last_name' : 'test11',
    #     'zipcode' : 2111,
    #     'price_paid' : 99,
    #     }))

    # print(crud.save({
    #     'user_id' : 69,
    #     'first_name' : '2222',
    #     'last_name' : '2222',
    #     'zipcode' : 2222,
    #     'price_paid' : 22,
    #     }))

    # for record in crud.find_all():
    #     print(record)

    # print(crud.find_all_by_id('70'))

    # print(crud.total())

    # print(crud.delete_record('25'))

    # for record in crud.find_all():
    #     print(record)

    # fields = [
    #     ('first_name', '%s', 'chie'),
    #     ('last_name', '%s', 'yamauchi'),
    #     ('zipcode', '%s', '2021'),
    #     ('price_paid', '%s', '150')
    #     ]

    # print(crud.update('22', fields))

    # for record in crud.find_all():
    #     print(record)

    # for record in crud.find_all_by_order('first_name'):
    #     print(record)

    # for record in crud.find_all_by_order('first_name', 'DESC'):
    #     print(record)


if __name__ == '__main__':
    main()