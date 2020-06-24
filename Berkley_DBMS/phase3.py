import sys
import os
from bsddb3 import db
from datetime import datetime
import re

#database creation
termsDB = db.DB()
emailsDB = db.DB()
datesDB = db.DB()
recsDB = db.DB()

termsDB.open('te.idx',None, db.DB_BTREE, db.DB_RDONLY)
emailsDB.open('em.idx',None, db.DB_BTREE, db.DB_RDONLY)
datesDB.open('da.idx',None, db.DB_BTREE, db.DB_RDONLY)
recsDB.open('re.idx',None, db.DB_HASH, db.DB_RDONLY)

#database cursors
tcursor = termsDB.cursor()
ecursor = emailsDB.cursor()
dcursor = datesDB.cursor()
rcursor = recsDB.cursor()

def main():
    # main system
    print("Welcome")
    print("1. Enter a Query")
    print("2. Quit")
    #query or quit
    choice = int(input("Please enter a number for the desired task...>"))
    validOptions = [1,2]
    active = True
    quest = True
    #check if valid
    while active:
        if choice not in validOptions:
            print("Please enter a valid Option")
        else: 
            active = False
            userOption(choice)
            while quest:
                mode = input("Enter desired vewing mode, full or brief...>")#full or brief
                if mode == "full":
                    lay = layout("full")
                    quest = False
                    goo = "good"
                elif mode == "brief":
                    lay = layout("brief")
                    quest = False
                    goo = "good"
                else:
                    print("Invalid form entered, please try again")
    # query the input
    queryPrompt(lay)
#check if valid
def layout(string):
    if string == "brief":
        return True
    else:
        return False
# query input and case sensitivity
def queryPrompt(lay):
    desiredQuery = input("Input the QUERY you would like to perform?...>").lower()
    querySplit(desiredQuery,lay)
# check if valid
def userOption(data):
    choice = str(data)
    if choice == "1":
        return 1
    elif choice == "2":
        quit()
