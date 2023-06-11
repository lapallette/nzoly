NZ Olympic WebApp Documentation

Welcome to the documentation for NZ Olympic Web Application.

Table of Contents

WebApp Structure
Assumptions
Discussion

WebApp Structure

NZ Olympic WebApp is a web application using the Flask framework.

Imported Modules
The following modules are imported in the application:

Flask
redirect
url_for
flash
re
datetime
mysql.connector
FieldType
connect
render_template
request
Functions

The application includes the following function:

getCursor(): This function establishes a connection to the database and returns a cursor object for executing SQL queries.

Defined Routes and Functions
The table below outlines the defined routes and their corresponding functions:

Route	Method	Function	Params	Description
/	GET	home	-	Renders the home page.
/list_members	GET	listmembers	-	Retrieves the member list and renders the page.

/member/<MemberID>	GET	member_events	MemberID	Retrieves event results and related information for a member and renders the page.
/list_events	GET	listevents	-	Retrieves the event list and renders the page.
/admin	GET	admin	-	Renders the admin page.
/admin/search	GET, POST	admin_search	-	Retrieves search results if memberQuery or eventQuery is provided, and renders the admin_search.html page.

/admin/add_member	GET, POST	admin_add_member	-	Renders the page to retrieve team information; if a POST request is received, it validates the form inputs and adds a new member to the database.
/admin/edit_member	GET	admin_edit_member_list	-	Retrieves the member list for editing and renders the page.

/admin/<memberID>/edit	GET, POST	admin_edit_member	memberID	If a POST request is received, it validates the form inputs and updates the member details in the database.
/admin/add_event	GET, POST	admin_add_event	-	Renders the page to retrieve event information; adds a new event to the database.

/admin/add_event_stage	GET, POST	admin_add_event_stage	-	Renders the page to retrieve event information; if a POST request is received, it validates the form inputs and inserts the new event into the database.

/admin/add_result	GET, POST	admin_add_result	-	Renders the page to retrieve member and stage information; if a POST request is received, it validates the form inputs and inserts the new event result into the database.

admin/show_report	GET	admin_show_report	-	Queries the database for medal details and members in teams, and renders the page to display a report of the medal tally and members in teams.


Assumptions

During the development of the web application, the following assumptions were made:

TeamID and NZTeam: It is assumed that "TeamID" in the "teams" table corresponds to "NZTeam" in the "events" table. This assumption allows the admin_add_event() function to prompt the administrator to select a team for the added event.
StageName, EventName, Sport, Location, and City: The fields "StageName" in the "event_stage" table, "EventName" and "Sport" in the "events" table, and "Location" and "City" in the "members" table were assumed to have no specific pattern or rules. Therefore, their length was checked rather than applying any specific pattern validation.

Positive PointsScored: It is assumed that the "PointsScored" field in the "event_stage" table should be a positive decimal value. Therefore, when adding a result in the admin_add_result() function, the code checks if "PointsScored" is a positive decimal.

Design Decisions

The following design decisions were made during the development of the web application:
Route Design: The routes to the site are divided into two main categories: routes starting with "/" are accessible to public users, while routes starting with "/admin" are reserved for administrators.
Page Design: The application uses separate HTML templates for public and administrator pages. Public pages extend from the "base.html" template, while administrator pages extend from the "admin.html" template.
GET and POST Methods: The GET method is used for displaying frontend pages, while the POST method is used for submitting form data. Several routes, including "/admin/search", "/admin/add_member", "/admin/<memberID>/edit", "/admin/add_event", "/admin/add_event_stage", and "/admin/add_result", utilize both GET and POST methods. In these cases, the "request.method == 'POST'" condition is used to detect a POST request and handle form data accordingly.

Discussion

1. Database Changes
To accommodate different types of Olympics (e.g., Winter Olympics and Summer Olympics), there are a few possible approaches:

Option 1: Add a new column in each table to indicate the Olympic type. For example, a column named "OlympicID" could be added to the "members" table, with values representing different Olympics (e.g., 1 for Summer Olympics, 2 for Winter Olympics). This approach requires modifying the existing table structure.

Option 2: Create separate tables for each type of Olympic event (e.g., "summer_members" and "winter_members"). This approach keeps the existing table structure intact but introduces new tables specific to each type of Olympic event.

The choice between these options depends on factors such as the complexity of the existing database structure and the specific requirements of the application.

2. Frontend Changes
To accommodate the Olympic type in the frontend, you can add a new column for "OlympicName" when displaying the member and event lists. Additionally, when accessing specific information or transferring data, ensure that the correct column is used. For example, when referencing the event ID, adjust the code from "{% Event[0] %}" to "{% Event[1] %}" to align with the new column structure.

3. Backend Changes
Backend changes will be required when interacting with the database. For example, when querying the database, adjust the SQL statement to include conditions related to the Olympic type. 
