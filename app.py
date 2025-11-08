import os
from flask import Flask, render_template, redirect, request, url_for
from models import db, Patient, Doctor, Appointment, Treatment, Availability
from dotenv import load_dotenv

app = Flask ( __name__ )
app.config [ "SQLALCHEMY_DATABASE_URI" ] = 'sqlite:///MediSync.db'

# Loading secrets from .env:
load_dotenv ( )
# Stores Admin credentials:
admin_email = os.getenv ( "ADMIN_EMAIL_ID" )
admin_password = os.getenv ( "ADMIN_PASS" )

# Binding the database to the app:
db.init_app ( app )

# Creating the tables within the database:
with app.app_context ( ):
	db.create_all ( )

@app.route ( "/", methods = [ "GET", "POST" ] )
def index ( ):
	return render_template ( "index.html" )

@app.route ( "/register/patient", methods = [ "GET", "POST" ] )
def patient_registeration ( ): # Patient Registeration form
	message = ""
	if request.method == "POST":
		name = request.form.get ( "name" )
		phone_number = request.form.get ( "phone" )
		email_id = request.form.get ( "email" )
		password = request.form.get ( "password" )
		age = request.form.get ( "age" )
		gender = request.form.get ( "gender" )
		address = request.form.get ( "address" )
		blood_group = request.form.get ( "blood_group" )
		medical_history = request.form.get ( "medical_history" )
		existing_patient = Patient.query.filter_by ( email = email_id ).first ( )
		if not existing_patient:
			new_patient = Patient ( name = name, email = email_id, password = password, phone = phone_number, age = age, gender = gender, address = address, blood_group = blood_group, medical_history = medical_history )
			db.session.add ( new_patient )
			db.session.commit ( )
			return redirect ( url_for ( "login", message = "Registeration successful. Please login with your new credentials." ))
		else:
			return redirect ( url_for ( "login", message = "This email ID is already registered. Please login or visit the registeration page and register with a different email ID." ))
	return render_template ( "patient_registeration.html" )

@app.route ( "/doctor_registeration", methods = [ "GET", "POST" ] )
def doctor_registeration ( ): # Doctor Registeration form. Successful registeration of a new doctor redirects to the admin dashboard and for an existing login ID, the user is redirected to the login form.
	if request.method == "POST":
		name = request.form.get ( "name" )
		phone = request.form.get ( "phone" )
		email_id = request.form.get ( "email" )
		password = request.form.get ( "password" )
		specialization = request.form.get ( "specialization" )
		qualification = request.form.get ( "qualification" )
		experience_years = request.form.get ( "experience_years" )
		existing_doctor = Doctor.query.filter_by ( email = email_id ).first ( )
		if not existing_doctor:
			new_doctor = Doctor ( name = name, phone = phone, email = email_id, password = password, specialization = specialization, qualification = qualification, experience_years = experience_years )
			db.session.add ( new_doctor )
			db.session.commit ( )
			return redirect ( url_for ( 'admin_dashboard' ))
		else:
			return redirect ( url_for ( 'login', message = "This email ID is already registered. Provide a new one or login into the existing one." ))
	return render_template ( "doctor_registeration.html" )

@app.route ( "/login", methods = [ "GET", "POST" ] )
def login ( ): # Common login form for all the 3 users
	message = request.args.get ( "message", "" )
	if request.method == "POST":
		role = request.form.get ( 'role' )
		email = request.form.get ( 'email' )
		password = request.form.get ( 'password' )
		if role == "doctor":
			doctor = Doctor.query.filter_by ( email = email ).first ( )
			if doctor:
				if doctor.password == password:
					return redirect ( url_for ( "doctor_dashboard", doctor_id = doctor.id ))
				else:
					return redirect ( url_for ( "error" ))
			else:
				return redirect ( url_for ( "error" ))
		elif role == "patient":
			patient = Patient.query.filter_by ( email = email ).first ( )
			if patient:
				if patient.password == password:
					return redirect ( url_for ( "patient_dashboard", patient_id = patient.id ))
				else:
					return redirect ( url_for ( "error" ))
			else:
				return redirect ( url_for ( "error" ))
		elif role == "admin":
			if email == admin_email and password == admin_password:
				return redirect ( url_for ( 'admin_dashboard' ))
			else:
				return redirect ( url_for ( 'error' ))
	return render_template ( "login.html", message = message )

@app.route ( "/patient/dashboard/<int:patient_id>", methods = [ "GET", "POST" ] )
def patient_dashboard ( patient_id ): # After login, patient is redirected to this route
	patient = Patient.query.get ( patient_id )
	return render_template ( "patient_dashboard.html", patient = patient)

