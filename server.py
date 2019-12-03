"""
SERVER FUNCTIONS:

0. The MAIN Function which handles all the other functions

1. Inserting books
2. Removing books
3. Incrementing Inventory's BookCount
4. Decrementing Inventory's BookCount
5. Managing Rentals
6. Add Customer
7. Find BookName which belongs to BookID

"""

import sqlite3
import socket
import time

#1
def add_book(BookName, BookAuthor):
	connection = sqlite3.connect("myTable.db") 
	crsr = connection.cursor() 
	
	#First we add the Book's details into the Book Table
	sql_command = """
		INSERT INTO Book (BookName, BookAuthor)
		VALUES (?1 , ?2)
		;
	"""
	crsr.execute(sql_command, [BookName, BookAuthor])
	connection.commit()

	"""
	Now we have to add an entry in the Inventory Table
	For this we require the BookID of the newly added book
	"""

	sql_command = """
		SELECT BookID
		FROM Book
		WHERE BookName = ?1 AND BookAuthor = ?2
		;
	"""
	crsr.execute(sql_command, [BookName, BookAuthor])
	BookID = crsr.fetchone()	

	sql_command = """
		INSERT INTO Inventory (BookID)
		VALUES (?1)
		;
	"""
	crsr.execute(sql_command, BookID)		
	connection.commit()

	connection.close()

#2
def remove_book(BookID):
	connection = sqlite3.connect("myTable.db")
	crsr = connection.cursor()

	"""
	Removing books is needed when the Rental agency decides to stop issuing a particular book
	There might be many reasons for doing so.
	Eitherways, in such a situation we need not check anything much.
	We could check to see if any returns are due. 
	In case of a due return, removing the book from the db might need to be delayed.
	"""

	sql_command = """
		SELECT COUNT(*) FROM Rental 
		WHERE BookID = ?1 AND DueDate > DATE('now')
		;
	"""
	crsr.execute(sql_command, BookID)
	
	if int(crsr.fetchone()[0]) > 0:
		return 0

	else:
		#First we have to remove it from out Book Table
		sql_command = """
			DELETE FROM Book 
			WHERE BookID = ?1
			;
		"""
		crsr.execute(sql_command, BookID)
		connection.commit() 
		return 1
		
		"""
		Note : We do not remove the other records of the Book as
		in the other tables we maintain vital records which might be
		required to track down earlier transactions, assess how much
		inventory space the old books are taking up etc.
		"""
	

#3a
def inventory_increment(BookID, count):
	connection = sqlite3.connect("myTable.db") 
	crsr = connection.cursor() 
	
	#We first check if BookID exists in Book
	sql_command = """
		SELECT *
		FROM Book
		WHERE BookID = ?1
		;
	"""
	crsr.execute(sql_command, BookID)
	result = crsr.fetchall()	
	
	if len(result) > 0:
		sql_command = """
			UPDATE Inventory 
			SET BookCount = (BookCount + ?1) 
			WHERE BookID = ?2 
			;
		"""
		crsr.execute(sql_command, [count, BookID])
		connection.commit()	
		connection.close()
		print("TABLE UPDATED")
		return 1
	else:
		connection.close()
		print("TABLE UNCHANGED")
		return 0

		
#3b
def inventory_decrement(BookID, count):
	connection = sqlite3.connect("myTable.db") 
	crsr = connection.cursor() 
	
	#We first check if BookID exists in Book
	sql_command = """
		SELECT *
		FROM Book
		WHERE BookID = ?1
		;
	"""
	crsr.execute(sql_command, BookID)
	result = crsr.fetchall()	
	
	if len(result) > 0:
		sql_command = """
			UPDATE Inventory 
			SET BookCount = (BookCount - ?1) 
			WHERE BookID = ?2 
			;
		"""
		crsr.execute(sql_command, [count, BookID])
		connection.commit()	
		connection.close()
		print("TABLE UPDATED")
		return 1
	else:
		connection.close()
		print("TABLE UNCHANGED")
		return 0

#4
def add_customer(CustomerName, CustomerEmail, CustomerPhone):
	connection = sqlite3.connect("myTable.db") 
	crsr = connection.cursor() 

	sql_command = """
		INSERT INTO Customer (CustomerName, CustomerEmail, CustomerPhone)
		VALUES (?1, ?2, ?3)
		;
	"""
	crsr.execute(sql_command, [CustomerName, CustomerEmail, CustomerPhone])
	connection.commit()
	connection.close()
	return 1

