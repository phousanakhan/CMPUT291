import sqlite3
import getpass
import time
import hashlib
import random
import re
import datetime
from datetime import datetime
from datetime import date
from datetime import timedelta

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def main():
    global connection, cursor
    
    database = input("Insert File Name for Desdired Database, ex. test.db. ...>") #insert database name
    
    connect(database)    
    validOptions = ['a','o'] #agent or user
    valid = False
    while valid == False:
        currentUserType, data = login()
        if currentUserType not in validOptions:
            print("The UserType is an invalid option") #makes sure user type is eiyther a or o
            valid = False   
        elif currentUserType != 'a': #opens officer menu
            optionsListOfficer(officerMenu(),currentUserType,data)
            valid = True
        elif currentUserType !='o':#opens agent menu
            optionsListAgent(agentMenu(),currentUserType,data)        
            valid = True
    
    connection.commit()
    connection.close()    
    

def login():
    global connection, cursor
    active = True
    while active:
        username = input("Enter your Username...>")
        password = getpass.getpass(prompt="Enter your Password ...>") #getpass.getpass hides the user input there for in this cae password is hidden when opening in terminal
        if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password): #sql injection prevention from lab slides
            cursor.execute("SELECT u.utype FROM users AS u WHERE u.uid = ? AND u.pwd = ? ;" , (username, password))  #sql injection prevention from lab slides
        activeuser = cursor.fetchall()
        #print(activeuser)
        if len(activeuser) == 0:
            print("Username or Password is Incorrect, Try again") #makes sure that the username and password match and that there actually is a user with that combination
        else:
            active= False
            data = (username,password) #savces the username and password as data to be passed to other functions
    #print(activeuser)
    #print(type(activeuser))
    userType = activeuser[0][0] #establishes the active usertype which is either a or o
    return userType, data


def agentMenu():
    options = [1,2,3,4,5,6,7]
    active = True
    print("\n\n")#prints all the user options for agents
    print("#################")
    print("#  Available Options:  #")
    print("#################")
    print("1. Register a birth")
    print("2. Register a Marrage ")
    print("3. Renew a Vehicle Registration ")
    print("4. Process Bill of Sale ")
    print("5. Process a Payment")
    print("6. Get a Driver Abstract")
    print("7. Logout")
    print("#################")
    print("\n")
    while active:
        choice = int(input("What task would you like to perform, Enter the number...>")) #makes ure the pick is withing the valid options in this case its a list
        if choice in options:
            active = False
        else:
            print("Please enter a valid option...>")
            active = True    
    
    return choice


def officerMenu():
    options = [1,2,3]
    active = True
    #prints all the user options for officers
    print("\n\n")
    print("#################")
    print("#  Available Options:  #")
    print("#################")
    print("1.  Issue a Ticket")
    print("2. Find a Car Owner")
    print("3. Logout")
    print("#################") 
    while active:
        choice = int(input("What task would you like to perform, Enter the number...>"))#makes ure the pick is withing the valid options in this case its a list
        if choice in options:
            active = False
        else:
            print("Please enter a valid option...>")
            active = True  
            
    return choice

def optionsListAgent(choice,userType,data):
    #helper function to launch the desired  fuction of the user who is an agent sending usertype and data as paramenters
    if choice == 1:
        registerBirth(userType,data)
    elif choice == 2:
        reg_marriage(userType,data)
    elif choice == 3:
        renewVehicle(userType,data)
    elif choice == 4:
        processBill(userType,data)
    elif choice == 5:
        processPayment(userType,data)
    elif choice == 6:
        driver_abstract(userType,data)
    elif choice == 7:
        logout()

def optionsListOfficer(choice,userType,data):
     #helper function to launch the desired  fuction of the user who is an officer sending usertype and data as paramenters
    if choice == 1:
        issue_ticket(userType,data)
    elif choice == 2:
        find_owner(userType,data)
    elif choice == 3:
        logout()


