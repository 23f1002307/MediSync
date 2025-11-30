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

\# Creating patient dashboard:

a) For patient related info:

1. Update their profile
2. &nbsp;Edit / remove any existing data
3. Change email id and password

b)For doctor related tasks:

1. Adding a table to view all doctors with their available time slots
2. &nbsp;Book any doctor from the table
3. Search any doctor by name or specialization

c) For upcoming appointments:

1. See all upcoming appointments with the doctor name, date, time, and status

d) Past appointments:

1. View all past appointments with treatment details





\# Appointment History \& conflict prevention:

1)Store and display complete appointment and treatment history ( in admin, doctor and patient dashboards )

2\) Prevent double booking of doctors at the same time slot.

3\) Maintain status updates (Booked / Completed / Cancelled).

4\) Admin and Doctor can view patient treatment records; Patients can view their own records.

5\) Patient cannot book a time slot when the doctor is not available.



\# Conclusion:

This app has been made keeping the UI simple and easy to navigate.

It is user friendly and completely accessible for people with vision impairment.



