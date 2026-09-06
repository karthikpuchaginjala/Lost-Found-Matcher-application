
from dbconnect import connection

def register_user():
    name=input("Enter name: ")
    phone=int(input("Enter phone: "))
    email=input("Enter email: ")
    password=input("Create password: ")
    c=connection()
    cursor=c.cursor()
    query="insert into users(name,phone,email,password) values(%s,%s,%s,%s)"
    cursor.execute(query,(name,phone,email,password))
    c.commit()
    print("Registration successful!")
    cursor.close()
    c.close()

def login_user():
    email=input("Enter email: ")
    password=input("Enter password: ")
    c=connection()
    cursor=c.cursor()
    query="select user_id,name from users where email=%s and password=%s"
    cursor.execute(query,(email,password))
    user=cursor.fetchone()
    cursor.close()
    c.close()
    if user:
        print("Login successful!")
        print(f"Welcome {user[1]}!")
        return user[0]
    else:
        print("Invalid email or password.")
        return None

def report_item(user_id):
    print("========== REPORT ITEM ==========")
    item_type=input("Enter item type (LOST/FOUND): ").upper()
    if item_type not in ("LOST","FOUND"):
        print("Invalid item type.")
        return
    category=input("Enter category: ")
    item_name=input("Enter item name: ")
    description=input("Enter description: ")
    color=input("Enter color: ")
    location=input("Enter location: ")
    date_reported=input("Enter date you are reporting (YYYY-MM-DD): ")
    imei=None
    if category.lower() in ("phone","mobile"):
        imei=input("Enter IMEI number: ")
    c=connection()
    cursor=c.cursor()
    query="""insert into items(user_id,item_type,category,item_name,description,color,location,date_reported,imei)
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    values=(user_id,item_type,category,item_name,description,color,location,date_reported,imei)
    cursor.execute(query,values)
    item_id=cursor.lastrowid
    c.commit()
    print("Item reported successfully!")
    print(f"Your report ID is: {item_id}")
    cursor.close()
    c.close()

def my_reports(user_id):
    c=connection()
    cursor=c.cursor()
    query="""select item_id,item_type,category,item_name,color,location,date_reported,status
    from items where user_id=%s"""
    cursor.execute(query,(user_id,))
    items=cursor.fetchall()
    print("========== MY REPORTS ==========")
    if not items:
        print("You have no reports.")
    else:
        for item in items:
            print("--------------------------------")
            print(f"Report ID : {item[0]}")
            print(f"Type      : {item[1]}")
            print(f"Category  : {item[2]}")
            print(f"Name      : {item[3]}")
            print(f"Color     : {item[4]}")
            print(f"Location  : {item[5]}")
            print(f"Date      : {item[6]}")
            print(f"Status    : {item[7]}")
    cursor.close()
    c.close()

def calculate_match_score(lost,found):
    score=0
    total=0
    if lost[3] and found[3]:
        total+=25
        if lost[3].lower()==found[3].lower():
            score+=25
    if lost[4] and found[4]:
        total+=20
        if lost[4].lower()==found[4].lower():
            score+=20
    if lost[6] and found[6]:
        total+=15
        if lost[6].lower()==found[6].lower():
            score+=15
    if lost[7] and found[7]:
        total+=15
        if lost[7].lower()==found[7].lower():
            score+=15
    if lost[9] and found[9]:
        total+=25
        if lost[9]==found[9]:
            score+=25
    if total==0:
        return 0
    percentage=(score/total)*100
    return percentage

def view_my_matches(user_id):
    c=connection()
    cursor=c.cursor()
    query="select * from items where user_id=%s and item_type='LOST' and status='ACTIVE'"
    cursor.execute(query,(user_id,))
    lost_items=cursor.fetchall()
    query="select * from items where item_type='FOUND' and status='ACTIVE'"
    cursor.execute(query)
    found_items=cursor.fetchall()
    print("========== MY POTENTIAL MATCHES ==========")
    for lost in lost_items:
        print("My lost item:",lost[4])
        for found in found_items:
            score=calculate_match_score(lost,found)
            if score>=40:
                print("-------------------------")
                print("Possible match!")
                print("Found item ID:",found[0])
                print("Found item:",found[4])
                print("Location:",found[7])
                print("Score:",round(score,2),"%")
                if score>=80:
                    print("Result: Strong potential match")
                elif score>=60:
                    print("Result: Possible match")
                else:
                    print("Result: Weak potential match")
    cursor.close()
    c.close()

def request_finder_contact(user_id):
    found_item_id=int(input("Enter found item ID: "))
    c=connection()
    cursor=c.cursor()
    query="select user_id,item_type,item_name from items where item_id=%s"
    cursor.execute(query,(found_item_id,))
    item=cursor.fetchone()
    if not item:
        print("Found item does not exist.")
        cursor.close()
        c.close()
        return
    if item[1]!="FOUND":
        print("Invalid item ID. Please enter a FOUND item ID.")
        cursor.close()
        c.close()
        return
    if item[0]==user_id:
        print("You cannot request your own contact.")
        cursor.close()
        c.close()
        return
    unlock=input("Can you unlock the phone? (yes/no): ")
    if unlock.lower()!="yes":
        print("You cannot send the request.")
        cursor.close()
        c.close()
        return
    answer=input("Do you want to send a request for the finder's contact? (yes/no): ")
    if answer.lower()=="yes":
        query="insert into requests(lost_user_id,found_item_id) values(%s,%s)"
        cursor.execute(query,(user_id,found_item_id))
        c.commit()
        print("Request sent to the finder!")
    else:
        print("Request cancelled.")
    cursor.close()
    c.close()

def check_contact(user_id):
    c=connection()
    cursor=c.cursor()
    query="select item_id from items where user_id=%s and item_type='FOUND'"
    cursor.execute(query,(user_id,))
    found_items=cursor.fetchall()
    if found_items:
        print("========== CONTACT REQUESTS ==========")
        for item in found_items:
            found_item_id=item[0]
            query="select request_id,lost_user_id from requests where found_item_id=%s and status='PENDING'"
            cursor.execute(query,(found_item_id,))
            request=cursor.fetchone()
            if request:
                request_id=request[0]
                query="select item_name from items where item_id=%s"
                cursor.execute(query,(found_item_id,))
                item_name=cursor.fetchone()
                print("-------------------------")
                print("Item:",item_name[0])
                print("A lost person wants your contact details.")
                answer=input("Do you want to share your contact number? (yes/no): ")
                if answer.lower()=="yes":
                    query="update requests set status='ACCEPTED' where request_id=%s"
                    cursor.execute(query,(request_id,))
                    c.commit()
                    print("Contact request accepted!")
                else:
                    query="update requests set status='REJECTED' where request_id=%s"
                    cursor.execute(query,(request_id,))
                    c.commit()
                    print("Contact request rejected.")
            else:
                print("No contact requests.")
    else:
        print("========== MY CONTACT REQUEST ==========")
        query="""select found_item_id,status
        from requests
        where lost_user_id=%s
        order by request_id desc"""
        cursor.execute(query,(user_id,))
        request=cursor.fetchone()
        if not request:
            print("You have not sent any contact request.")
        else:
            found_item_id=request[0]
            status=request[1]
            query="select item_name from items where item_id=%s"
            cursor.execute(query,(found_item_id,))
            item=cursor.fetchone()
            print("Found Item:",item[0])
            if status=="PENDING":
                print("Status: PENDING")
                print("Waiting for the finder to respond.")
            elif status=="REJECTED":
                print("Status: REJECTED")
                print("Finder rejected your request.")
            else:
                query="select user_id from items where item_id=%s"
                cursor.execute(query,(found_item_id,))
                finder=cursor.fetchone()
                query="select phone from users where user_id=%s"
                cursor.execute(query,(finder[0],))
                phone=cursor.fetchone()
                print("Status: ACCEPTED")
                print("Finder Contact:",phone[0])
    cursor.close()
    c.close()

def resolve_item(user_id):
    item_id=int(input("Enter your report ID: "))
    c=connection()
    cursor=c.cursor()
    query="update items set status='RESOLVED' where item_id=%s and user_id=%s"
    cursor.execute(query,(item_id,user_id))
    c.commit()
    if cursor.rowcount>0:
        print("Report marked as resolved.")
    else:
        print("Report not found or does not belong to you.")
    cursor.close()
    c.close()