def registerBirth(userType,data):
    #register birth function allowing user who is agent to register a birth and at same time register a person 
    #upon entering all of the prompts for input and those inputs being valid
    global connection, cursor
    username = data[0]
    password = data[1]
    print("Enter Information as Prompted\n")
    #User address
    cursor.execute("SELECT city FROM users WHERE uid = ?", (str(data[0]), ))#finds the user address of the active agent
    useradd = cursor.fetchall()
    useraddress = useradd[0][0]
    #print(useraddress)
    
    #Random Regno
    cursor.execute("SELECT MAX(regno) FROM births")
    birthregno = int(cursor.fetchone()[0]) + 1     
    
    #Reg Date
    birthregdate = time.strftime("%Y-%m-%d")#sets registration date to current date 
    
    #Child names
    childfname = input("Enter Childs First Name...>").capitalize()
    childlname = input("Enter Childs Last Name...>").capitalize()
    temp = True
    while temp:
    #Child gender
        gender = input("Enter Childs Gender M/F...>").upper()#sets the gender to either M or F dependent on input
        if gender == "male":
            gender = "M"
        elif gender == "female":
            gender = "F"
        
        if len(gender) != 1:
            print("Invalid input")
        else:
            temp = False
        
    
    #Child bdate
    bdateupdate = validdate('Enter your birth date in YYYY-MM-DD format: ')#makes sure date input is valid by using helper function

    
    #Child bplace
    birthplace = input("Enter Childs Place of Birth...>").capitalize()
    
    #Father Parent Info
    fathfname = input("Enter Childs Fathers First Name...>").lower()
    fathlname = input("Enter Childs Fathers Last Name...>").lower()
    
    cursor.execute("SELECT LOWER(fname), LOWER(lname) FROM persons WHERE fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE ;",(fathfname,fathlname))     #finds the first name and last name of people who have the name as entered above to ensure they are in the persons database       
    father = cursor.fetchall()
    #print(father)
    #print(father[0][0])
    #print(father[0][1])    
    #print(father[0])
    
    fatherList = []
    for i in father: #add to list
        fatherList.append(i)    
    #print(fatherList)
    if (fathfname, fathlname) not in fatherList: #if the fathers fname and lname are not in the database then they will need to enter the data to add them to the persons database
        print("Father Not in Database, Please Register Below.")
        fathfname = fathfname.capitalize()
        print("Fathers First Name...> " + fathfname)
        fathlname = fathlname.capitalize()
        print("Fathers Last Name...> " + fathlname )
        fathbplace = input("Fathers Birth Place...>")
        
        fathbdate = validdate("Fathers Birth Date in YYYY-MM-DD format:...> ")
              
        fathadd = input("Fathers Address...>").capitalize()
        fathpho = input("Fathers Phone#...>")
        if fathpho == "":
            phoneformfath = ""  
        else:
            phoneformfath = format(int(fathpho[:-1]), ",").replace(",","-") + fathpho[-1]# formats the phone number that the person inputs by thousands and dividing it by a - ex 1234567890 = 1-234-567-890 credit. utdemir from stackoverflow via https://stackoverflow.com/questions/7058120/whats-the-best-way-to-format-a-phone-number-in-python 
    
        cursor.execute("INSERT INTO persons VALUES(?,?,?,?,?,?);",(fathfname, fathlname,fathbdate,fathbplace,fathadd,phoneformfath))# adds the father to the database if he isnt already in there
        connection.commit()
        print("Father Now in Database")
        
    else:
        print("Father is in Database, Please Continue")        
        
    #Mother Parent Info
    mothfname = input("Enter Childs Mother First Name...>").lower()
    mothlname = input("Enter Childs Mother last Name...>").lower()
    
    cursor.execute("SELECT LOWER(fname), LOWER(lname) FROM persons WHERE fname = ?  COLLATE NOCASE AND lname = ? COLLATE NOCASE;",(mothfname,mothlname)) #if the mothers fname and lname are not in the database then they will need to enter the data to add them to the persons database
    mother= cursor.fetchall()
    #print(father[0][0])
    #print(father[0][1])
    #print(father[0])
    motherList = []
    for i in mother: #add to list
        motherList.append(i)      
    #print(motherList)
    if (mothfname, mothlname) not in motherList:
        print("Mother Not in Database, Please Register Below.")
        mothfirname = mothfname.capitalize()
        print("Mothers First Name...> " + mothfirname )
        mothlasname = mothlname.capitalize()
        print("Mothers Last Name...> " + mothlasname)
        mothbplace = input("Mothers Birth Place...>")
        
        mothbdate = validdate("Mothers Birth Date in YYYY-MM-DD format:...> ")
        mothadd = input("Mothers Address...>")
        
        mothpho = input("Mothers Phone#...>")
        
        if mothpho == "":
            phoneformmoth = ""
        else:
            phoneformmoth = format(int(mothpho[:-1]), ",").replace(",","-") + mothpho[-1]# formats the phone number that the person inputs by thousands and dividing it by a - ex 1234567890 = 1-234-567-890 credit. utdemir from stackoverflow via https://stackoverflow.com/questions/7058120/whats-the-best-way-to-format-a-phone-number-in-python 
        
        cursor.execute("INSERT INTO persons VALUES (?,?,?,?,?,?);",(mothfname, mothlname,mothbdate,mothbplace,mothadd,phoneformmoth))     # adds the mother to the database if he isnt already in there   
        connection.commit()
        print("Mother Now in Database")
        
    else:
        print("Mother is in Database, Please Continue")

    cursor.execute("SELECT address, phone FROM persons WHERE fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE ;",(mothfname,mothlname))    
    motherdata = cursor.fetchall()    
    #print(motherdata, type(motherdata))
    #print(motherdata[0][0])
    #print(motherdata[0][1])    
    
    #print(fathfname.capitalize())
    temp1 = fathfname.capitalize()
    #print(fathlname.capitalize())
    temp2 = fathlname.capitalize()
    #print(mothfname.capitalize())
    temp3 = mothfname.capitalize()
    #print(mothlname.capitalize())    
    temp4 = mothlname.capitalize()
       
    cursor.execute("INSERT INTO persons VALUES(?,?,?,?,?,?);",(childfname, childlname, bdateupdate, birthplace, motherdata[0][0], motherdata[0][1]))
    connection.commit()#inserts new person in to the persons table which is the new child into the database
    cursor.execute("INSERT INTO births VALUES (?,?,?,?,?,?,?,?,?,?);",(birthregno, childfname, childlname, birthregdate, birthplace, gender, temp1, temp2, temp3, temp4))
    connection.commit()#insters the new child in the the births table with the required characteristics 
   
    print("Succesfully Registered a Birth and a Person \n\n")
    
    
    guess = input("Would you like to perform another task?...y/n...>") #prompts the user if they would like to perform another task afer the proir has completed e
    if guess == 'y':
        if userType == 'a':
            optionsListAgent(agentMenu(),userType,data) #launches the agent menu with all the requiered parameters
        else:
            optionsListOfficer(officerMenu(),userType,data)#launches the officer menu with all the requiered parameters
    else:
        logout()

