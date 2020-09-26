import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="passw0rd",
  database="db_rolodex"
)

#Creats the Account table if it doesn't exist
def create_table():
  createtable = "Create Table IF NOT EXISTS Accounts "
  createtable = createtable + "("
  createtable = createtable + " AccountID 	INT 			NOT NULL AUTO_INCREMENT,"
  createtable = createtable + " AccountType VARCHAR(1) 		NOT NULL,"
  createtable = createtable + " IsActive	VARCHAR(1)		NOT NULL,"
  createtable = createtable + " FullName 	VARCHAR(1000) 	NOT NULL,"
  createtable = createtable + " FirstName 	VARCHAR(200) 	NOT NULL,"
  createtable = createtable + " MiddleName 	VARCHAR(200) 	NOT NULL,"
  createtable = createtable + " LastName 	VARCHAR(500) 	NOT NULL,"
  createtable = createtable + " Comments 	VARCHAR(5000) 	NOT NULL,"
  createtable = createtable + " AddressLine1 	VARCHAR(200) 	NOT NULL,"
  createtable = createtable + " AddressLine2 	VARCHAR(200) 	NOT NULL,"
  createtable = createtable + " AddressLine3 	VARCHAR(200) 	NOT NULL,"
  createtable = createtable + " City 	VARCHAR(200) 	NOT NULL,"
  createtable = createtable + " StateProv 	VARCHAR(100) 	NOT NULL,"
  createtable = createtable + " PostalCode 	VARCHAR(20) 	NOT NULL,"
  createtable = createtable + " Country 	VARCHAR(50) 	NOT NULL,"
  createtable = createtable + " Phone1 	VARCHAR(50) 	NOT NULL,"
  createtable = createtable + " Phone2 	VARCHAR(50) 	NOT NULL,"
  createtable = createtable + " Phone3 	VARCHAR(50) 	NOT NULL,"
  createtable = createtable + " Phone4	VARCHAR(50) 	NOT NULL,"
  createtable = createtable + " AddedDate 	DATETIME		NOT NULL,"
  createtable = createtable + " PRIMARY KEY (AccountID)"
  createtable = createtable + " );"

  mycursor = mydb.cursor()
  mycursor.execute(createtable)

#Insert a new account
def insert_Account():
  mycursor = mydb.cursor()
  current_utc = datetime.datetime.utcnow()

  AccountType = input("Is this a Business (Y/N)? ")
  if AccountType == "Y" or AccountType == "y":
    AccountType = "B"
    FullName = input("Business Name is: ")
    FirstName = ""
    MiddleName = ""
    LastName = ""
  else:
    AccountType = "I"
    FullName = ""
    FirstName = input("First Name is: ")
    MiddleName = input("Middle Name is: ")
    LastName = input("Last Name is: ")
  
  Comments = input("Comments: ")
  AddressLine1 = input("Address Line 1: ")
  AddressLine2 = input("Address Line 2: ")
  AddressLine3 = input("Address Line 3: ")
  City = input("City: ")
  StateProv = input("State or Prov: ")
  PostalCode = input("Postal Code: ")
  Country = input("Country: ")
  Phone1 = input("Phone 1: ")
  Phone2 = input("Phone 2: ")
  Phone3 = input("Phone 3: ")
  Phone4 = input("Phone 4: ")

  sql = "INSERT INTO Accounts (AccountType, IsActive, FullName, FirstName, MiddleName, LastName, Comments, AddressLine1, AddressLine2, AddressLine3, City, StateProv, PostalCode, Country, Phone1, Phone2, Phone3, Phone4, AddedDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  val = (AccountType, "Y", FullName, FirstName, MiddleName, LastName, Comments, AddressLine1, AddressLine2, AddressLine3, City, StateProv, PostalCode, Country, Phone1, Phone2, Phone3, Phone4, current_utc)
  mycursor.execute(sql, val)

  mydb.commit()

#search accounts
def search_Account():
  mycursor = mydb.cursor()
  print("1 - Search by Account # or Name")
  print("2 - Search by Phone Number")
  print("3 - Search by Address")
  menu = input("Make a number selection? ")

  columns = "SELECT concat('Account # ', CAST(AccountID as char(20)), ' - ', FullName, Trim(concat(firstName, ' ', MiddleName, ' ', LastName)), ' - Active = ', IsActive, char(10), char(13), 'Address: ', AddressLine1, char(10), char(13), AddressLine2, char(10), char(13), City, ', ',StateProv,' ',PostalCode, char(10), char(13), Phone1) as Results"

  if menu == "1":
    searchname = input("Name or AccountID to search: ")
    if searchname.isdigit():
      query = " From Accounts WHERE AccountID = " + searchname
    else:
      query = " From Accounts WHERE concat(FullName,FirstName,MiddleName,LastName) LIKE '%" + searchname +"%'"
  elif menu == "2":
    searchname = input("Phone Number to search: ")
    query = " From Accounts WHERE REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(concat(Phone1,Phone2,Phone3,Phone4),')',''),'(',''),'-',''),' ',''),'.','') LIKE '%" + searchname +"%'"
  elif menu == "3":
    searchname = input("Address to search: ")
    query = " From Accounts WHERE REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(concat(AddressLine1,AddressLine2,AddressLine3,City, StateProv, PostalCode),'#',''),',',''),'-',''),' ',''),'.','') LIKE '%" + searchname +"%'"

  query = columns + query

  mycursor.execute(query)
  myresult = mycursor.fetchall()

  for x in myresult:
    print(x)

#Activate or Deactivate an account by ID
def switch_Account_Active():
  mycursor = mydb.cursor()
  accountID = input('Which Account # do you want to update? ')
  sql = "UPDATE Accounts SET IsActive = CASE WHEN IsActive = 'Y' THEN 'N' ELSE 'Y' END WHERE AccountID = '" + accountID + "'"
  mycursor.execute(sql)
  mydb.commit()
  print("Account # " + accountID + " has had its active status switched.")

#Run the program
create_table()
exitprogram = False

while exitprogram == False:
  print("1 - Add account")
  print("2 - Search account")
  print("3 - Activate/Deactivate account")
  print("4 - Exit")
  menu = input("Make a number selection? ")

  if menu == "1":
    insert_Account()
  elif menu == "2":
    search_Account()
  elif menu == "3":
    switch_Account_Active()
  elif menu == "4":
    exitprogram = True 
  else:
    print("You chose poorly")