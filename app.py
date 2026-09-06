from functions import (register_user,
login_user,
report_item,
my_reports,
view_my_matches,
request_finder_contact,
check_contact,
resolve_item
)

print("==============================================")
print("         LOST & FOUND ITEM MATCHER")
print("==============================================")

while True:
    print("\n========== MAIN MENU ==========")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice=int(input("Enter your choice: "))

    if choice==1:
        register_user()

    elif choice==2:
        user_id=login_user()

        if user_id:
            while True:
                print("\n========== USER MENU ==========")
                print("1. Report Lost Item")
                print("2. Report Found Item")
                print("3. My Reports")
                print("4. Check My Matches")
                print("5. Request Finder Contact")
                print("6. Check Contact Requests")
                print("7. Mark Report Resolved")
                print("8. Logout")
                choice=int(input("Enter your choice: "))

                if choice==1:
                    report_item(user_id)
                elif choice==2:
                    report_item(user_id)
                elif choice==3:
                    my_reports(user_id)
                elif choice==4:
                    view_my_matches(user_id)
                elif choice==5:
                    request_finder_contact(user_id)
                elif choice==6:
                    check_contact(user_id)
                elif choice==7:
                    resolve_item(user_id)
                elif choice==8:
                    break
    elif choice==3:
        print("Thank you for using Lost & Found Matcher!")
        break

    else:
        print("Invalid choice.")
