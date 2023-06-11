NZ Olympic WebApp Documentation

Welcome to the documentation for NZ Olympic Web Application.

Table of Contents

WebApp Structure
Assumptions
Discussion

WebApp Structure

The NZ Olympic WebApp is built using the Flask framework. It consists of the following modules:

Flask
render_template
request
redirect
url_for
re
datetime
mysql.connector
FieldType
connect

Function

getCursor()
This function establishes a database connection and returns a cursor object.

Routes and Functions

Routes and Functions

Route	Method	Function	Params	Description
/	GET	home	-	Renders the home page.
/listmembers	GET	listmembers	-	Retrieves the member list from the database and renders the member list page.
listevents	GET	listevents	-	Retrieves the event list from the database and renders the event list page.
/member/<memberid>	GET	memberdetails	memberid	Retrieves the details of a specific member from the database based on the provided member ID and renders the member details page.
/admin	GET	admin	-	Renders the admin page.
/admin_search	GET	admin_search	-	Retrieves search results based on the provided event and member queries, and renders the admin search page.
/add_member	GET, POST	add_member	-	If a POST request is received, it validates the form inputs and adds a new member to the database. If a GET request is received, it retrieves team information to render the add member page.
/add_event	GET, POST	add_event	-	If a POST request is received, it validates the form inputs and adds a new event to the database. If a GET request is received, it retrieves team information to render the add event page.
/event_stage	GET, POST	event_stage	-	If a POST request is received, it validates the form inputs and adds a new event stage to the database. If a GET request is received, it retrieves event information to render the add event stage name.
/add_scores	POST	add_scores	-	Adds scores to the database based on the provided event stage and score.
/reports	GET	generate_reports	-	Retrieves data for generating reports and renders the reports page.

Assumptions

The database connection details (host, user, password, database) are defined in a separate file named "connect.py".
The "getCursor()" function is used to establish a database connection and return a cursor object.
The "/listmembers" route retrieves the member list from the database and renders the "memberlist.html" template, displaying member details.
The "/listevents" route retrieves the event list from the database and renders the "eventlist.html" template, displaying event details.
The "/member/<memberid>" route retrieves the details of a specific member from the database based on the provided member ID and renders the "memberdetails.html" template, displaying member details and related event information

Design Decisions

1. Route Design
The routes in this web application are divided into two main sections: public routes and administrator routes.

Public Routes: These routes are accessible to all users and start with /. Users can access interfaces and pages provided by these routes.
Administrator Routes: These routes are only accessible to administrators and start with /admin. Administrators can access interfaces and pages provided by these routes, which are specifically designed for administrative tasks.

2. Page Design
The page design follows a modular approach using template inheritance.

Public Pages: Public pages extend the base.html template, which serves as the base layout for all public interfaces.
Administrator Pages: Administrator pages extend the admin.html template, which provides the layout and design specific to administrative tasks.

3. GET and POST Methods
The GET and POST methods are used in the web application for different purposes.

GET Method: The GET method is used to retrieve and display frontend pages. Users can access and view information through GET requests.
POST Method: The POST method is used to submit form data and perform actions that modify the backend data. It is used in functions that handle form submissions.

The following routes utilize both GET and POST methods:

/admin/search
/admin/add_member
/admin/<memberID>/edit
/admin/add_event
/admin/add_event_stage
/admin/add_result
In these functions, the code checks the request method using if request.method == "POST" to detect and handle POST requests. This allows the functions to retrieve data from the submitted form.

1. Database Changes
Regarding the database changes, there are two suggested approaches:

Add a New Column: Add a new column to each relevant table to indicate the Olympic type (Summer or Winter). For example, you can add an "OlympicID" column where a specific number represents a Summer Olympic and a different number represents a Winter Olympic. The column can be used to distinguish between the two types of events or members.

Add Separate Tables: Create separate tables for each Olympic type, such as "summer_members" and "winter_members". This approach allows you to store data specific to each Olympic type in separate tables.