def reg_marriage(userType,data,user_fname = '%s', user_lname = '%s'):
    # marriages (regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname)
    # regno must be generated
    # regdate is today's date
    # regplace is user's city
    global connection, cursor
    cursor = connection.cursor()

    user_fname = input("input your first name: ")
    user_lname = input("input your last name: ")
    user_fname = user_fname.lower()    #make all the user input lowercase. This will handle case sensitivity
    user_lname = user_lname.lower()    #make all the user input lowercase. This will handle case sensitivity
       

    p_fname = input("input partner first name: ")
    p_lname = input("input partner last name: ")  
    p_fname = p_fname.lower()    #make all the user input lowercase. This will handle case sensitivity 
    p_lname = p_lname.lower()     #make all the user input lowercase. This will handle case sensitivity
    cursor.execute("SELECT fname, lname FROM persons") #select all fname, lname
    user_list = cursor.fetchall()
    userList = []
    tups = None
    bups = None
    for i in user_list: #add to userList. The userList will contain fname, lname of all persons in db
        (tups,bups) = i
        tups=tups.lower()
        bups=bups.lower()
        i = (tups,bups)
        userList.append(i)

    if (user_fname, user_lname) in userList and (p_fname, p_lname) in userList: #check if user input in the database
        print("user and partner in database, register process finished")
        #unique regno

        cursor.execute("SELECT MAX(regno) FROM marriages")    #Obtain the maximum regno, then add 1
        regno = int(cursor.fetchone()[0]) + 1    #Obtain the maximum regno, then add 1

        #regdate
        regdate = time.strftime("%Y-%m-%d")

        #regplace
        cursor.execute("SELECT city FROM users WHERE uid = ?", (str(data[0]), ))    #city of user 

        regplace = cursor.fetchone()
        if regplace != None:
            for city in regplace:
                regplace = str(city)
        else:
            regplace = "None"

        #insert marraige
        #.capitalize() capitalize the first letter. This handle case sensitivity
        cursor.execute("INSERT into marriages VALUES(?,?,?,?,?,?,?);", (regno, regdate, regplace, user_fname.capitalize(), user_lname.capitalize(), p_fname.capitalize(), p_lname.capitalize()))
        connection.commit()          

    elif (user_fname, user_lname) not in userList:   #check if user_fname, user_lname in database, if not add to person
        print("user details is not in database, please input the following")
        new_fname = user_fname
        new_lname = user_lname

        new_bdate = validdate('Enter your birth date in YYYY-MM-DD format: ')
        

        new_bplace = input("Input your birth place: ")
        new_address = input("Input your address: ")
        new_phone = input("Input your phone number: ")

        cursor.execute("INSERT into persons VALUES(?,?,?,?,?,?);", (new_fname.capitalize(), new_lname.capitalize(), new_bdate, new_bplace, new_address, new_phone))
        connection.commit()
        reg_marriage(userType, data, user_fname, user_lname)    #call the function again. This time informations will be in db.

    elif (p_fname, p_lname) not in userList:#check if p_fname, p_lname in database, if not add to person
        print("partner details is not in database, please input the following")
        new_fname_1 = p_fname
        new_lname_1 = p_lname

        new_bdate_1 = validdate('Enter partner birth date in YYYY-MM-DD format: ')
         

        new_bplace_1 = input("Input partner birth place: ")
        new_address_1 = input("Input partner address: ")
        new_phone_1 = input("Input partner phone number: ")

        cursor.execute("INSERT into persons VALUES(?,?,?,?,?,?);", (new_fname_1.capitalize(), new_lname_1.capitalize(), new_bdate_1, new_bplace_1, new_address_1, new_phone_1))
        connection.commit()
        reg_marriage(userType, data, user_fname, user_lname)

    guess = input("Would you like to perform another task?...y/n...>")
    if guess == 'y':
        if userType == 'a':
            optionsListAgent(agentMenu(),userType,data)
        else:
            optionsListOfficer(officerMenu(),userType,data)
    else:
        logout()