# splitting and handling queries
def querySplit(query,lay):

    #date - Newer, older or exact
    #Subj - containing word
    #body - containing word
    #containing - ___%
    #to email
    # from email 
    #bcc
    #cc
    #subj / body
    userQuery = []
    for words in query.split():
        userQuery.append(words)
    #---------------------------------handle Subj---------------------------------
    # for further understand look at "handle date" all the logic is the same
    finalSub = []
    for word in userQuery:
        if "subj" in word: 
            if len(word) == 5: 
                date = int(userQuery.index(word))+1 
                date1 = userQuery[date]
                FF = str(word)+str(date1)
                userQuery.remove(word)
                userQuery.remove(word+1)
                
                finalSub.append(FF)

            elif len(word) < 5:
                symbol = int(userQuery.index(word))+1
                symbol1 = userQuery[symbol]
                date = symbol + 1
                try:
                    date2 = userQuery[date]
                except Exception:
                    AA = str(word) + str(symbol1)
                AA = str(word) + str(symbol1)
                if len(AA) == 5 or len(AA)<5:
                    AA = AA + str(date2)
                else:
                    AA = AA
                finalSub.append(AA)
                userQuery.remove('subj')

            elif len(word) > 5:
                finalSub.append(str(word))

    
    #---------------------------------handle Body---------------------------------
    # for further understand look at "handle date" all the logic is the same
    finalBod = []
    for word in userQuery:
        if "body" in word:
            if len(word) == 5:
                date = int(userQuery.index(word))+1
                date1 = userQuery[date]
                FF = str(word)+str(date1)
                finalBod.append(FF)

            elif len(word) < 5:
                symbol = int(userQuery.index(word))+1
                symbol1 = userQuery[symbol]
                date = symbol + 1
                try:
                    date2 = userQuery[date]
                except Exception:
                    AA = str(word) + str(symbol1)
                AA = str(word) + str(symbol1)
                if len(AA) == 5 or len(AA)<5:
                    AA = AA + str(date2)
                else:
                    AA = AA
                finalBod.append(AA)
                userQuery.remove('body')

            elif len(word) > 5:
                finalBod.append(str(word))

    #---------------------------------handle Date---------------------------------
    # for further understand look at "handle date" all the logic is the same
    finalDat = []
    for word in userQuery:
        if "date" in word: #handle date, find date in word
            if len(word) == 5: #so date is "date:". THe len(date:) = 5
                date = int(userQuery.index(word))+1 #the date itself is the index of (date:) + 1. This is because if the lend(date:) = 5, then the next term will be the date
                date1 = userQuery[date]
                FF = str(word)+str(date1)  #adding "date:" with "yyyy/mm/dd"
                finalDat.append(FF)

            elif len(word) < 5: #so date is "date"
                symbol = int(userQuery.index(word))+1 #symbol is either ";" or ";yyyy/mm/dd"
                symbol1 = userQuery[symbol]
                date = symbol + 1 #if symbol is ";", then the date is the next index
                try:
                    date2 = userQuery[date] #if not out of range, then date2 will get the date
                except Exception:
                    AA = str(word) + str(symbol1) #if out of range, add "date" with ":yyyy/mm/dd"
                AA = str(word) + str(symbol1)
                if len(AA) == 5 or len(AA)<5: #if len(AA) == 5, meaning if AA = "date:", then we add str(date2) which is the date
                    AA = AA + str(date2)
                else:
                    AA = AA
                finalDat.append(AA)
                userQuery.remove("date") #removing the date so the if there's duplicate, the second time the loops run, it will not find the first index but go to the next

            elif len(word) > 5: #date:yyyy/mm/dd
                finalDat.append(str(word))
            
              
                

    #---------------------------------handle email------------------------------
    # for further understand look at "handle date" all the logic is the same
    finalEmato = []
    list1=[]
    for word in userQuery:
        if "to" in word: #follow the same logic as handling the date
            if len(word) == 3: 
                mail = int(userQuery.index(word)) + 1
                mail1 = userQuery[mail]
                PP = str(word) + str(mail1)
                list1.append(PP)

            elif len(word) < 3:
                symbol = int(userQuery.index(word)) + 1
                symbol1 = userQuery[symbol]
                mail2 = symbol + 1
                try:
                    mail3 = userQuery[mail2]
                except Exception:
                    DD = str(word) + str(symbol1)
                DD = str(word) + str(symbol1)
                if len(DD) == 3 or len(DD)<3:
                    DD = DD + str(mail3)
                else:
                    DD = DD
                list1.append(DD)
                userQuery.remove('to')
            
            elif len(word) > 3:
                list1.append(str(word))

    for item in list1:
        if "to" and "@" in item:
            finalEmato.append(item)
    
    list_3 = []
    finalEmafrom = []
    for word in userQuery:
        if "from" in word:
            if len(word) == 5:
                mail = int(userQuery.index(word)) + 1
                mail1 = userQuery[mail]
                PP = str(word) + str(mail1)
                list_3.append(PP)

            elif len(word) < 5:
                symbol = int(userQuery.index(word)) + 1
                symbol1 = userQuery[symbol]
                mail2 = symbol + 1
                try:
                    mail3 = userQuery[mail2]
                except Exception:
                    DD = str(word) + str(symbol1)
                DD = str(word) + str(symbol1)
                if len(DD) == 5 or len(DD)<5:
                    DD = DD + str(mail3)
                else:
                    DD = DD
                list_3.append(DD)
                userQuery.remove('from')

            elif len(word) > 5: 
                list_3.append(str(word))

    for item in list_3:
        if "from" and "@" in item:
            finalEmafrom.append(item)


    #---------------------------------handle cc---------------------------------
    # for further understand look at "handle date" all the logic is the same
    list4=[]
    finalCc = []
    for word in userQuery: #follow the same logic as handling the date
        if "cc" in word:
            #print(word) #cc: cc
            if len(word) == 3:
                mail = int(userQuery.index(word)) + 1
                mail1 = userQuery[mail]
                PP = str(word) + str(mail1)
               # print(PP)
                list4.append(PP)

            elif len(word) < 3:
                symbol = int(userQuery.index(word)) + 1
                
                symbol1 = userQuery[symbol]
                mail2 = symbol + 1
              
                try:
                    mail3 = userQuery[mail2]
                except Exception:
                    DD = str(word) + str(symbol1)
                DD = str(word) + str(symbol1)
              
                if len(DD) == 3 or len(DD)<3:
                    DD = DD + str(mail3)
                    
                else:
                    DD = DD
                list4.append(DD)
                userQuery.remove('cc')
            
            elif len(word) > 3:
                list4.append(str(word))

    for item in list4:
        if "cc" and "@" in item:
            finalCc.append(item) 

    #---------------------------------handle %---------------------------------
    # check if percent at the end of the word
    # append to the list
    finalCon = []
    for word in userQuery:
        if "%" in word:
            finalCon.append(word)

    #---------------------------------handle bcc ----------------------------------
    # for further understand look at "handle date" all the logic is the same
    list5=[]
    finalBcc = []
    for word in userQuery: #follow the same logic as handling the date
        if "bcc" in word:
            #print(word) #cc: cc
            if len(word) == 4:
                mail = int(userQuery.index(word)) + 1
                mail1 = userQuery[mail]
                PP = str(word) + str(mail1)
               # print(PP)
                list5.append(PP)

            elif len(word) < 4:
                symbol = int(userQuery.index(word)) + 1
               
                symbol1 = userQuery[symbol]
                mail2 = symbol + 1
                
                try:
                    mail3 = userQuery[mail2]
                except Exception:
                    DD = str(word) + str(symbol1)
                DD = str(word) + str(symbol1)
              
                if len(DD) == 4 or len(DD)<4:
                    DD = DD + str(mail3)
                 
                else:
                    DD = DD
                list5.append(DD)
                userQuery.remove('bcc')
            
            elif len(word) > 4:
                list5.append(str(word))
    

    
    for item in list5:
        if "bcc" and "@" in item:
            finalBcc.append(item)


    #----------------handle Body / subject where not specifed---------------------
    # for further understand look at "handle date" all the logic is the same
    keyWords = ["subj","body","date","bcc","cc","to","from", "%", ">", ">=", "<", "=<",":","subj:","body:","date:","bcc:","cc:","to:","from:","date<","date>","date<=","date>="] #all possible keyword combinations
    finalList = []
    finalSubBod = []
    terms = []
    emails = []
    
   #adds all the final lists from the for loops and creates a master list of all query parts which will be used in the subj or body parts.
   #adds all the body / subj to the terms portion, 
   #adda all the bcc / to / from / cc to the email portion 
   #adds all the dates to the date portion
    for i in finalBod:
        finalList.append(i)
        terms.append(i) #terms list for queries
    for i in finalSub:
        finalList.append(i)
        terms.append(i) #terms list for queries
    for i in finalDat:
        finalList.append(i) #Dates list for queries
    for i in finalEmato:
        finalList.append(i)
        emails.append(i) #emails list for queries
    for i in finalEmafrom:
        finalList.append(i)
        emails.append(i) #emails list for queries
    for i in finalCc:
        finalList.append(i)
        emails.append(i) #emails list for queries
    for i in finalBcc:
        finalList.append(i)
        emails.append(i) #emails list for queries
    for i in finalCon:
        finalList.append(i)
        terms.append(i)#terms list for queries
    words=userQuery 
    for i in userQuery: # removes all the words that are in the user query that are not in the keywords which allows the remainin terms in to considered into the subj / body part where it is terms query
        if (i in keyWords):
            words.remove(i)
    for i in words:
        for x in finalList:
            if(i in x):
                words.remove(i)
    for i in words:
        terms.append(i)
    #print(words)
    maindata=setup()
    if(len(terms)>0):
        for i in terms:
            terms_query(i,maindata)
    if(len(emails)>0):
        for i in emails:
            email_query(i,maindata)
    if(len(finalDat)>0):
        for i in finalDat:
            date_query(i,maindata)
    getResults(lay,maindata)
