import pickle

class Member(object):
	mid = 0 
	def __init__(self, name):
		self.name = name
		self.i = Member.mid
		Member.mid += 1

class Book(object):
	bid = 0 
	def __init__(self, title, author, publisher):
		self.title = title
		self.author = author
		self.publisher = publisher
		self.outOnLoan = False
		self.i = Book.bid
		Book.bid += 1

class Loan(object):
	def __init__(self, member, book, date):
		self.member = member
		self.book = book
		self.date = date


def addMember(alist):
	try:
		print("\n Add new customer")
		n = input(" Name   : ").strip()
		if n != "":
			alist.append(Member(n))
			return True
		else:
			return False
	except Exception:
		return False
	
def addBook(alist):
	print("\n Add new book")
	print(" (Enter no title to quit)")
	t = input(" Title     : ").strip()
	if t == "":
		return False
	a = input(" Author    : ").strip()
	p = input(" Publisher : ").strip()
	alist.append(Book(t,a,p))
	return True

def getItemById(alist, i):
	"""Pass a list of records and an id
	will return an object with matching id
	or None if no match found"""
	for record in alist:
		if record.i == i:
			return record
	return None


def getPersonIndexByName(alist, name):
	"""Pass a list of records and a name
	will return the index with matching name
	or None if no match found"""
	for i in range(0, len(alist) ):
		if alist[i].name == name:
			return i
	return None
	
def getBooksByAuthor(alist, author):
	mylist = []
	for record in alist:
		if record.author == author:
			mylist.append(record)
	return mylist


def findAllBooksByAuthor(alist):
	print("\n Find all books by author")
	author = input("  Enter author: ")
	mylist = getBooksByAuthor(alist, author)
	viewBooks(mylist)


def viewLoans(loans):
	if len(loans) == 0:
		print("\n NO LOANS")
	else:
		print("\n All loans")
		print(" ---------")
		for record in loans:
			print( " "+ record.book.title +" \t-> "+ record.member.name ) 


def viewMembers(alist):
	if len(alist) == 0:
		print("\n NO MEMBERS")
	else:
		print("\n Library membership\n ------------------")
		for record in alist:
			print(" "+str(record.i)+" "+record.name)
			
def viewBooks(alist):
	if len(alist) == 0:
		print("\n NO BOOKS")
	else:
		print("\n Current books\n --------")
		for record in alist:
			print(" "+str(record.i)+" '"+record.title+"' by "+record.author)

def newTransaction(members, books, loans):
	print(" \n New transaction.\n Take membership card and scan.")
	try:
		mid = int(input(" Enter member ID : "))
	except Exception:
		return False
	else:
		member = getItemById(members, mid)
		if not(member == None):
			print("\n Username found: "+member.name)
			print(" Scan book now and enter ID.")
			try:
				bid = int(input(" Enter book ID : "))
			except Exception:
				return False
			else:
				book = getItemById(books, bid)
				if book.outOnLoan:
					print("\n ! This book is already on loan.")
				else:
					print(" Title: "+book.title)
					if not(book == None):
						loans.append(Loan(member, book, "Today") )
						book.outOnLoan = True
						print(" \n Loan complete (Hand book to member and smile).")
						return True
					else:
						print("\n ! Book not found.")
						return False
		else:
			print("\n ! Customer not found.")
			return False

def returnBook(members, books, loans):
	print(" \n Book return.\n Take membership card and scan.")
	try:
		mid = int(input(" Enter member ID : "))
	except Exception:
		return False
	else:
		member = getItemById(members, mid)
		if not(member == None):
			print("\n Username found: "+member.name)
			print(" Scan book now and enter ID.")
			try:
				bid = int(input(" Enter book ID : "))
			except Exception:
				return False
			else:
				book = getItemById(books, bid)
				if not(book.outOnLoan):
					print("\n ! This book has not been checked out.\n Return to trolley for reshelving.")
				else:
					print(" Title: "+book.title)
					if not(book == None):
						loanIndex = findLoanIndex(loans, member, book)
						if loanIndex != None:
							loans.pop(loanIndex)
							book.outOnLoan = False
							print("\n Book returned successfully.")
							return True
						else:
							print("\n ! Something went wrong. There is no loan for that member and book.")
							return False
					else:
						print("\n ! Book not found.")
						return False
		else:
			print("\n ! Customer not found.")
			return False

def findLoanIndex(loans, member, book):
	for i in range(len(loans)):
		record = loans[i]
		if record.member.name == member.name and record.book.title == book.title:
			return i
	return None
			

def save(a1,a2,a3):
	try:
		f = open("librarydata.dat", "wb")
		pickle.dump(a1, f)
		pickle.dump(a2, f)
		pickle.dump(a3, f)
		f.close()
	except Exception:
		print(" ! File error ")

def load():
	try:
		f = open("librarydata.dat", "rb")
		a1 = pickle.load(f)
		a2 = pickle.load(f)
		a3 = pickle.load(f)
		f.close()
		Member.mid = len(a1)

		Book.bid = len(a2)
		return a1, a2, a3
	except Exception:
		print(" ! File error ")
		return [], [], []
		
members, books, loans = load()

flagToLeave = False

while not(flagToLeave):
	print("\n MAIN MENU")
	print("  1. Add member")
	print("  2. Add book")
	print("  3. New transaction")
	print("  4. View loans")
	print("  5. View members")
	print("  6. View books")
	print("  7. Find books by author")
	print("  8. Return book")

	user = input(">>> ")
	ok_to_save = False
	if user == "1":
		if addMember(members):
			save(members, books, loans)
	elif user == "2":
		if addBook(books):
			save(members, books, loans)
	elif user == "3":
		if newTransaction(members, books, loans):
			save(members, books, loans)
	elif user == "4":
		viewLoans(loans)
	elif user == "5":
		viewMembers(members)
	elif user == "6":
		viewBooks(books)
	elif user == "7":
		findAllBooksByAuthor(books)
	elif user == "8":
		if returnBook(members, books, loans):
			save(members, books, loans)