def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))

def renewVehicle(userType, data):
    #Renew a vehicle registration.The user should be able to provide an existing registration number and renew the registration. 
    #The system should set the new expiry date to one year from today's date if the current registration either has expired or expires today. 
    #Otherwise, the system should set the new expiry to one year after the current expiry date.
    global connection, cursor
    cursor = connection.cursor()    
    

#The system should set the new expiry date to one year from today's date if the current registration either has expired or expires today. 
    today_date = datetime.today() #get today's date

#check whether registration exist in db
    exist_reg = int(input("input an existing registration number: ")) #user input existed regno

    cursor.execute("SELECT regno FROM registrations;")
    all_regno = cursor.fetchall()
    all_reg_list = []
    for i in all_regno:
        for j in i:
            all_reg_list.append(j)    #Two for loops allows j to a string
    
    while exist_reg not in all_reg_list:
        print("This registration number is not in the database")
        exist_reg = int(input("TRY AGAIN:\n input an existing registration number: "))

    cursor.execute("SELECT expiry FROM registrations WHERE regno = ?;", (exist_reg, ) ) #sql execution
    
    expiry_date = None
    existReg_1 = cursor.fetchone() 
    for date in existReg_1:
        year,month,day = date.split('-')
        expiry_date= datetime(int(year),int(month),int(day))    #assigning expiry_date
        
        
    if expiry_date <= today_date: #check if expiry date is less than or equal to current date
        expiry_date = add_years(datetime.today(),1)
        expiry_date = expiry_date.strftime("%Y-%m-%d") #This will be the new expiry date. 
        cursor.execute("UPDATE registrations SET expiry = ? WHERE regno =?;", (expiry_date, exist_reg, ) ) #sql execution
    
    elif expiry_date > today_date:
        expiry_date = add_years(expiry_date,1)
        expiry_date = expiry_date.strftime("%Y-%m-%d")
        cursor.execute("UPDATE registrations SET expiry = ? WHERE regno =?;", (expiry_date, exist_reg, ) )
        
    connection.commit() 
    
    guess = input("Would you like to perform another task?...y/n...>")
    if guess == 'y':
        if userType == 'a':
            optionsListAgent(agentMenu(),userType,data)
        else:
            optionsListOfficer(officerMenu(),userType,data)
    else:
        logout()
def processBill(userType,data):
    global connection, cursor
    vin=True
    while(vin==True):
        pVIN = input("input an existing vehicle's VIN: ")
        cursor.execute('''Select regno from registrations where vin = ?''',(pVIN,))
        vinno1 = cursor.fetchone()
        if(vinno1!=None):vin=False
        else: print("Invalid please try again")
    pCurrentFname = input("input the first name of the current owner: ")
    pCurrentLname = input("input the last name of the current owner: ")
    pCurrentName = (pCurrentFname.lower(), pCurrentLname.lower())
    
    pNewFname = input("input the first name of the new owner: ")
    pNewLname = input("input the last name of the new owner: ")
    pNewName = (pNewFname.lower(), pNewLname.lower())
    
    pPlateNumber = input("input the a new plate number: ")
    
    
    
    #check if new owner in persons table
    cursor.execute("SELECT fname, lname FROM persons") #select all fname, lname
    user_list = cursor.fetchall()
    userList = []
    tups = None
    bups = None
    for i in user_list: #add to list. This handle case sensitivity
        (tups,bups) = i
        tups=tups.lower()
        bups=bups.lower()
        i = (tups,bups)
        userList.append(i)
    while pNewName not in userList:    #if user input not in userList
        print("new owner is not in the database, please try again")
        pNewFname = input("input the first name of the new owner: ")
        pNewLname = input("input the last name of the new owner: ")
        pNewName = (pNewFname.lower(), pNewLname.lower())        
        
    
    #For most recent owner, we must find the latest registration for the VIN. Then compare the owner
    cursor.execute("SELECT regdate FROM registrations WHERE VIN = ?;", (pVIN, ) )
    reg_date = []
    latest_reg_date = None
    latest_owner = None
    pubs = None
    dubs = None
    
    CurrentDate = cursor.fetchall()   
    for tuple1 in CurrentDate:
        for date in tuple1:
            reg_date.append(date)
    latest_reg_date = max(reg_date)    #max(reg_date) will return the latest date
    
    cursor.execute("SELECT fname,lname FROM registrations WHERE VIN = ? AND regdate = ?;", (pVIN, latest_reg_date,  ) )
    m_recent_owner = cursor.fetchall()
    for i in m_recent_owner: #turn list into tuple, so it can be compare against output
        (pubs, dubs) = i #handle case sensitivity
        pubs = pubs.lower()
        dubs = dubs.lower()
        latest_owner = (pubs, dubs)

    
    #Transfer can NOT be made if owner entered does not match the owner in db
    while latest_owner != pCurrentName:
        print("Transfer can not be made")
        print("Latest owner is not the same as current owner")
        Fname = input("TRY AGAIN: input the first name of the current owner: ")
        Lname = input("TRY AGAIN: input the last name of the current owner: ")
        pCurrentName = (Fname.lower(), Lname.lower())
           
           
    #Transfer CAN be made
    #1.Unique_regno    2.regdate = today    3.expiry = 1yr + today    4.newVin = OldVIN    5.plate numb    6.fname,lname
    regno = None
    regDate = None
    expiryDate = None
    newVIN = None
    #pPlateNumber
    #pCurrentFname 
    #pCurrentLname  
    
    if latest_owner == pCurrentName:
