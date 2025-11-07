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
def doctor_registeration ( ): # Doctor Registeration form
	message = ""
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
			return redirect ( url_for ( 'login', message = "Registeration successful. Please login with your new Email ID and password." ))
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
	return render_template ( "admin_dashboard.html" )

@app.route ( "/error" )
def error ( ): # To handle any missed conditions
	return render_template ( "error.html" )

if __name__ == "__main__":
	app.run ( debug = True )