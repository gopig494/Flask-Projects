import sqlite3
con=sqlite3.connect("\\home\\gopi\\Documents\\projects\\flask_projects\\contact.db")
cursor=con.cursor()
cursor.execute("""create table addressbook(Sno integer primary key autoincrement,
				FirstName varchar(20) not null,LastName varchar(20) null,
				MobileNumber integer unique not null,OfficeNumber integer not null,mailid text not null unique,address text not null); """)
con.commit()
con.close()

print("Table Created Successfully")