#Create new registration
        #1
        cursor.execute("SELECT MAX(regno) FROM registrations")
        regno = int(cursor.fetchone()[0]) + 1
        
        #2
        regDate = datetime.today().strftime("%Y-%m-%d")
        
        
        #3
        expiryDate = add_years(datetime.today(),1)
        expiryDate = expiryDate.strftime("%Y-%m-%d")
        
        #4
        newVIN = pVIN
        
    cursor.execute("INSERT into registrations VALUES(?,?,?,?,?,?,?);", (regno, regDate, expiryDate, pPlateNumber, newVIN, pNewFname.capitalize(), pNewLname.capitalize()))
    
#current registration
    cursor.execute("UPDATE registrations SET expiry = ? WHERE VIN =? AND fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE ;", (regDate, pVIN, pCurrentFname, pCurrentLname) )

    connection.commit() 

    guess = input("Would you like to perform another task?...y/n...>")
    if guess == 'y':
        if userType == 'a':
            optionsListAgent(agentMenu(),userType,data)
        else:
            optionsListOfficer(officerMenu(),userType,data)
    else:
        logout()


def processPayment(userType,data):
#Process a payment.The user should be able to record a payment by entering a valid ticket number and an amount. 
#The payment date is automatically set to the day of the payment (today's date). 
#A ticket can be paid in multiple payments but the sum of those payments cannot exceed the fine amount of the ticket.
    global connection, cursor
    
    #check if ticket number is valid   
    valid_ticket = input("input a valid ticket number(tno): ")
    valid_ticket = int(valid_ticket)
    cursor.execute("SELECT tno FROM tickets; ")
    tick_list = cursor.fetchall()
    tickList1 = []
    for ticket in tick_list:
        for tuple_ticket in ticket:
            tickList1.append(tuple_ticket) 
    while valid_ticket not in tickList1:
        print("ticket number is not valid. Please try again")
        valid_ticket = input("input a valid ticket number(tno): ")
        valid_ticket = int(valid_ticket)
        
    #displaying tno, fine, vdate
    cursor.execute("SELECT tno, fine, vdate FROM tickets WHERE tno = ?; ",(valid_ticket, ))
    info_list = cursor.fetchall()
    #print(info_list)
    print("tno: ", info_list[0][0]) #info_list contains list inside a list
    print("fine: ", info_list[0][1])
    print("vdate: ", info_list[0][2])
    
    #displaying total payments from tno
    cursor.execute("SELECT sum(amount) FROM payments WHERE tno=? GROUP BY tno; ", (valid_ticket, ))
    paid_list = cursor.fetchone()
    for amount_paid in paid_list:    
        print("You have paid in total: ", paid_list[0])
    
    if (paid_list == None) or (paid_list[0] == 0):
        Amount_Paid = 0
    else:
        Amount_Paid = int(paid_list[0])
        

    #Enter amount of payment
    fine = int(info_list[0][1])
    left_pay = print("You still need to pay: ", (fine - Amount_Paid))    #display amount needed to be pay
    payment = int(input("enter an amount you want to pay: "))
    
    #check if payment <= 0
    while payment <= 0:
        print("payment must be greater than 0")
        payment = int(input("TRY AGAIN: enter an amount you want to pay: "))
        
    #check if payment > fine
    while payment > fine:
        print("Payment can not be greater than fine")
        payment = int(input("TRY AGAIN: enter an amount you want to pay: "))
        
        
    today_date = datetime.today().strftime("%Y-%m-%d")
    if paid_list == None:
        cursor.execute("INSERT INTO payments VALUES(?,?,?);", (valid_ticket, today_date, payment, ))
        connection.commit() 
    
    else: #initial payment already made in db
        paid_list = paid_list[0]
        if (paid_list + payment) <= fine:
            try:
                cursor.execute("INSERT INTO payments VALUES(?,?,?);", (valid_ticket, today_date, payment, ))
                connection.commit() 
                print("payment have been recorded")
            except Exception: #Exception catches all the exception in python
                print("error, payment have already been made today. Please try again tomorrow")
                
        else:
            print("sum of total payment is greater than fine")
            
    guess = input("Would you like to perform another task?...y/n...>")
    if guess == 'y':
        if userType == 'a':
            optionsListAgent(agentMenu(),userType,data)
        else:
            optionsListOfficer(officerMenu(),userType,data)
    else:
        logout()

    connection.commit() 