def setup():
    #create maindata file with all row ids
    maindata = set()
    iter = rcursor.first()
    while iter:
        maindata.add(iter[0].decode())
        iter = rcursor.next()
    return maindata
def date_query(datein,maindata):
    # split date figure out the operator
    if len(datein.split(":"))>1:
        x=datein.split(":")
        operator=":"
    elif len(datein.split("<="))>1:
        x=datein.split("<=")
        operator="<="
    elif len(datein.split(">="))>1:
        x=datein.split(">=")
        operator=">="
    elif len(datein.split(">"))>1:
        operator=">"
        x=datein.split(">")
    elif len(datein.split("<"))>1:
        operator="<"
        x=datein.split("<")
    
    date = datetime.strptime(x[1],"%Y/%m/%d")
    iter = dcursor.first()
    date_ID = set()
    # run through the database and save row ids for rec that satisfies
    while iter:
        insert = False
        iterdate=datetime.strptime(iter[0].decode(),"%Y/%m/%d")
        if (operator==":"):
            if iterdate==date: insert=True
        elif (operator==">"):
            if iterdate>date: insert=True
        elif (operator==">="):
            if iterdate>=date: insert=True
        elif (operator=="<"):
            if iterdate<date: insert=True
        elif (operator=="<="):
            if iterdate<=date: insert=True
        else:
            print("Invalid Operator")
            break
        if insert: date_ID.add(iter[1].decode())
        iter = dcursor.next()
    maindata = maindata.intersection_update(date_ID)
