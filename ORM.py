import LibraryBook as LB
from Catelog import Catelog

from prettytable import PrettyTable as PT

# Driver Code

britishLibrary = Catelog()
print("British Library Created...\n")

# retrieve the book objects and user objects once the application is started from db
britishLibrary.retrieveUserObjects()
print("User Objects Retrieved...\n")
britishLibrary.retrieveBookObjects()
print("Book Objects Retrieved...\n")

booksInLibrary = britishLibrary.bookDict
registeredUsers = britishLibrary.userDict



op = "Y"
while op == "Y":

	choice = int(input("Choose an action:\n1 - Lend Book\n2 - Return Book\n3 - Check Borrowed Status\n4 - Books Borrowed By a User\n5 - Add Book\n6 - Remove Book\n7 - Register New User\n8 - Delete User\n9 - List Users by Name\n10 - List All Users\n11 - List All Books\n12 - Exit\n\n-->  "))

	if choice == 1:		# Lend Book
		bookID = int(input("Enter the Book ID: "))
		userID = int(input("Enter the user ID: "))
		book = booksInLibrary[bookID]
		user = registeredUsers[userID]
		try:
			result = book.lend(user)
			print(result)
		except LB.BookLimitReachedError as error:
			print(error.getMessage)

	elif choice == 2:   # Return Book
		bookID = int(input("Enter the Book ID: "))
		userID = int(input("Enter the User ID: "))
		book = booksInLibrary[bookID]
		user = registeredUsers[userID]

		bookState = input("Is the book in a acceptable state: [Y/n]")
		if bookState == "Y":
			result = book.acceptReturn(user)
		else:
			# remove book from the catelog
			britishLibrary.removeBook(bookID)
			result = "Book Damaged. Please Replace Book."
		print(result)

	elif choice == 3:   # Check Borrowed State 
		bookTitle = input("Enter the title of the book: ")
		books = britishLibrary.checkIfBookIsBorrowed(bookTitle)
		table = PT(["Book ID", "Borrowed State", "User ID", "First Name", "Last Name"])
		for bookID in books:
			book = books[bookID]
			print(book)
			borrowedState = book[0]
			user = book[1]
			if user == None:
				userID = None
				userFirstName = None
				userLastName = None
			else:
				userID = user.userID
				userFirstName = user.firstName
				userLastName = user.lastName
			table.add_row([bookID, borrowedState, userID, userFirstName, userLastName])
		print(table)

	elif choice == 4:   # Books Borrowed By User
		userID = int(input("Enter the User ID: "))
		user = registeredUsers[userID]
		booksBorrowed = user.booksBorrowed() # list of objects
		
		table = PT(["Book ID", "Title", "Author", "Year Published", "Pages"])
		for book in booksBorrowed:
			bookID = book.bookID
			title = book.title
			author = book.author
			yearPublished = book.yearPublished
			pages = book.pages
			table.add_row([bookID, title, author, yearPublished, pages])
		print(table)
		
	elif choice == 5:   # Add Book
		title = input("Enter the Title: ")
		author = input("Enter the author's name: ") 
		yearPublished = int(input("Enter the year it was Published: "))
		pages = int(input("Enter the Number of Pages: "))
		britishLibrary.addBook(title, author, yearPublished, pages)
	
	elif choice == 6:   # Remove Book
		bookID = int(input("Enter the book ID: "))
		britishLibrary.removeBook(bookID)
	
	elif choice == 7:   # Register New User
		firstName = input("First Name: ")
		lastName = input("Last Name: ")
		address = input("Adrress: ")
		email = input("Email: ")
		britishLibrary.addUser(firstName, lastName, address, email)
	
	elif choice == 8:   # Delete User
		userID = int(input("Enter the User ID: "))
		britishLibrary.removeUser(userID)
	
	elif choice == 9:   # Get List of User By Name
		name = input("Enter First Name: ")
		users = britishLibrary.getListOfUsersByName(name)    # list of objects
		table = PT(["User ID", "First Name", "Last Name", "Address", "Email"])
		for idx in range(len(users)):
			user = users[idx]
			userID = user.userID
			firstName = user.firstName
			lastName = user.lastName
			address = user.userAddress
			email = user.userEmail
			table.add_row([userID, firstName, lastName, address, email])
		print(table)

	elif choice == 10:  # Get List of all the Users
		table = PT(["User ID", "First Name", "Last Name", "Address", "Email"])
		for userID in registeredUsers:
			user = registeredUsers[userID]
			userID = user.userID
			firstName = user.firstName
			lastName = user.lastName
			address = user.userAddress
			email = user.userEmail
			table.add_row([userID, firstName, lastName, address,email])
		print(table)

	elif choice == 11:  # Get List of all the Books
		table = PT(["Book ID", "Title", "Author", "Year Published", "Number of Pages", "Borrowed State", "User ID", "User First Name", "User Last Name"])
		for bookID in booksInLibrary:
			book = booksInLibrary[bookID]   #object
			bookID = book.bookID
			title = book.title
			author = book.author
			yearPublished = book.yearPublished
			pages = book.pages
			borrowedState = book.borrowedState
			if book.user == None:  # check if book has been borrowed
				userID = None
				userFirstName = None
				userLastName = None
			else:
				userID = book.user.userID
				userFirstName = book.user.firstName
				userLastName = book.user.lastName
			table.add_row([bookID, title, author, yearPublished, pages, borrowedState, userID, userFirstName, userLastName])
		print(table)

	elif choice == 12:	
		op = "n"