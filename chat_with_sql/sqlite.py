import sqlite3

# connect to sqlite
connection = sqlite3.connect("student.db")

# Now Create a cursor object to insert records and create table
cursor = connection.cursor()

# Create Table
table_info = """
create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT)
"""

cursor.execute(table_info)

# insert Data

cursor.execute('''Insert Into STUDENT values('Vishal', 'Developer', 'A', 95)''')
cursor.execute('''Insert Into STUDENT values('Ajay', 'Devops', 'B', 100)''')
cursor.execute('''Insert Into STUDENT values('Zishan', 'QA', 'A', 99)''')
cursor.execute('''Insert Into STUDENT values('Ankur', 'Devops', 'B', 90)''')
cursor.execute('''Insert Into STUDENT values('Prashant', 'Devops', 'D', 45)''')
cursor.execute('''Insert Into STUDENT values('Vibhu', 'QA', 'A', 90)''')
cursor.execute('''Insert Into STUDENT values('Riya', 'Developer', 'D', 78)''')
cursor.execute('''Insert Into STUDENT values('Piya', 'QA', 'B', 78)''')
cursor.execute('''Insert Into STUDENT values('Tiya', 'Devops', 'C', 88)''')
cursor.execute('''Insert Into STUDENT values('Raj', 'Devops', 'C', 89)''')
cursor.execute('''Insert Into STUDENT values('Mohan', 'Developer', 'A', 90)''')
cursor.execute('''Insert Into STUDENT values('Adi', 'QA', 'C', 95)''')
cursor.execute('''Insert Into STUDENT values('Jay', 'QA', 'A', 95)''')

print("Inserted data: ")
data = cursor.execute("Select * from STUDENT")
for row in data:
    print(row)

connection.commit()
connection.close()