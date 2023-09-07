import flask
import MySQLdb.cursors
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, validators
from wtforms.validators import DataRequired
from datetime import timedelta
import time
# for mail sending
from flask_mail import *  
from random import *  
import nexmo




app = Flask(__name__)
# app.secret_key= '123456'
from configure import config
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config["MAIL_SERVER"]='smtp.googlemail.com'  
app.config["MAIL_PORT"] = 465     
app.config["MAIL_USERNAME"] = 'rahulkumar34251@gmail.com'  
app.config['MAIL_PASSWORD'] = 'dzgvrbspupkorwwi'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True 
mail = Mail(app)   
mysql = config(app)

client = nexmo.Client(key='7b3ed80c', secret='T2aELCzxStq59X5F')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')


# @app.route('/admin')
# def admin():
#     email = session.get('email')
#     phone = str(session.get('phone'))
#     if(email=="admin@host.local" and phone== "1234567899"):
#         return render_template('admin.html')
#     return render_template('pagenotfound.html')



# Authentication
@app.route("/login", methods=["POST", "GET"])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form.get('email')
        phone = str(request.form.get('mobile'))

        if email != 'admin@host.local' or phone != "1234567899":
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            flag = False
            otp = randint(000000,999999)
            otp_valid_till = time.time() + 900  #added 15 min
            if email != '' and phone == '':
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                account1 = cursor.fetchone()
                if(account1):
                    print("enter in email if")
                    session['email'] = email
                    session['phone'] = phone
                    # msgmail = Message('One Time OTP Verification',sender = 'rahulkumar34251@gmail.com', recipients = [email])  
                    # msgmail.body = f'Hello users, Welcome to organization name. Your otp is : {otp}'  
                    # mail.send(msgmail) 
                    cursor.execute(f"UPDATE users SET otp = {otp},otp_valid_till = {otp_valid_till}  WHERE email = %s", ((email,)))
                    mysql.connection.commit()
                    cursor.close()
                    msg = "OTP Send Successfully."
                    flask.flash(msg)
                    return redirect(url_for('verifyOtp'))
            elif phone != '' and email == '':
                cursor.execute("SELECT * FROM users WHERE phone_no = %s", (phone,))
                account1 = cursor.fetchone()
                if(account1):
                    print("enter in phone if")
                    # client.send_message({'from': 'Rahul Kumar', 'to': '9727270199', 'text': f'Your otp is: {otp}'})
                    session['email'] = email
                    session['phone'] = phone
                    cursor.execute(f"UPDATE users SET otp = {otp}, otp_valid_till = {otp_valid_till} WHERE phone_no = %s", ((phone,)))
                    mysql.connection.commit()
                    cursor.close()
                    msg = "OTP sent successfully"
                    flask.flash(msg)
                    return redirect(url_for('verifyOtp'))
            elif phone != ''  and email != "":
                cursor.execute("SELECT * FROM users WHERE email = %s and phone_no = %s", (email,phone))
                account1 = cursor.fetchone()
                if(account1):
                    print("enter in phone email if")
                    session['email'] = email
                    session['phone'] = phone
                    # msgmail = Message('One Time OTP Verification',sender = 'rahulkumar34251@gmail.com', recipients = [email])  
                    # msgmail.body = f'Hello users, Welcome to organization name. Your otp is : {otp}'  
                    # mail.send(msgmail) 
                    cursor.execute(f"UPDATE users SET otp = {otp},otp_valid_till = {otp_valid_till}  WHERE email = %s and phone_no = %s", ((email,phone)))
                    mysql.connection.commit()
                    cursor.close()
                    msg = "OTP Send Successfully."
                    flask.flash(msg)
                    return redirect(url_for('verifyOtp'))
            else:
                print("enter in else phon")
                msg = "You have not registered. Please Registered first"
                flask.flash(msg)
                return render_template('login.html')
            
        elif email == "admin@host.local" and phone == "1234567899":
            session['email'] = email
            session['phone'] = phone
            msg = "Login Successfully"
            flask.flash(msg)
            # session.permanent = True
            return redirect(url_for('admin'))
        else:
            session.pop('email', None)
            session.pop('phone', None)
            msg = "You have not registered yet. Please register first"
            flask.flash(msg)
            return render_template("invalid.html")
    
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        # Get the values from the form
        company_name = request.args.get('company')
        emp_no = request.args.get('empNo')
        
        if(company_name == 'Others'):
            company_name = request.args.get('otherCompany')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE company_name = %s and emp_no = %s", (company_name, emp_no))
        user = cursor.fetchone()
        cursor.close()
        if(user):
            user_detail = {
                'name': user['user_name'],
                'designation':user['designation'],
                'email': user['email'],
                'mobile': user['phone_no']
            }
            return render_template('register.html', user_detail=user_detail)
        else:
            user_detail = {
                'name': '',
                'designation':'',
                'email': '',
                'mobile': ''
            }
            return render_template('register.html', user_detail=user_detail)
        

    return render_template('register.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verifyOtp():
    if request.method == 'POST':
        otp = request.form.get('otp')
        email = session.get('email')
        phone = str(session.get('phone'))
        session['otpVerified'] = False
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        currentTime = time.time()
        print(otp)
        print(email)
        print(phone)
        
        if(email != ''):
            cursor.execute("SELECT otp, otp_valid_till FROM users WHERE email = %s", (email,))
            detail = cursor.fetchone()
            print(detail['otp_valid_till'])
            print(currentTime)
            if(otp == detail['otp']):
                print('ture')
            if(otp == detail['otp'] and currentTime < detail['otp_valid_till']):
                print("enter in chekup")
                cursor.execute("UPDATE users set is_otp_verified = %s WHERE email = %s", (True, email,))
                mysql.connection.commit()
                cursor.close()
                session['otpVerified'] = True
                print("coming")
                return redirect(url_for('user'))
            else:
                print("enter in else")
                session['otpVerified'] = False
                msg = "Your otp is not correct. Plese enter a valid otp."
                flask.flash(msg)
                return render_template('verifyOtp.html')
        else:
            cursor.execute("SELECT otp, otp_valid_till FROM users WHERE phone_no = %s", (phone,))
            detail = cursor.fetchone()
            if(otp == detail.otp and currentTime < detail.otp_valid_till):
                cursor.execute("UPDATE users set is_otp_verified = %s WHERE phone_no = %s", (True, phone,))
                mysql.connection.commit()
                cursor.close()
                session['otpVerified'] = True
                return redirect(url_for('user'))
            else:
                session['otpVerified'] = False
                msg = "Your otp is not correct. Plese enter a valid otp."
                flask.flash(msg)
                return render_template('verifyOtp.html')
    print("hey");

    return render_template('verifyOtp.html')

# users
@app.route('/user')
def user():
    # email = session.get('email')
    # phone = str(session.get('phone'))
    # otpVerified = session.get('otpVerified')
    # if(phone == ''):
    #     if(email and otpVerified):
    #        return render_template('user.html')
    #     else:
    #         return render_template('invalid.html')
    # else:
    #     if(phone and otpVerified):
    #        return render_template('user.html')
    #     else:
    #         return render_template('invalid.html')
    return render_template('user.html')

# @app.route('/*')
# def notfound():
#     return render_template('pagenotfound.html')

@app.route('/userquiz')
def userQuiz():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM question WHERE quiz_type_id  = %s", (1,))
    question = cursor.fetchall()
    print(question[0])
    print(len(question))
    totalQuestion = len(question)
    return render_template('userquiz.html', questions=question, totalQuestion =totalQuestion)

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Admin
@app.route('/admin')
def admin():
    return render_template('admin.html')


# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route("/submit_option", methods=["POST"])
def submit_option():
    question_index = int(request.form.get("question_index"))
    selected_option = request.form.get("selected_option")
    
    # Store the selected option in the database or perform any other necessary actions
    
    # Return a response indicating success or failure
    return "Option submitted successfully"


if __name__ == '__main__':
    app.run(debug=True)