def ValidInput(inputMessage, validResponses):
    # Makes sure that the given question, has the correct input
    Exit = False
    while (not Exit):
        response = input(inputMessage)
        for r in validResponses:
            if (r == response):
                Exit = True
                break
        if(Exit == True):
            break
        print("Invalid input")
    return response

def driver_abstract(userType,data):
    #  The user should be able to enter a first name and a last name and get a driver abstract, 
    #  which includes the number of tickets, the number of demerit notices, the total number of 
    #  demerit points received both within the past two years and within the lifetime. The user 
    #  should be given the option to see the tickets ordered from the latest to the oldest. For 
    #  each ticket, you will report the ticket number, the violation date, the violation
    #  description, the fine, the registration number and the make and model of the car 
    #  for which the ticket is issued. If there are more than 5 tickets, at most 5 tickets
    #  will be shown at a time, and the user can select to see more.
    global connection, cursor

    # input first and last name
    fname = input('Enter first name: ')
    lname = input('Enter last name: ')
    name = (fname,lname)

    # demerit notices and points query
    # num_dnotice[0]: number of demerit notices
    # num_dnotice[1]: total demerit points
    cursor.execute('''SELECT COUNT(*),sum(points) FROM demeritNotices d
                WHERE d.fname = ? COLLATE NOCASE AND d.lname = ? COLLATE NOCASE;''',name)
    num_dnotice = cursor.fetchone()
    if num_dnotice[0] == None: 
        num_dnotices = 0 # set number of demerit notices to 0
    else: num_dnotices = num_dnotice[0]
    if num_dnotice[1] == None: 
        num_dnoticepoints = 0 # set total number of demerit to 0
    else: num_dnoticepoints = num_dnotice[1]

    # demerit points in last 2 years query
    # num2yr_points[0]: number of demerit points in last two years
    cursor.execute('''SELECT COUNT(*),sum(points) FROM demeritNotices 
                        WHERE fname = ? COLLATE NOCASE AND lname = ? COLLATE NOCASE
                        AND ddate > date('now', '-2 years');''',name)
    num2yr_points = cursor.fetchone()
    if num2yr_points[0] == None: 
        num2yr_pointnotices = 0 # set number of demerit notices to 0
    else: num2yr_pointnotices = num2yr_points[0] # set number to the sum of points
    if num2yr_points[1] == None: 
        num2yr_point = 0 # set number of demerit notices to 0
    else: num2yr_point = num2yr_points[1] # set number to the sum of points

    #  tickets given in past two years
    cursor.execute('''SELECT COUNT(*) 
                    FROM tickets t,registrations r,vehicles v 
                    WHERE r.fname = ? COLLATE NOCASE AND r.lname = ? COLLATE NOCASE
                    AND r.regno = t.regno
                    AND r.vin = v.vin AND t.vdate > date('now', '-2 years');''',name)
    ticket2yr = cursor.fetchone()
    if ticket2yr[0] == None:
        tickets2yr = 0 # if tickets in last 2 years is 0
    else: tickets2yr = ticket2yr[0] # set number to the tickets found

    #  each ticket details ticket number, violation date. fine, registration number
    #  make and model of the car
    cursor.execute('''SELECT t.tno,t.vdate,t.violation,t.fine,r.regno,v.make,v.model 
                    FROM tickets t,registrations r,vehicles v 
                    WHERE r.fname = ? COLLATE NOCASE AND r.lname = ? COLLATE NOCASE
                    AND r.regno = t.regno
                    AND r.vin = v.vin ORDER BY t.vdate DESC;''',name)
    tickets = cursor.fetchall()
    if tickets == None:
        tickets=0 # if not tickets found number of tickets in lifetime equal 0

    # Output
    print(fname+" "+lname+"'s Driver Abstract:\nnumber of tickets: "+str(len(tickets))+"\nnumber of tickets in past 2 years: "+str(tickets2yr)+"\nnumber of demerit notices: "+ str(num_dnotices)+"\nnumber of demerit notices within the past 2 years: "+str(num2yr_pointnotices)+"\ntotal number of demerit points in past 2 years: "+str(num2yr_point)+"\ntotal number of demerit points in lifetime: "+str(num_dnoticepoints)+"\n")

    # Viewing all tickets
    if(len(tickets)>0):
        option = ValidInput("View {fname} {lname}'s tickets (Y/N)?: ", ["y", "Y", "n", "N"])
        option = str.upper(option)
        start = 0
        end = 0
        if len(tickets) >= 5:
            end = 5
        else:
            end = len(tickets)
        
        #  display tickets 
        while option != 'N':
            for item in range(start,end):
                print("Ticket number: "+str(tickets[item][0])+"\nTicket date: "+str(tickets[item][1])+"\nTicket description: "+str(tickets[item][2])+"\nTicket fine: "+str(tickets[item][3])+"\nVehicle registration number: "+str(tickets[item][4])+"\nVehicle make: "+str(tickets[item][5])+"\nVehicle model: "+ (tickets[item][6])+"\n")
            if len(tickets) > (end+4):
                option = ValidInput('View more tickets (Y/N): ', ["y", "Y", "n", "N"])
                option = str.upper(option)
                if option == 'N':break
                start = end
                end += 5
            elif len(tickets) == end:
                option = 'N'
                break
            else:
                # display more tickets
                option = ValidInput('View more tickets (Y/N): ', ["y", "Y", "n", "N"])
                option = str.upper(option)
                if option == 'N':break
                start = end
                end = len(tickets)
    print("Complete!")
    
    #  allows the agent to perform another task
    guess = input("Would you like to perform another task?...y/n...>")
    if guess == 'y':
        if userType == 'a':
            optionsListAgent(agentMenu(),userType,data)
        else:
            optionsListOfficer(officerMenu(),userType,data)
    else:
        logout()


