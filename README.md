# NZ Olympic WebApp Documentation

***

Welcome to the documentation for NZ Olympic Web Application.

## Table of Contents

- [WebApp Structure](#WebApp-Structure)
- [Assumptions](#Assumptions)
- [Discussion](#Discussion)

---

## My Web Structure

NZ Olympic WebApp is a web application using Flask frame.

### Import modules
-Flask
-redirect
-url_for
-flash
-re
-datetime
-mysql.connector
-FieldType
-connect
-render_template
-request


### Function
+getCrusor()
    Establish a database connection and return a cursor object


### Define route and function

| Route             | Method | Function        | Params | Description                                |
|-------------------|--------|-----------------|--------|--------------------------------------------|
| /                 | GET    | home            | -   | Render the home page.                      |
| /list_members     | GET    | listmembers     | -   | Retrieve member list and renders the page. |
| /member/<MemberID>| GET    | member_events   | MemberID | Retrieve event results and related information of the member and renders the page. |
| /list_events      | GET    | listevents      | -   | Retrieve event list and renders the page.  |
| /admin            | GET    | admin           | -   | Render the admin page.                     |
| /admin/search     | GET, POST | admin_search | -   | If memberQuery or eventQuery is provided, it retrieves search results and renders the page "admin_search.html". |
| /admin/add_member | GET, POST | admin_add_member | - |It retrieves team information to render the page;  If a POST request is received, it validates the form inputs, then adds a new member to the database.          |
| /admin/edit_member | GET   | admin_edit_member_list | - | Retrieves member list for editing and renders the page. |
| /admin/<memberID>/edit | GET, POST | admin_edit_member | memberID | If a POST request is received, it validates the form inputs, updates the member details in the database. |
| /admin/add_event  | GET, POST | admin_add_event | - | Retrieves team information to render the page; Adds a new event to the database.           |
| /admin/add_event_stage | GET, POST | admin_add_event_stage | - |Retrieves event information to render the page;  If a POST request is received, it validates the form inputs, inserts the new event into the database. |
| /admin/add_result | GET, POST | admin_add_result | - | Retrieves member and stage information to render the page; If a POST request is received, it validates the form inputs, inserts the new event result into the database. |
| /admin/show_report | GET | admin_show_report | - | It queries the database for medal details and members in teams and renders the page. Display a report of medal tally and members in teams.|

## Assumptions 

1. Assumming "TeamID" in "teams" table is equal to "NZTeam" in "events" table, so when I create the admin_add_event() function, administrator select a team for the added event.
2. The "StageName" in "event_stage" table contain "Qualification", "Final", "Heat 1", there is no clear pattern.Assumming the "StageName" is no rule, so I just check the length.
3. "EventName", "Sport" in "events" table, "Location" in "event_stage" table, "City" in "members" table are similar situation with "StageName". Assumming they are no pattern, so I just check the length.
4. Assumming "PointsScored" larger than 0, so when I add_result I check if "PointsScored" is a positive decimal.


## Design decisions

### 1.Route design

The routes to this site is devided to `/` and `/admin`.  
Public users can visit interfaces start with `/` and administrator can visit interfaces start with `/admin`.  

### 2.Page design

- For public pages extends from `base.html` 
- For administrator pages extends from `admin.html`

### 3.GET and POST methods

The GET method is used for displaying the frontend page, and the POST method is used for submitting form data in my web application.
The function of these route below use both GET and POST methods. 
- /admin/search
- /admin/add_member
- /admin/<memberID>/edit
- /admin/add_event
- /admin/add_event_stage
- /admin/add_result
In these functions I use 'if request.method =="POST"' to detect POST method. Because these function get data from form.

## Discussion

### 1. Database changes

In my opinion, there are two ways.
1. Add a new column for each table, and define which number means Winter Olympic and which number means Summer Olympic.
For example, '1' means Summer Olympic, '2' means Winter Olympic. In "members" table:
|memberID|TeamID|FirstName|LastName|City|Birthdate|OlympicID|
|1|103|Atticus|Finch|Christchurch|2000-01-01|1|
||||||||
2. Add tables for different Olympic, for example:

```sql
CREATE TABLE IF NOT EXISTS summer_members
(
MemberID INT auto_increment PRIMARY KEY NOT NULL,
TeamID INT NOT NULL,
FirstName VARCHAR(50) NOT NULL,
LastName VARCHAR(50) NOT NULL,
City VARCHAR(30),
Birthdate DATE NOT NULL,
FOREIGN KEY (TeamID) REFERENCES teams(TeamID)
ON UPDATE CASCADE
ON DELETE CASCADE
);
```


### 2. Front end changes

Add a Olympic column when listing members and events and so on. The `/list_events` route will displays like:
|OlympicName|EventID|EventName|Sport|NZTeam|
|----|----|----|----|----|
|**Winter Olympic**|3|Big Air|Snowboarding|101|
|**Summer Olympic**|12|...|...|...|

Also when you display the information or transfer the data, should pay attention to the column. For example to use EventID:
Before:
'''Jinja
{% Event[0]%}
'''
After:
'''Jinja
{% Event[1]%}
'''

### 3. Backend changes

The query SQL should be change when you want to operate the database. For example:

```sql
SELECT * FROM members WHERE OlympicName == "Winter Olympic"
```

