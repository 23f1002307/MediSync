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
2.  Displaying all the doctors in a tabular format on the dashboard
3. Added update and blacklist buttons next to each doctor to update their pre existing data or to remove them from the database
4. Added a "Add a doctor" button to register new doctors

B) For Patient related tasks:

1. Search any patient with their ID, contact number or name
2. All patients are visible on the dashboard by default
3. Each patient has a blacklist button as a control for the admin to remove the patient from the dashboard

c) For Appointments:

1. All appointments along with the doctor name and patient name and treatment details is displayed on the admin dashboard



\# Creating doctor dashboard functionalities:

a) See all appointments

1. See individual appointments with the control to mark any appointment as cancelled or completed
2. View full patient's medical history
3. See the treatment for that appointment
4. Edit treatment details like diagnosis, prescription and additional notes

b) Manage doctor's schedule:

1. Add a new time slot
2. Modify an existing time slot
3. View all the time slots in a tabular format



