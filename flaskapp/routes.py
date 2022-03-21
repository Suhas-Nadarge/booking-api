from flaskapp import db,app,bcrypt
from flask import request
from flask_jsonpify import jsonify
from flaskapp.models import User,Booking
from flask_login import login_user , current_user , logout_user , login_required
from datetime import datetime

from flaskapp.send_email import send_email


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
            return jsonify({'status': 'fail', 'message': 'User already registered.'}),500
        

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
        return jsonify({'status':'success','id':user.id,'isDoctor':user.isDoctor,'firstname':user.firstname, 'lastname':user.lastname}), 200
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
    # appointment_date = data['appointment_date']
    appointment_date = datetime.strptime(data['appointment_date'] , '%Y-%m-%dT%H:%M:%S.%fZ')
    # appointment_date = datetime.strftime(data['appointment_date'],'%Y-%m-%dT%H:%M:%SZ')
    print(appointment_date)
    additional_comments = data['additional_comments']
    slot_number = data['slot_number']
    patient_id = data['patient_id']
    doctors_id = data['doctors_id']   
    slot = data['slot']

    appointment = Booking(reason=reason,appointment_date=appointment_date,additional_comments=additional_comments,
                slot_number=slot_number,slot = slot, patient_id=patient_id,doctors_id=doctors_id)
    userObj = User.query.filter_by(id=patient_id).first()
    print(userObj, patient_id)
    doctor = get_user_details_from_id(doctors_id)
    db.session.add(appointment)
    send_email(userObj.email,'isBooked',doctor, userObj.firstname,appointment_date,slot)
    db.session.commit()
    
    return jsonify({'massage':'booking done'}) ,200

# @app.route("/getDocsAppointments/<int:doctor_id>",methods=['GET'])
@app.route("/getDocsAppointments",methods=['POST'])

def get_day_appointments():
    # doctor_name
    data = request.get_json()
    if data['isPatient']:
        appointments = Booking.query.filter_by(patient_id=data['id']).all()
        # doctor_name = 
    else:
        appointments = Booking.query.filter_by(doctors_id=data['id']).all()
        # doctor_name = get_user_details_from_id(data['id']) a if a < b else b
    doc_name = get_user_details_from_id(appointments[0].doctors_id) if data['isPatient'] and appointments else ''
    appointments_list = [ 
        {'appointment_date': appointment.appointment_date,'reason':appointment.reason,
        'slot_number': appointment.slot_number, 'doctor_name': doc_name ,'slot': appointment.slot,'id': appointment.id,'patient_id':appointment.patient_id, 'patient_name': get_user_details_from_id(appointment.patient_id),'isCancelled': appointment.isCancelled, } 
        for appointment in appointments
    ]

    return jsonify(appointments=appointments_list) ,200

@app.route("/cancel",methods=['POST'])
def cancel_appointment():


    data = request.get_json()

    patient_id = data['patient_id']
    doctors_id = data['doctors_id']
    app_id = data['app_id']
    userObj = User.query.filter_by(id=patient_id).first()
    appointment = Booking.query.filter_by(id=app_id).first()
    appointment.isCancelled = True
    db.session.add(appointment)
    db.session.commit()
    doctor = get_user_details_from_id(doctors_id)

    send_email(userObj.email, 'isCancelled',doctor, userObj.firstname, appointment.appointment_date, appointment.slot )
    return jsonify({'message': 'appoitment canceled'}) ,200


def get_user_details_from_id(user_id):

    user = User.query.filter_by(id=user_id).first()

    return f"{user.firstname} {user.lastname}"


    


# from flaskapp import db
# >>> db.close_all()
# >>> db.create_all()