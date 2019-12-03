# importing module 
import sqlite3 
  
# connecting to the database  
connection = sqlite3.connect("myTable.db") 
  
# cursor  
crsr = connection.cursor() 
  
sql_command = """
	CREATE TABLE Book(  
		BookID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,  
		BookName VARCHAR(50),  
		BookAuthor VARCHAR(40)  
		);
	"""
crsr.execute(sql_command) 

#DATE is of format : "YYYY-MM-DD"
sql_command = """
	CREATE TABLE Rental(
		RentalID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		CustomerID INTEGER NOT NULL,
		BookID INTEGER NOT NULL,
		RentalDate DATE NOT NULL,
		DueDate DATE NOT NULL,
		ReturnDate DATE,
		FOREIGN KEY(CustomerID) REFERENCES Customer,
		FOREIGN KEY(BookID) REFERENCES Book
		);

	"""
crsr.execute(sql_command)

sql_command = """
	CREATE TABLE Customer(
		CustomerID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		CustomerName VARCHAR(40),
		CustomerEmail VARCHAR(50),
		CustomerPhone VARCHAR(15)
		);
	"""
crsr.execute(sql_command)

sql_command = """
	CREATE TABLE Inventory(
		BookID INTEGER NOT NULL,
		BookCount INTEGER DEFAULT 0,
		FOREIGN KEY(BookID) REFERENCES Book
		);

	"""
crsr.execute(sql_command)

# To save the changes in the files. Never skip this.  
# If we skip this, nothing will be saved in the database. 
connection.commit() 
  
# close the connection 
connection.close() 