@app.route ( "/doctor/dashboard/<int:doctor_id>", methods = [ "GET", "POST" ] )
def doctor_dashboard ( doctor_id ): # For doctors, this will redirect to their dashboard
	doctor = Doctor.query.get ( doctor_id )
	return render_template ( "doctor_dashboard.html", doctor = doctor )

@app.route ( "/admin/dashboard", methods = [ "GET", "POST" ] )
def admin_dashboard ( ): # Login page will redirect here if the correct admin credentials are entered
	# All Doctors, patients, and appointments need to be displayed on the admin dashboard:
	all_doctors = Doctor.query.all ( ) # It will return a list of Doctor objects	
	all_patients = Patient.query.all ( )
	all_appointments = Appointment.query.all ( )
	return render_template ( "admin_dashboard.html", all_doctors = all_doctors, all_patients = all_patients, all_appointments = all_appointments, searched_doctor = None, searched_patient = None )

# The following 3 methods are to deal with doctor related tasks on the admin dashboard: update_doctor, delete_doctor, search_doctor
@app.route ( "/update/doctor/<int:doctor_id>", methods = [ "GET", "POST" ] )
def update_doctor ( doctor_id ):
	doctor = Doctor.query.get ( doctor_id )
	if request.method == "POST":
		doctor.name = request.form.get ( "name" )
		doctor.phone = request.form.get ( "phone" )
		doctor.email = request.form.get ( "email" )
		doctor.password = request.form.get ( "password" )
		doctor.specialization = request.form.get ( "specialization" )
		doctor.qualification = request.form.get ( "qualification" )
		doctor.experience_years = request.form.get ( "experience_years" )
		db.session.commit ( )
		return redirect ( url_for ( 'admin_dashboard' ))
	return render_template ( 'update_doctor.html', doctor = doctor )

@app.route ( "/delete/doctor/<int:doctor_id>", methods = [ "GET", "POST" ] )
def delete_doctor ( doctor_id ):
	doctor = Doctor.query.get ( doctor_id )
	db.session.delete ( doctor )
	db.session.commit ( )
	return redirect ( url_for ( 'admin_dashboard' ))

@app.route ( "/search/doctor", methods = [ "GET", "POST" ] )
def search_doctor ( ):
	search_by = request.form.get ( "search_by" )
	search_value = request.form.get ( "search_value" )
	# If search is None then return all entries:
	if search_value == None or search_by == None:
		return redirect ( url_for ( "admin_dashboard" ))
	# If search is performed:
	if search_by == "doctor_name":
		filtered_doctors = Doctor.query.filter ( Doctor.name.ilike (f"%{search_value}%" )).all ( )
	elif search_by == "specialization":
		filtered_doctors = Doctor.query.filter ( Doctor.specialization.ilike ( f"%{search_value}%" )).all ( )
	else:
		filtered_doctors = [ ]
	all_patients = Patient.query.all ( )
	all_appointments = Appointment.query.all ( )
	return render_template ( "admin_dashboard.html", all_doctors = filtered_doctors, all_patients = all_patients, all_appointments = all_appointments, searched_doctor = search_value, searched_patient = None )

# The following 2 methods are to deal with patient related tasks on the admin dashboard: search patient and delete_patient
@app.route ( "/delete/patient/<int:patient_id>", methods = [ "GET", "POST" ] )
def delete_patient ( patient_id ):
	patient = Patient.query.get ( patient_id )
	db.session.delete ( patient )
	db.session.commit ( )
	return redirect ( url_for ( 'admin_dashboard' ))

@app.route ( "/search/patient", methods = [ "GET", "POST" ] )
def search_patient ( ):
	search_by = request.form.get ( "search_by" )
	search_value = request.form.get ( "search_value" )
	if search_value == None or search_by == None:
		return redirect ( url_for ( 'admin_dashboard' ))
	if search_by == "patient_name":
		filtered_patients = Patient.query.filter ( Patient.name.ilike ( f"%{search_value}%" ) ).all ( )
	elif search_by == "contact":
		filtered_patients = Patient.query.filter ( Patient.phone.ilike ( f"%{search_value}%" ) ).all ( )
	elif search_by == "id":
		filtered_patients = Patient.query.filter ( Patient.id.ilike ( f"%{search_value}%" ) ).all ( )
	else:
		filtered_patients = [ ]
	all_doctors = Doctor.query.all ( )
	all_appointments = Appointment.query.all ( )
	return render_template ( "admin_dashboard.html",
		all_doctors = all_doctors,
		all_patients = filtered_patients,
		all_appointments = all_appointments,
		searched_doctor = None,
		searched_patient = search_value
	)

@app.route ( "/error" )
def error ( ): # To handle any missed conditions
	return render_template ( "error.html" )

if __name__ == "__main__":
	app.run ( debug = True )