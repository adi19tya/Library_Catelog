from flask import Flask, jsonify, request

from DBUtils import DBUtils
from DBUtils import SQLActions
	
class BookLimitReachedError(Exception):

	BOOK_LIMIT_PER_USER = 7

	def __init__(self, user):
		self.user = user


	def getMessage(self):
		message = str(BookLimitReachedError.bookLimitPerUser) + " books have already been borrowed by " + self.user

class LibraryBook:

	def __init__(self, bookID, title, author, yearPublished, pages, borrowedState = "Available", user = None):
		self.bookID = bookID
		self.title = title
		self.author = author
		self.yearPublished = yearPublished
		self.pages = pages
		self.borrowedState = borrowedState
		self.user = user   # object


	def lend(self, user):

		if len(user.borrowedBookList) >= BookLimitReachedError.BOOK_LIMIT_PER_USER:
			raise BookLimitReachedError(user)
		
		self.borrowedState = "Borrowed"       # change borrowed state of the book
		self.user = user                      # change the user of the book object to the user passed
		user.borrowedBookList.append(self)    # add book object to borrowed list of the user

		# change the borrowed_state and user_id in the database
		queryType = "update"
		borrowedStateQuery = "UPDATE LIBRARY_BOOK SET borrowed_state = 'Borrowed' WHERE book_id = " + str(self.bookID)
		userIDQuery = "UPDATE LIBRARY_BOOK SET user_id = " + str(user.userID) + " WHERE book_id = " + str(self.bookID)
		DBUtils.getInstance().executeQuery(queryType, borrowedStateQuery)
		DBUtils.getInstance().executeQuery(queryType, userIDQuery)

		return "Book successfully Lent"


	def acceptReturn(self, user):

		self.borrowedState = "Available"   # change borrowed state of book object to "Available"
		self.user = None                   # change owner of book to None
		user.borrowedBookList.remove(self) # remove book object from the users borrowed books list

		# change the borrowed state and the use id in the database
		queryType = "update"
		borrowedStateQuery = "UPDATE LIBRARY_BOOK SET borrowed_state = 'AVAILABLE' WHERE book_id = " + str(self.bookID)
		userIDQuery = "UPDATE LIBRARY_BOOK SET user_id = NULL WHERE book_id = " + str(self.bookID)
		DBUtils.getInstance().executeQuery(queryType, borrowedStateQuery)
		DBUtils.getInstance().executeQuery(queryType, userIDQuery)

		return "Book successfully Returned"


		