def terms_query(termin,maindata):
    #split terms to determine whether subj body or prefix or single word
    if(len(termin.split(":"))>1):
        x=termin.split(":")
        typ=x[0]
        term=x[1]
    elif("%" in termin):
        typ="pre"
        term=termin[:-1]
    else:
        term=termin
        typ=""
    term_ID = set()
    iter = tcursor.first()
    if typ =="body":
        typ="b"
    elif typ=="subj":
        typ="s"
    # run through the database and save row ids for rec that satisfies
    while iter:
        field=(iter[0].decode("utf-8")).split("-",1)
        if(field[0]==typ):
            if field[1]==term:
                term_ID.add(iter[1].decode())
        elif(typ=="pre"):
            if(field[1].startswith(term)):
                term_ID.add(iter[1].decode())
        elif(typ==""):
            if(field[1]==term):
                term_ID.add(iter[1].decode())
        iter = tcursor.next()
    maindata = maindata.intersection_update(term_ID)
def email_query(emailin,maindata):
    # split email to determine to from bcc or cc
    x=emailin.split(":")
    typ=x[0]
    email=x[1]
    iter = ecursor.first()
    email_ID=set()
    #  run through the database and save row ids for rec that satisfies
    while iter:
        field=(iter[0].decode("utf-8")).split("-")
        #print(field[0])
        if(field[0]==typ):
            if email in (iter[0].decode()):
                email_ID.add(iter[1].decode())
        iter = ecursor.next()
    maindata = maindata.intersection_update(email_ID)

def getResults(typ,maindata):
    #Prints all the results from the records database that correspond to id's mast_ids 
    if(typ==False):
        for key in maindata:
            rec = recsDB.get(str(key).encode())
            print(rec)
        print("End of results.")
    else:
        for key in maindata:
            rec = recsDB.get(str(key).encode())
            title = re.search("<subj>(.*)</subj>", str(rec)).group(1)
            print(key, title)

        print("End of results.")
    main()

main()