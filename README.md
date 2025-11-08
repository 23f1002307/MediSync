# MediSync

A Flask-based Hospital Management System web app with role-based access for Admin, Doctors, and Patients — featuring appointment booking, doctor scheduling, patient records, and secure data management using Jinja2 templating and SQLite ORm.



\# Created a common login form for the 3 users namely: admin ( super user ), doctor and patient:

Admin - No registeration required

Doctor - Could be Registered by the admin only.

Patient - Register from the Home page of the app.

If the email ID is found to be present in the database then, the user is prompted that you have been already registered with us and is redirected to the login page.



Login Page contains:

Email ID which acts as the unique User ID

Password to login onto the Patient / Doctor dashboard



\# 3 dashboards for the 3 users is created and endpoints are added in the app.py file



\# Adding Admin Dashboard Functionalities:

A) For Doctor related tasks:

1. Created a search box to filter doctors by their specialization or name
2. &nbsp;Displaying all the doctors in a tabular format on the dashboard
3. Added update and blacklist buttons next to each doctor to update their pre existing data or to remove them from the database
4. Added a "Add a doctor" button to register new doctors

B) For Patient related tasks:





