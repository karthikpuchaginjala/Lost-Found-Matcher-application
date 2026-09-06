# Lost & Found Item Matcher

A menu-driven **Lost & Found Item Matcher** built using **Python and MySQL**. The application allows users to register, report lost or found items, view their reports, identify potential matches using a match score, request a finder's contact details, respond to contact requests, and mark reports as resolved.

## Features

- User registration
- User login
- Report a lost item
- Report a found item
- View personal reports
- Find potential matches between lost and found items
- Calculate a match percentage based on item details
- Request the finder's contact details
- Finder can accept or reject a contact request
- Share the finder's registered phone number after acceptance
- Mark a report as resolved
- Logout

## Technologies Used

- **Python**
- **MySQL**
- **PyMySQL**

## Project Structure

```text
pro-lostmatcher/
│
├── app.py
├── functions.py
├── dbconnect.py
└── README.md
```

### `app.py`

Contains the main menu and user menu. It calls the functions for registration, login, reporting items, checking matches, contact requests, and resolving reports.

### `functions.py`

Contains the main application functions:

- `register_user()`
- `login_user()`
- `report_item()`
- `my_reports()`
- `calculate_match_score()`
- `view_my_matches()`
- `request_finder_contact()`
- `check_contact()`
- `resolve_item()`

### `dbconnect.py`

Contains the MySQL connection function used by the application.

## Application Flow

```text
MAIN MENU
│
├── Register
│
├── Login
│   │
│   └── USER MENU
│       ├── Report Lost Item
│       ├── Report Found Item
│       ├── My Reports
│       ├── Check My Matches
│       ├── Request Finder Contact
│       ├── Check Contact Requests
│       ├── Mark Report Resolved
│       └── Logout
│
└── Exit
```

## Matching System

The application compares details of a user's lost item with active found items.

The current matching logic considers:

| Detail | Weight |
|---|---:|
| Item name | 25% |
| Description | 20% |
| Location | 15% |
| Date reported | 15% |
| IMEI | 25% |

A potential match is displayed when the calculated score is **40% or higher**.

The result is classified as:

- **80% or above** → Strong potential match
- **60% to below 80%** → Possible match
- **40% to below 60%** → Weak potential match

## Contact Request Process

The contact-sharing process is designed so that the finder decides whether to share their registered contact number.

```text
Lost User
   │
   ├── Finds a potential match
   │
   ├── Enters Found Item ID
   │
   ├── Confirms phone unlocking
   │
   └── Sends contact request
             │
             ▼
          Finder
             │
             ├── Accept
             │      │
             │      └── Lost user can see finder contact
             │
             └── Reject
                    │
                    └── Lost user sees rejected status
```

## Database

The application uses a MySQL database named:

```sql
lost_foundd
```

The main tables are:

- `users`
- `items`
- `matches`
- `requests`

### `users`

Stores registered user information such as name, phone, email, and password.

### `items`

Stores lost and found item information, including category, item name, description, color, location, date reported, IMEI, and status.

### `matches`

Stores lost-item/found-item match information, including score and match status.

### `requests`

Stores requests made by lost users for a finder's contact details.

## Database Setup

Create the database and tables in MySQL before running the application.

The database connection in `dbconnect.py` should be configured for your own local MySQL installation.

**Important:** Do not publish your real MySQL password or other credentials on GitHub or LinkedIn. Replace local credentials with your own secure configuration before sharing the project publicly.

## Installation

### 1. Install Python

Make sure Python is installed on your system.

### 2. Install PyMySQL

Open Command Prompt or Terminal:

```bash
pip install pymysql
```

### 3. Create the MySQL Database

Create the `lost_foundd` database and the required tables using your MySQL SQL script.

### 4. Configure the Database Connection

Update `dbconnect.py` with your local MySQL username, password, host, and database name.

### 5. Run the Application

From the project directory:

```bash
python app.py
```

## Example Workflow

### Step 1: Register

```text
1. Register
Enter name
Enter phone
Enter email
Create password
```

### Step 2: Login

```text
2. Login
Enter email
Enter password
```

### Step 3: Report a Lost Item

```text
1. Report Lost Item
```

Enter the item details. For a phone/mobile category, the application also asks for an IMEI number.

### Step 4: Check Matches

```text
4. Check My Matches
```

The application displays potential matches and their scores.

Example:

```text
Possible match!
Found item ID: 2
Found item: iphone 13
Location: hyderabad
Score: 60.0 %
Result: Possible match
```

### Step 5: Request Finder Contact

```text
5. Request Finder Contact
```

The lost user enters the found item ID, confirms the phone-unlocking condition, and sends a contact request.

### Step 6: Finder Responds

The finder logs in and selects:

```text
6. Check Contact Requests
```

The finder can accept or reject the request.

### Step 7: Lost User Checks Response

After acceptance, the lost user can check the contact status and view the finder's registered phone number.

## Current Limitations

This is a console-based student project and can be improved in future versions.

Possible improvements:

- Password hashing
- Better input validation
- Exception handling for database errors
- Prevention of duplicate contact requests
- More advanced matching logic
- Separate GUI or web interface
- Better date validation
- More detailed match records
- Secure environment-variable based database credentials

## Future Scope

The project can be extended into a web or mobile application where users can upload item images and use more advanced matching techniques.

## Author

**Karthik**

© 2026 Karthik. All rights reserved.
