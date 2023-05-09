class User:

	def __init__(self, userID, firstName, lastName, userAddress, userEmail):
		self.userID = userID
		self.firstName = firstName
		self.lastName = lastName
		self.userAddress = userAddress
		self.userEmail = userEmail
		self.borrowedBookList = []       # list of objects


	def booksBorrowed(self):
		return self.borrowedBookList
