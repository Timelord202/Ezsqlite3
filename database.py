import time
import sqlite3
import keyboard
from pathlib import Path

delay = 0.1

print(
'''
############################
q - quit the program (Note: if you don't press q, and the program doesn't close automatically, your changes won't be saved)
s - store file
r - retrieve file
l - list files in database
d - delete file from database
############################
'''
)

def store():
    
    PATH = input('Enter absolute file path: ')
    with open(PATH, 'rb') as f:
        file_data = f.read()
    path_inst = Path(PATH)
    path_name = path_inst.stem + path_inst.suffix

    c.execute('CREATE TABLE IF NOT EXISTS files ( file_name TEXT, file BLOB );')
    c.execute('INSERT INTO files (file_name, file) VALUES (?, ?);', (path_name, file_data))


def retrieve():

    PATH = input('File you would like to retrieve?: ')
    OUT_PATH = input('Where would you like to store the file? ')

    c.execute('SELECT * FROM files WHERE file_name=(?)', [PATH])
    file_data = c.fetchone()[1]

    with open(f'{OUT_PATH}\{PATH}', 'wb') as f:
        f.write(file_data)

    c.execute('DELETE FROM files WHERE file_name=(?)', [PATH])


def list_files():
    
    c.execute('SELECT file_name FROM files')
    name_list = set([row for row in c])

    if len(name_list):
        print(name_list)
    else:
        print('No files in database')

    time.sleep(delay)

def delete_files():

    PATH = input('File to delete: ')
    c.execute('DELETE FROM files WHERE file_name=(?)', [PATH])


conn = sqlite3.connect('database.db')
c = conn.cursor()

while True:
    try:
        if keyboard.is_pressed('s'):
            store()
    except Exception as exec:
        print(exec)

    if keyboard.is_pressed('r'):
        retrieve()

    if keyboard.is_pressed('l'):
        list_files()

    if keyboard.is_pressed('d'):
        delete_file()

    if keyboard.is_pressed('q'):
        break

conn.commit()
conn.close()