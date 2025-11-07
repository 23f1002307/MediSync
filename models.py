from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy ( )

class Patient ( db.Model ):
	id = db.Column ( db.Integer, primary_key = True )
	name = db.Column ( db.String ( 50 ), nullable = False )
	email = db.Column ( db.String ( 100), unique = True, nullable = False )
	password = db.Column ( db.String ( 100), nullable = False )
	phone = db.Column ( db.String ( 15 ), nullable = False )
	gender = db.Column ( db.String ( 1 ), nullable = False )
	age = db.Column ( db.Integer )
	blood_group = db.Column ( db.String ( 3 ))
	address = db.Column ( db.String ( 500))
	medical_history = db.Column ( db.String ( 1000 ) )

class Doctor ( db.Model ):
	id = db.Column ( db.Integer, primary_key = True )
	name = db.Column ( db.String ( 50 ), nullable = False )
	email = db.Column ( db.String ( 100), unique = True, nullable = False )
	password = db.Column ( db.String ( 100), nullable = False )
	phone = db.Column ( db.String ( 15 ), nullable = False )
	specialization = db.Column ( db.String ( 60), nullable = False )
	qualification = db.Column ( db.String ( 50), nullable = False )
	experience_years = db.Column ( db.Integer, nullable = False )

class Availability ( db.Model ):
	id = db.Column ( db.Integer, primary_key = True )
	doctor_id = db.Column ( db.Integer, db.ForeignKey ( 'doctor.id' ), nullable = False )
	day = db.Column ( db.String ( 20), nullable = False )
	start_time = db.Column ( db.Time )
	end_time = db.Column ( db.Time )
	doctor = db.relationship ( 'Doctor', backref = db.backref ( 'availabilities' ))

class Appointment ( db.Model ):
	id = db.Column ( db.Integer, primary_key = True )
	doctor_id = db.Column ( db.Integer, db.ForeignKey ( 'doctor.id' ), nullable = False )
	patient_id = db.Column ( db.Integer, db.ForeignKey ( 'patient.id' ), nullable = False )
	status = db.Column ( db.String ( 20 ), nullable = False )
	date = db.Column ( db.Date )
	time = db.Column ( db.Time )
	# Relations:
	doctor = db.relationship ( 'Doctor', backref = db.backref ( 'appointments' ))
	patient = db.relationship ( 'Patient', backref = db.backref ( 'appointments' ))
	treatment = db.relationship ( 'Treatment', backref = 'appointment', uselist = False )

class Treatment ( db.Model ):
	id = db.Column ( db.Integer, primary_key = True )
	appointment_id = db.Column ( db.Integer, db.ForeignKey ( 'appointment.id' ), unique = True, nullable = False )
	diagnosis = db.Column ( db.String ( 500 ) )
	prescription = db.Column ( db.String ( 500 ) )
	notes = db.Column ( db.String ( 500 ) )
