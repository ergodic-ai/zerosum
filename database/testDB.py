from datetime import datetime

from database.pgresDB import Database

def create_tables(tableName:str, db2:Database):
    query = '''CREATE TABLE {} (state VARCHAR(100),timestamp VARCHAR(100) PRIMARY KEY, gameInstance INTEGER, score VARCHAR(100) );'''.format(tableName)
    db2.execute_command(query)

def update_table(tableName:str, gameInstance: int, state:str, score: str, db2:Database):
    curTime = datetime.now().strftime('%H:%M:%S')
    query = '''INSERT INTO {} (state, timestamp, gameInstance, score) VALUES ({}, {},{},{});'''.format(tableName, state, "\'"+curTime+"\'", gameInstance, score)
    print(query)
    db2.execute_command(query)

db = Database("yourdatabase","yourusername","yourpassword")
# create_tables("testplayertable", db)
update_table("testplayertable", 0, "'some state'", "'some score'", db)

db.execute_command('''SELECT * from test;''')
