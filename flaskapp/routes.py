from flaskapp import db,app
from flask import request
from flask_jsonpify import jsonify
from flaskapp.models import User,Booking
from flask_login import login_user , current_user , logout_user , login_required


@app.route("/")
def index():

    return jsonify({'welcome':'Home Page'}) 


@app.route("/register",methods=['POST'])
def register():


    data = request.get_json()

    
    if request.method == 'POST':

        if current_user.is_authenticated:
            return jsonify({'status':'fail','massage':'user is already logged in'})


        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        isDoctor = data['isDoctor']
        password = data['password']
        
        
        user = User.query.filter_by(email=email).first()

        if user:
            return jsonify({'status': 'fail', 'message': 'User already registered.'})
        

        hashed_passwd = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(firstname=firstname,lastname=lastname,isDoctor=isDoctor,email=email,password=hashed_passwd)
        db.session.add(user)
        db.session.commit()

        massage = f"User {firstname} successfully added "

        return jsonify({'status': 'success', 'message': massage}) , 200

    return jsonify({'data':'something went wrong'}) , 500


@app.route("/login",methods=['POST'])
def login():
    

    data = request.get_json()

    if current_user.is_authenticated:
            return jsonify({'status':'fail','massage':'user is already logged in'})
    
    email = data['email']
    password = data['password']
    

    user = User.query.filter_by(email=email).first()
    
    if user and bcrypt.check_password_hash(user.password,password):
        login_user(user)
        return jsonify({'status':'success','user':user}), 200
    else:
        return jsonify({'status':'fail','massage':'something went wrong'}) , 401

    return jsonify({'massage':'something went wrong'})

@app.route("/logout",methods=['POST'])
@login_required
def logout():
    logout_user()
    return  jsonify({'status':'success','massage':'logged out'}), 200




@app.route("/getAllDoctors",methods=['GET'])
def get_all_doctors():

    doctors = User.query.filter_by(isDoctor=True).all()

    doc_list = [ 
        {'full_name': f'{doc.firstname} {doc.lastname}',
         'isDoctor' : doc.isDoctor,
         'id': doc.id
        } for doc in doctors
    ]

    return jsonify(doctors=doc_list) ,200




@app.route("/bookAppointment",methods=['POST'])
def book_appointments():

    data = request.get_json()

    reason = data['reason']
    appointment_date = data['appointment_date']
    additional_comments = data['additional_comments']
    slot_number = data['slot_number']
    patient_id = data['patient_id']
    doctors_id = data['doctors_id']    

    appointment = Booking(reason=reason,appointment_date=appointment_date,additional_comments=additional_comments,
                slot_number=slot_number,patient_id=patient_id,doctors_id=doctors_id)

    db.session.add(appointment)
    db.session.commit(appointment)
    
    return jsonify({'massage':'booking done'}) ,200

@app.route("/getDayAppointments/<int:doctor_id>",methods=['GET'])
def get_day_appointments(doctor_id):

    appointments = Booking.query.filter_by(doctors_id=doctor_id).all()


    appointments_list = [ 
        {'appointment_date': appointment.appointment_date,
        'slot_number': appointment.slot_number, 'patient_name': get_patient_details_from_id(patient_id) } 
        for appointment in appointments
    ]

    return jsonify(appointments=appointments_list) ,200

@app.route("/cancel",methods=['POST'])
def cancel_appointment(doctor_id):


    data = request.get_json()

    patient_id = data['patient_id']
    doctors_id = data['doctors_id']

    appointment = Booking.query.filter_by(id=patient_id).filter_by(doctors_id=doctors_id).first()

    appointment.isCancelled = True

    db.session.commit(appointment)

    return jsonify({'message': 'appoitment canceled'}) ,200


def get_patient_details_from_id(patient_id):

    patient = User.query.filter_by(id=patient_id).first()

    return f"{patient.firstname} {patient.lastname}"


    