def validdate(prompt):
    # checks whether the date entered in a valid format, and the date is valid
    # date is invalid if the formal is wrong or if the date in the future
    inputDate = input(prompt)
    # if date is not present set it to null
    if (inputDate==""):
        inputDate = "null"
    else:
        # check format of the date
        isValidDate = True
        try:
            datetime.strptime(inputDate, '%Y-%m-%d')
        except ValueError:
            isValidDate=False
        if(isValidDate):
            year,month,day = inputDate.split('-')
            try :
                datetime(int(year),int(month),int(day))
            except ValueError :
                isValidDate = False
            # checks if date is greater than today
            today = datetime.today().strftime("%Y-%m-%d")
            if(inputDate>today):
                isValidDate = False
        if(isValidDate) :
            return inputDate
        else:
            # invalid allows user to input again
            print("Invalid entry")
            validdate(prompt)
        
def validamount(prompt):
    # whether the given entry is an int if not than allow user to input again
    num = int(input(prompt))
    isValid = True
    if(isinstance(num,int)):
        return num
    else:
        print("Invalid entry")
        validamount(prompt)
        
def issue_ticket(userType,data):
    #  The user should be able to provide a registration number and see the person name that 
    #  is listed in the registration and the make, model, year and color of the car registered.
    #  Then the user should be able to proceed and ticket the registration by providing a
    #  violation date, a violation text and a fine amount. A unique ticket number should 
    #  be assigned automatically and the ticket should be recorded. The violation date 
    #  should be set to today's date if it is not provided.
    global connection, cursor

    #  input
    regno = input("Enter the registration number: ")
    #  check whether registration exists
    cursor.execute('''Select regno from registrations where regno = ?''',(regno,))
    regno1 = cursor.fetchone()

    # registration exists
    if(regno1!=None):
        #  find the vehicle
        cursor.execute('''Select r.fname, r.lname, v.make, v.model, v.year, v.color
            From registrations As r, vehicles As v
            Where r.regno=? And r.vin = v.vin''', (regno,))
        vehicle = cursor.fetchall()
        #  output info of the vehicle
        print("First name: "+str(vehicle[0][0])+"\nLast name: "+str(vehicle[0][1])+"\nVehicle make: "+str(vehicle[0][2])+"\nVehicle model: "+str(vehicle[0][3])+"\nVehicle year: "+str(vehicle[0][4])+"\nVehicle color: "+str(vehicle[0][5])+"\n")
        #  confirm to to proceed to issue ticket
        option = ValidInput('Proceed to issue ticket(Y/N): ', ["y", "Y", "n", "N"])
        option = str.upper(option)
        if(option == "Y"):
            #  info about the the ticket being issued
            vdate = validdate("Enter the violation date(YYYY-MM-DD): ")
            if(vdate==""):
                vdate = datetime.date.today().strftime("%Y-%m-%d")
            violation = input("Enter reason for violation: ")
            fine= validamount("Enter fine amount(integer): ")
            cursor.execute("SELECT max(tno) FROM tickets;")
            tno = cursor.fetchone()
            if tno == None:
                tno = 0
            else:
                tno = int(tno[0]) + 1
            #  inserting ticket into the tickets database
            cursor.execute("Insert into tickets values (?, ?, ?, ?, ?)", (tno, regno, fine, violation, vdate))
            connection.commit()
            print("Complete!")
    else:
        #  if registration number doesn't exist output no matches found
        print("No matches were found")
    
    #  allows the officer to perform another task
    guess = input("Would you like to perform another task?...y/n...>")
    if guess == 'y':
        if userType == 'a':
            optionsListAgent(agentMenu(),userType,data)
        else:
            optionsListOfficer(officerMenu(),userType,data)
    else:
        logout()