#5
def add_rental(CustomerID, BookID, RentalDate):
	connection = sqlite3.connect("myTable.db") 
	crsr = connection.cursor() 


	#A rental can only be created if there is atleast one book in the inventory
	sql_command = """
		SELECT BookCount
		FROM Inventory
		WHERE BookID = ?1
		;
	"""
	crsr.execute(sql_command, BookID)
	x = crsr.fetchall()[0]
	print(x)

	if int(x[0]) > 0 :
		sql_command = """
			INSERT INTO Rental (CustomerID, BookID, RentalDate, DueDate)
			VALUES (?1, ?2, ?3, Date(?3,'+14 day'))
			;
		"""
		crsr.execute(sql_command, [CustomerID, BookID, RentalDate])
		connection.commit()
		#We must also reduce the BookCount from the inventory
		inventory_decrement(BookID, 1)
		connection.close()
		return 1
	else:
		return 0

#6
def accept_return(RentalID, ReturnDate):
	#First we check if the Rental exists
	connection = sqlite3.connect("myTable.db")
	crsr = connection.cursor()

	sql_command = """
		SELECT * 
		FROM Rental
		WHERE RentalID = ?1
		;
	"""
	crsr.execute(sql_command, RentalID)
	x = crsr.fetchall()
	
	if len(x) > 0:
		#This means that the RentalID exists
		sql_command = """
			UPDATE RENTAL 
			SET ReturnDate = ?1
			WHERE RentalID = ?2
			;
		"""
		crsr.execute(sql_command, [ReturnDate, RentalID])
		connection.commit()

		sql_command = """
			SELECT BookID
			FROM Rental 
			WHERE RentalID = ?1
			;	
		"""

		crsr.execute(sql_command, RentalID)
		BookID = crsr.fetchall()[0]

		#We must also increment the Inventory's BookCount by 1
		count = 1
		inventory_increment(BookID, count)
		connection.close()
		return 1
	
	else:
		#The RentalID does not exist
		connection.close()
		return 0

#7
def DisplayBook():
	connection = sqlite3.connect("myTable.db")
	crsr = connection.cursor()

	sql_command = """
		SELECT * 
		FROM Book
		;
	"""
	crsr.execute(sql_command)
	result = ""

	for row in crsr.fetchall():
		result = result + str(row) + '\n'
	connection.close()
	return result

#8
def DisplayInventory():
	connection = sqlite3.connect("myTable.db")
	crsr = connection.cursor()

	sql_command = """
		SELECT * 
		FROM Inventory
		;
	"""
	crsr.execute(sql_command)
	result = ""
	for row in crsr.fetchall():
		result = result + str(row) + '\n'
	
	result = result + '\n'
	connection.close()
	return result

#9
def DisplayCustomer():
	connection = sqlite3.connect("myTable.db")
	crsr = connection.cursor()

	sql_command = """
		SELECT * 
		FROM Customer
		;
	"""
	crsr.execute(sql_command)
	result = ""
	for row in crsr.fetchall():
		result = result + str(row) + '\n'

	result = result + '\n'
	connection.close()
	return result

#10
def DisplayRental():
	connection = sqlite3.connect("myTable.db")
	crsr = connection.cursor()
	
	sql_command = """
		SELECT * 
		FROM Rental
		;
	"""
	crsr.execute(sql_command)
	result = ""
	for row in crsr.fetchall():
		result = result + str(row) + '\n'

	result = result + '\n'
	connection.close()
	return result


	
