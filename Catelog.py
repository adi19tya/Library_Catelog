from DBUtils import DBUtils 
from DBUtils import SQLActions
from User import User
from LibraryBook import LibraryBook

class Catelog:

	def __init__(self):
		currentUserID = 0
		currentBookID = 0
		self.userDict = {}
		self.bookDict = {}
		

	def getListOfUsersByName(self, firstName):
		usersList = []
		for userID in self.userDict:
			if userID.firstName == firstName:
				user = self.userDict[userID]
				usersList.append(user)
		return usersList


	def checkIfBookIsBorrowed(self, title):
		#get list of ids books with the given name and thier borrowed status
		booksWithSameName = {}
		for bookID in self.bookDict:
			book = self.bookDict[bookID]
			if book.title == title:
				booksWithSameName[bookID] = [book.borrowedState, book.user]
		return booksWithSameName


	def addBook(self, title, author, yearPublished, pages):
			# create a library book object
			self.bookDict[self.currentBookID] = LibraryBook(self.currentBookID, title, author, yearPublished, pages)

			queryType = "update"
			query = "INSERT INTO LIBRARY_BOOK (book_id, title, author, year_published, pages) VALUES ( '" + str(self.currentBookID) + "', '" + title + "', '" + author + "', '" + str(yearPublished) + "', '" + str(pages) + "');"
			print(query)
			DBUtils.getInstance().executeQuery(queryType, query)
			self.currentBookID += 1
	
		
	def removeBook(self, bookID):
		del self.bookDict[bookID]

		queryType = "update"
		query = "DELETE FROM LIBRARY_BOOK WHERE book_id= " + str(bookID)
		DBUtils.getInstance().executeQuery(queryType, query)
		

	def addUser(self, firstName, lastName, userAddress, userEmail):
			self.userDict[self.currentUserID] = User(self.currentUserID, firstName, lastName, userAddress, userEmail)

			queryType = "update"
			query = "INSERT INTO USER (user_id, first_name, last_name, address, email) VALUES ('" + str(self.currentUserID) + "', '" + firstName + "', '" + lastName + "', '" + userAddress + "', '" + userEmail + "');"
			print(query)
			DBUtils.getInstance().executeQuery(queryType, query)
			self.currentUserID += 1
			
		
	def removeUser(self, userID):

		queryType = "update"
		query = "DELETE FROM USER WHERE user_id= " + str(userID)
		DBUtils.getInstance().executeQuery(queryType, query)
		del self.userDict[userID]
		

	def retrieveUserObjects(self):
		queryType = "fetch"
		query = "SELECT * FROM LIBRARY_BOOK"
		result = DBUtils.getInstance().executeQuery(queryType, query)
		print(result)
		for i in range(len(result)):
			# 0 - book_id, 1 - title, 2 - author, 3 - year_published, 4 - pages, 5 - borrowed_state, 6 - user_id
			bookId = result[i][0]
			row = result[i]
			book = LibraryBook(row[0],row[1],row[2],row[3],row[4], row[5])
			self.bookDict[bookId] = book
			if book.borrowedState == "Borrowed":  # if the borrowed state is borrowed, then add the book object to user's borrowed List	
				# add book object to borrowed list of the user 
				userID = row[6]
				user = self.userDict[userID]
				user.borrowedBookList.append(book)
				# update the user ID of the book object to given user ID
				book.user = user

		lastBookID = max(self.bookDict.keys())
		self.currentBookID = self.bookDict[lastBookID].bookID + 1

					
	def retrieveBookObjects(self):
		queryType = "fetch"
		query = "SELECT * FROM USER"
		result = DBUtils.getInstance().executeQuery(queryType, query)
		print(result)
		for i in range(len(result)):
			# 0 - user_id, 1 - first_name, 2 - last_name, 3 - address, 4 - email
			self.userDict[result[i][0]] =  User(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4])
		lastUserID = max(self.userDict.keys())
		self.currentUserID = self.userDict[lastUserID].userID + 1
		
			