def find_owner(userType,data):
    #  The user should be able to look for the owner of a car by providing one or more 
    #  of make, model, year, color, and plate. The system should find and return all matches. 
    #  If there are more than 4 matches, you will show only the make, model, year, color, and 
    # the plate of the matching cars and let the user select one. When there are less than 4 
    #  matches or when a car is selected from a list shown earlier, for each match, the make, 
    #  model, year, color, and the plate of the matching car will be shown as well as the latest 
    #  registration date, the expiry date, and the name of the person listed in the latest 
    #  registration record.
    select = 0
    # intial query
    findowner_query = '''SELECT v.make, v.model, v.year, v.color, r.plate, r.regdate, r.expiry, r.fname||' '||r.lname
FROM vehicles v, (select vin, plate, regdate, expiry, fname, lname 
                                    from registrations r1 
                                    where regdate >= (select max(regdate) from registrations r2 where r2.vin = r1.vin)) as r
WHERE v.vin = r.vin'''
    print("Please give one or more characteristics (one atleast) to find the owner")
    # input the characteristics
    make = input("Enter car make, or leave it blank: ")
    model = input("Enter car model, or leave it blank: ")
    year = input("Enter car year, or leave it blank: ")
    color = input("Enter car color, or leave it blank: ")
    plate = input("Enter car plate, or leave it blank: ")
    # if make provided add this to query
    if make!='':
        findowner_query += " AND v.make = '{}'".format(make)
        findowner_query += ' COLLATE NOCASE'
    else: select += 1
    # if model provided add this to query
    if model!='':
        findowner_query += " AND v.model = '{}'".format(model)
        findowner_query += ' COLLATE NOCASE'
    else: select += 1
    # if color provided add this to query
    if color!='':
        findowner_query += " AND v.color = '{}'".format(color)
        findowner_query += ' COLLATE NOCASE'
    else: select += 1
    # if year provided add this to query
    if year!='':
        findowner_query += " AND v.year = '{}'".format(year)
    else: select += 1
    # if plate provided add this to query
    if plate!='':
        findowner_query += " AND r.plate = '{}'".format(plate)
    else: select += 1
    # check if at least one characteristics is provided
    if select != 5:
        findowner_query += ' COLLATE NOCASE;'
        cursor.execute(findowner_query)
        vehicles = cursor.fetchall()
        # if no vehicles found
        if (vehicles== None):
            print("No vehicles found")
        # if number of vehicles found greater than or equal to 4 than only display make, model, year, color, and plate
        # and allow user to select the car to obtain owner info
        elif(len(vehicles)>=4):
            for car in range(0,len(vehicles)):
                print("Car number "+str(car)+"\nCar Make: "+str(vehicles[car][0])+"\nCar Model: "+str(vehicles[car][1])+"\nCar Year: "+str(vehicles[car][2])+"\nCar Color: "+str(vehicles[car][3])+"\nCar Plate: "+str(vehicles[car][4])+"\n")
            option = ValidInput('Would you like to select a car(Y/N): ', ["y", "Y", "n", "N"])
            option = str.upper(option)
            if(option == "Y"):
                car = validamount("Enter the car number to view details: ")
                print("Car number "+str(car)+"\nCar Make: "+str(vehicles[car][0])+"\nCar Model: "+str(vehicles[car][1])+"\nCar Year: "+str(vehicles[car][2])+"\nCar Color: "+str(vehicles[car][3])+"\nCar Plate: "+str(vehicles[car][4])+"\nRegistration date: "+str(vehicles[car][5])+"\nRegistration expiry date: "+str(vehicles[car][6])+"\nOwner name: "+str(vehicles[car][7])+"\n")
        # if number of cars are less than 4
        else:
            for car in range(0,len(vehicles)):
                print("Car number "+str(car)+"\nCar Make: "+str(vehicles[car][0])+"\nCar Model: "+str(vehicles[car][1])+"\nCar Year: "+str(vehicles[car][2])+"\nCar Color: "+str(vehicles[car][3])+"\nCar Plate: "+str(vehicles[car][4])+"\nRegistration date: "+str(vehicles[car][5])+"\nRegistration expiry date: "+str(vehicles[car][6])+"\nOwner name: "+str(vehicles[car][7])+"\n")
    # allows officer to perform another task
    guess = input("Would you like to perform another task?...y/n...>")
    if guess == 'y':
        if userType == 'a':
            optionsListAgent(agentMenu(),userType,data)
        else:
            optionsListOfficer(officerMenu(),userType,data)
    else:
        logout()

def logout():
    print("Have a Nice Day")
    print("\n\n")
    print("################")
    main() #relaunches main in order to bring up the login screen once again.

main()