def MainApp():

	BUFSIZE = 4096
	ServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	port = 33333
	ServerSock.bind(('10.20.206.29',port))
	ServerSock.listen(5)

	MainBody = "Book Rental Management System\n\nMENU:\n1.  Inserting books\n2.  Removing books\n3.  Modify Inventory's BookCount\n4.  Add Customer\n5.  Add Rental\n6.  Accept Return\n7.  Display Book Table\n8.  Display Inventory Table\n9.  Display Customer Table\n10. Display Rental Table\n\n0.  -----SHUT DOWN SERVER-----\n"

	while True:
		ClientSock, addr = ServerSock.accept()
		print("CONNECTED TO CLIENT : ", addr)
		#ClientSock.send(bytes(MainBody, 'utf-8'))
		while True:
			#ClientSock.send(MainBody.encode())
			choice = ClientSock.recv(24).decode()
			print(choice)
		
			choice = int(choice)	
			if choice == 0:
				ClientSock.send("SERVER SHUTDOWN")
				exit(0)		
			if choice == 1:
				ClientSock.send("INSERT_BOOK:\nEnter the Book's Name : ".encode())
				BookName = ClientSock.recv(BUFSIZE).decode()
				ClientSock.send("Enter the Book's Author's Name : ".encode())
				BookAuthor = ClientSock.recv(BUFSIZE).decode()
				add_book(BookName, BookAuthor)
				ClientSock.send('0'.encode())
				buf = ClientSock.recv(BUFSIZE).decode()
				ClientSock.send("Book added successfully!\n\n".encode())
			
			elif choice == 2:
				ClientSock.send("REMOVE_BOOK:\nEnter the Book's ID : ".encode())
				BookID = ClientSock.recv(BUFSIZE).decode()
				result = remove_book(BookID)
				if result == 0:
					ClientSock.send('0'.encode())
					buf = ClientSock.recv(BUFSIZE).decode()
					ClientSock.send("Book could not be removed as one or more copies of the mentioned book is yet to be returned. Try removing it again once the books have been returned.\n".encode())
				else:
					#ClientSock.send('0'.encode())
					ClientSock.send('0'.encode())
					buf = ClientSock.recv(BUFSIZE).decode()
					ClientSock.send("Book removed successfully!\n\n".encode())

			elif choice == 3:
				ClientSock.send("INVENTORY UPDATER:\nEnter the Book's ID : ".encode())
				BookID = ClientSock.recv(BUFSIZE).decode()
				ClientSock.send("Increase(+) or Decrease(-) the Inventory count? : ".encode())
				choice = ClientSock.recv(BUFSIZE).decode()
				ClientSock.send("By how much? : ".encode())
				count  = ClientSock.recv(BUFSIZE).decode()
				if choice == '+':
					result = inventory_increment(BookID, count)
				elif choice == '-':
					result = inventory_decrement(BookID, count)
				else:
					ClientSock.send("INVALID CHOICE. TRY AGAIN.\n\n".encode())
					break

				if result == 0:
					ClientSock.send('0'.encode())
					buf = ClientSock.recv(BUFSIZE).decode()
					ClientSock.send("BookID DOES NOT EXIST IN THE DATABASE!\n\n".encode())
				elif result == 1:
					ClientSock.send('0'.encode())
					buf = ClientSock.recv(BUFSIZE).decode()
					ClientSock.send("INVENTORY UPDATED SUCCESFULLY!\n\n".encode())	

			elif choice == 4:
				ClientSock.send("Add Rental:\nEnter the CustomerID : ".encode())
				CustomerID = ClientSock.recv(BUFSIZE).decode()
				ClientSock.send("Enter the BookID : ".encode())
				BookID = ClientSock.recv(BUFSIZE).decode()
				ClientSock.send("Enter the Rental Date (YYYY-MM-DD) : ".encode())
				RentalDate = ClientSock.recv(BUFSIZE).decode()
				result = add_rental(CustomerID, BookID, RentalDate)
				if result == 0:
					ClientSock.send('0'.encode())
					buf = ClientSock.recv(BUFSIZE).decode()
					ClientSock.send(("NOT ENOUGH BOOKS IN THE INVENTORY. RENTAL COULD NOT BE ADDED. PLEASE TRY AGAIN LATER!\n\n").encode())
				elif result == 1:
					ClientSock.send('0'.encode())
					buf = ClientSock.recv(BUFSIZE).decode()
					ClientSock.send(("RENTAL ADDED SUCCESSFULLY!\n\n").encode())

			elif choice == 5:
				ClientSock.send("Add Customer:\nEnter the Customer's Name : ".encode())
				CustomerName = ClientSock.recv(BUFSIZE).decode()
				ClientSock.send("Enter the Customer's Email : ".encode())
				CustomerEmail = ClientSock.recv(BUFSIZE).decode()
				ClientSock.send("Enter the Customer's Phone Number : ".encode())
				CustomerPhone = ClientSock.recv(BUFSIZE).decode()
				result = add_customer(CustomerName, CustomerEmail, CustomerPhone)
				if result == 0:
					ClientSock.send('0'.encode())
					buf = ClientSock.recv(BUFSIZE).decode()
					ClientSock.send(("CUSTOMER COULD NOT BE ADDED. PLEASE TRY AGAIN!\n\n").encode())
				elif result == 1:
					ClientSock.send('0'.encode())
					buf = ClientSock.recv(BUFSIZE).decode()
					ClientSock.send(("CUSTOMER ADDED SUCCESSFULLY!\n\n").encode())

			elif choice == 6:
				ClientSock.send("Accept Return:\nEnter the RentalID : ".encode())
				RentalID = ClientSock.recv(BUFSIZE).decode()
				ClientSock.send("Enter the Return Date (YYYY-MM-DD) : ".encode())
				ReturnDate = ClientSock.recv(BUFSIZE).decode()
				result = accept_return(RentalID, ReturnDate)
				if result == 0:
					ClientSock.send('0'.encode())
					buf = ClientSock.recv(BUFSIZE).decode()
					ClientSock.send(("THE RENTALID DOES NOT EXIST. TRY AGAIN!\n\n").encode())
				elif result == 1:
					ClientSock.send('0'.encode())
					buf = ClientSock.recv(BUFSIZE).decode()
					ClientSock.send(("RETURN ACCEPTED SUCCESSFULLY!\n\n").encode())

			elif choice == 7:
				result = DisplayBook()
				ClientSock.send(result.encode())

			elif choice == 8:
				result = DisplayInventory()
				ClientSock.send(result.encode())

			elif choice == 9:
				result = DisplayCustomer()
				ClientSock.send(result.encode())
			
			elif choice == 10:
				result = DisplayRental()
				ClientSock.send(result.encode())

				

MainApp()
		
	




	
	
	
	
	

	
	
