from sqlite3 import connect

class DataBase(object):
    def __init__(self, dbname):
        self.conn = connect(dbname + '.db')
        self.cursor = self.conn.cursor()

    def createTable(self, tbname, attributes = []):
        command = 'CREATE TABLE IF NOT EXISTS ' + tbname + '(' 

        for at in range(len(attributes) - 1):
            command += attributes[at] + ','

        command += attributes[-1] + ');'

        self.cursor.execute(command)
        self.conn.commit()
        
    def insertInTable(self, table, values = [], attri=''):
        self.cursor.execute('INSERT INTO ' + table + '(' + attri + ')' + ' VALUES (' + ((len(values) -1) * '?,') +  '?);', values)
        self.conn.commit() 

    def readTable(self, table, att):
        return self.cursor.execute('SELECT ' + att + ' FROM ' + table).fetchall()

    def updateTable(self, table, att, new_values, id, valueid):
        command = 'UPDATE ' + table + ' SET ' 

        for at in range(len(att) - 1):
            command += f'{att[at]} = ?, '
        
        command += att[-1] + f' = ? WHERE {id} IS ?;' 
        
        new_values.append(valueid)
        self.cursor.execute(command, new_values)
        self.conn.commit()
    
    def deleteItemTable(self, table, id, id_value):
        self.cursor.execute('DELETE FROM ' + table + f' WHERE {id} = ?', (id_value,))
        self.conn.commit()