
from flask import Flask,flash,redirect,render_template,url_for,request,jsonify,session,abort
from flask_session import Session
from flask_mysqldb import MySQL
from datetime import date
from datetime import datetime
import mysql.connector 
from mysql.connector import OperationalError
from sdmail import sendmail
from tokenreset import token
from stoken1 import token1
from otp import genotp
import os
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from key import *
app=Flask(__name__)
app.secret_key='hellohelo'
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['MYSQL_HOST'] ='localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD']='8341434767@@@@@'
# app.config['MYSQL_DB']='freelancer_marketplace'
mydb=mysql.connector.connect(host='localhost',user='root',password='8341434767@@@@@',db='freelancer_marketplace')
# mydb=MySQL(app)
Session(app)

@app.route('/')
def index():
    return render_template('index.html')
#=========================================Freelancer login and register
@app.route('/ulogin',methods=['GET','POST'])
def ulogin():
    if session.get('user'):
        return redirect(url_for('users_dashboard'))
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('SELECT count(*) from users where email=%s',[email])
        count=cursor.fetchone()[0]

        if count==1:
            cursor.execute('select password from users where email=%s',[email])
            confirm_password=cursor.fetchone()[0]
            cursor.execute('select username from users where email=%s',[email])
            user=cursor.fetchone()[0]
            if confirm_password==password:
                session['user']=user
                if not session.get(user):
                    session[user]={}
                return redirect(url_for("users_dashboard"))
            else:
                flash('Invalid password')
                return redirect(url_for('ulogin'))
        else :
            flash('ACCOUNT NOT REGISTERED')
            return redirect(url_for('uregistration'))
    return render_template('flogin.html')

@app.route('/uregistration',methods=['GET','POST'])
def uregistration():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        phone_number = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']       
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from users where username=%s',[username])
        count=cursor.fetchone()[0]
        cursor.execute('select count(*) from users where email=%s',[email])
        count1=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            flash('USERNAME ALREADY EXISTED')
            return redirect(url_for('uregistration'))
        elif count1==1:
            flash('EMAIL ALREADY EXISTED')
            return redirect(url_for('uregistration'))
        else :
             if password==confirm_password:
                    otp = genotp()
                    var1={'username':username,'first_name':first_name,'last_name':last_name,'email':email,'phone_number':phone_number,'password':password,'fotp':otp}
                    subject = 'Registration OTP for Freelancer Account in TALENT-HUB'
                    body=f"Thanks for signing up\n\nfollow this link for further steps-{otp}"
                    sendmail(to=email, subject=subject, body=body)
                    flash('OTP sent successfully')
                    return redirect(url_for('fotpform',fotp=token(data=var1, salt=salt)))
             else:
                    flash('Password not matched')
                    return redirect(url_for('uregistration'))
    return render_template('fregister.html')
@app.route('/fotpform/<fotp>',methods=['GET','POST'])
def fotpform(fotp):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        var1=serializer.loads(fotp,salt=salt)
    except Exception as e:
        flash('OTP expired')
        return render_template('otp.html')
    else:
        if request.method=='POST':
            otp=request.form['otp']
            if var1['fotp'] == otp :
                cursor=mydb.cursor(buffered=True)
                cursor.execute('insert into users(username,first_name,last_name,email,phone_number,password) values(%s,%s,%s,%s,%s,%s)',[var1['username'],var1['first_name'],var1['last_name'],var1['email'],var1['phone_number'],var1['password']])
                mydb.commit()
                cursor.close()
                flash('Registration Successfull')
                return redirect(url_for('ulogin'))
            else:
                flash('Invalid OTP')
                return render_template('otp.html')
        return render_template('otp.html')
@app.route('/forgotf',methods=['GET','POST'])
def forgotf():
    if request.method=='POST':
        email=request.form['email']
        subject='RESET Link for password for Freelancer account in TALENT-HUB'
        body=f"Click the link to verify the reset password:{url_for('verifyforgetf',data=token(data=email,salt=salt2),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('Reset Link has been sent to your mail')
        return redirect(url_for('forgotf'))
    return render_template('forgot.html')
@app.route('/verifyforgetf/<data>',methods=['GET','POST'])
def verifyforgetf(data):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(data,salt=salt2,max_age=180)
    except Exception :
        flash('Link Expired')
        return redirect(url_for('forgotf'))
    else :
        if request.method=='POST':
            npassword=request.form['npassword']
            cpassword=request.form['cpassword']
            if npassword==cpassword:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update users set password=%s where email=%s',[npassword,data])
                mydb.commit()
                flash("PASSWORD RESET SUCCESSFULLY")
                return redirect(url_for('ulogin'))
            else:
                flash('PASSWORD NOT MATCHED')
                return redirect(url_for('verifyforgetf'))
    return render_template('newpassword.html')
@app.route('/ulogout')
def ulogout():
    if session.get('user'):
        session.pop('user')
        flash('Successfully logged out')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('ulogin'))
@app.route('/users_dashboard')
def users_dashboard():
    if session.get('user'):
        return render_template('users_dashboard.html')
    return redirect(url_for('ulogin'))
#============================== Business registration
@app.route('/blogin',methods=['GET','POST'])
def blogin():
     if session.get('company'):
        return redirect(url_for('company_dashboard'))
     if request.method=='POST':
           username=request.form['gst_number']
           password=request.form['password']
           cursor=mydb.cursor(buffered=True)
           cursor.execute('SELECT count(*) from companies where gst_number=%s',[username])
           count=cursor.fetchone()[0]
           if count==1:
                cursor.execute('select password from companies where gst_number=%s',[username])
                cpassword=cursor.fetchone()[0]
                if cpassword==password:
                    session['company']=username
                    if not session.get(username):
                        session[username]={}
                    return redirect(url_for("company_dashboard"))
                else:
                    flash('Invalid password')
                    return redirect(url_for('blogin'))
           else :
                flash('ACCOUNT NOT REGISTERED')
                return redirect(url_for('bregistration'))
     return render_template('blogin.html')
@app.route('/bregistration',methods=['GET','POST'])
def bregistration():
    if request.method=='POST':
        gst=request.form['gst_number']
        company=request.form['company_name']
        email=request.form['email']
        phone=request.form['phone_number']
        location=request.form['location']
        industry=request.form['industry']
        linkedin_profile = request.form['linkedin_profile']
        password=request.form['password']
        cpassword=request.form['cpassword']

        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from companies where gst_number=%s',[gst])
        count=cursor.fetchone()[0]
        cursor.execute('select count(*) from companies where email=%s',[email])
        count1=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            flash('USERNAME ALREADY EXISTED')
            return redirect(url_for('bregistration'))
        elif count1==1:
            flash('EMAIL ALREADY EXISTED')
            return redirect(url_for('bregistration'))
        else:
            if password==cpassword:
                    otp = genotp()
                    var2={'gst':gst,'company':company,'email':email,'phone':phone,'location':location,'industry':industry,'linkedin_profile':linkedin_profile,'password':password,'botp':otp}
                    subject = 'Registration OTP for Business Account in TALENT-HUB'
                    body=f"Thanks for signing up\n\nfollow this link for further steps-{otp}"
                    sendmail(to=email, subject=subject, body=body)
                    flash('OTP sent successfully')
                    return redirect(url_for('botpform',botp=token1(data1=var2, salt=salt)))
            else:
                    flash('Password not matched')
                    return redirect(url_for('bregistration'))
    return render_template('bregister.html')
@app.route('/botpform/<botp>',methods=['GET','POST'])
def botpform(botp):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        var2=serializer.loads(botp,salt=salt)
    except Exception as e:
        flash('OTP expired')
        return render_template('otp.html')
    else:
        if request.method=='POST':
            otp=request.form['otp']
            if var2['botp'] == otp :
                cursor=mydb.cursor(buffered=True)
                cursor.execute('INSERT INTO companies(gst_number, company_name, email, phone_number, location, industry, linkedin_profile, password) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', [var2['gst'], var2['company'], var2['email'], var2['phone'], var2['location'], var2['industry'], var2['linkedin_profile'], var2['password']])
                mydb.commit()
                cursor.close()
                flash('Registration Successfull')
                return redirect(url_for('blogin'))
            else:
                flash('Invalid OTP')
                return render_template('otp.html')
        return render_template('otp.html')
@app.route('/forgotb',methods=['GET','POST'])
def forgotb():
    if request.method=='POST':
        email=request.form['email']
        subject='RESET Link for password for Business account in TALENT-HUB'
        body=f"Click the link to verify the reset password:{url_for('verifyforgetb',data1=token1(data1=email,salt=salt2),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('Reset Link has been sent to your mail')
        return redirect(url_for('forgotb'))
    return render_template('forgot.html')
@app.route('/verifyforgetb/<data1>',methods=['GET','POST'])
def verifyforgetb(data1):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data1=serializer.loads(data1,salt=salt2,max_age=600)
    except Exception :
        flash('Link Expired')
        return redirect(url_for('forgotb'))
    else :
        if request.method=='POST':
            npassword=request.form['npassword']
            cpassword=request.form['cpassword']
            if npassword==cpassword:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update companies set password=%s where email=%s',[npassword,data1])
                mydb.commit()
                flash("PASSWORD RESET SUCCESSFULLY")
                return redirect(url_for('blogin'))
            else:
                flash('PASSWORD NOT MATCHED')
                return redirect(url_for('verifyforgetb'))
    return render_template('newpassword.html')
@app.route('/blogout')
def blogout():
    if session.get('company'):
        session.pop('company')
        flash('Successfully logged out')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('blogin'))
#===================creating freelancer account

@app.route('/freelancer_management',methods=['GET','POST'])
def freelancer_management():
    if session.get('user'):
        print("==================================",session.get('user'))
        if request.method=="POST":
            id1_pic=genotp()
            name=request.form['name']
            email=request.form['email']
            pimage=request.files['profile_image']
            availability=request.form['availability']
            location=request.form['location']
            experience=request.form['experience']
            institution_name=request.form['institution_name']
            year=request.form['year']
            amount=request.form['amount']
            working=request.form['working_hours']
            filename=id1_pic+'.jpg'
            # datetime object containing current date and time
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from freelancer where name=%s',[name])
            count=cursor.fetchone()[0]
            if count==1:
                flash('A freelancer with the same name already exists.')
                return render_template('freelancer_management.html')
            now = datetime.now()
            cursor=mydb.cursor(buffered=True)
            cursor.execute('INSERT INTO  freelancer (name, email,account_creation_date,profile_image,availability,location, experience, institution_name, year,username,amount,working_hours) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)',[name,email,now,id1_pic,availability,location,experience,institution_name,year,session['user'],amount,working])

            #path = r"C:\Users\U$ER\Downloads\freelancer_marketplace\static"
            path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
            if not os.path.exists(path):
                os.makedirs(path,exist_ok=True)
            pimage.save(os.path.join(path, filename))
            mydb.commit()
            flash('details added sucessfully')
            return render_template('freelancer_management.html')
        return render_template('freelancer_management.html')
    return redirect(url_for('ulogin'))
@app.route('/addproject',methods=['GET','POST'])
def addproject():
    if session.get('user'):
        if request.method=="POST":
            id1_pic=genotp()
            project_name=request.form['project_name']
            description=request.form['description']
            project_image_file=request.files['project_image_file']
            completion_date=request.form['completion_date']
            filename=id1_pic+'.jpg'
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select freelancer_id from freelancer where username=%s',[session['user']])
            fid=cursor.fetchone()[0]
            cursor.execute('insert into projects (freelancer_id,project_name,description,project_image,completion_date) values (%s,%s,%s,%s,%s)',[fid,project_name,description,id1_pic,completion_date])
            #path = r"C:\Users\U$ER\Downloads\freelancer_marketplace\static"
            path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
            if not os.path.exists(path):
                os.makedirs(path,exist_ok=True)
            project_image_file.save(os.path.join(path, filename))
            mydb.commit()
            flash('projects details added')
            return render_template('users_dashboard.html')
        return render_template('addproject.html')
    return redirect(url_for('ulogin'))
#======================UPDATE PROJECT DETAILS
@app.route('/updateproject',methods=['GET','POST'])
def updateproject():
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select freelancer_id from freelancer where username=%s',[session['user']])
        fid=cursor.fetchone()[0]
        cursor.execute('select * from projects where freelancer_id=%s',[fid])
        pdetails=cursor.fetchall()
        if request.method=="POST":
            #id1_pic=genotp()
            project_name=request.form['project_name']
            description=request.form['description']
            #project_image_file=request.files['project_image_file']
            completion_date=request.form['completion_date']
            #filename=id1_pic+'.jpg'
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select freelancer_id from freelancer where username=%s',[session['user']])
            fid=cursor.fetchone()
            cursor.execute('''UPDATE projects SET project_name= %s, description = %s, completion_date = %sWHERE freelancer_id = %s''', (project_name, description,completion_date, fid))
            # path = r"E:\freelancer_marketplace\static"
            # project_image_file.save(os.path.join(path, filename))
            mydb.commit()
            cursor.close()
            flash('Project details updated successfully')
            return render_template('users_dashboard.html')
        
        return render_template('updateprojects.html',pdetails=pdetails)
    return redirect(url_for('ulogin'))

@app.route('/addskills',methods=['GET','POST'])
def addskills():
    if session.get('user'):
        if request.method=="POST":
            skill_name=request.form['skill_name']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select freelancer_id from freelancer where username=%s',[session['user']])
            fid=cursor.fetchone()[0]
            cursor.execute('insert into skills (freelancer_id,skill_name) values (%s,%s)',[fid,skill_name])
            
            mydb.commit()
            flash('skills details added')
            return render_template('users_dashboard.html')
        return render_template('addskills.html')
    return redirect(url_for('ulogin'))
#===================update skills
@app.route('/updateskills',methods=['GET','POST'])
def updateskills():
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select freelancer_id from freelancer where username=%s',[session['user']])
        fid=cursor.fetchone()[0]
        cursor.execute('select * from skills where freelancer_id=%s',[fid])
        sdetails=cursor.fetchall()
        if request.method=="POST":
            skill_name=request.form['skill_name']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select freelancer_id from freelancer where username=%s',[session['user']])
            fid=cursor.fetchone()[0]
            cursor.execute('''UPDATE skills SET skill_name= %s WHERE freelancer_id = %s''', (skill_name, fid))

            mydb.commit()
            flash('skills updated scucessfully')
            return render_template('users_dashboard.html')
        
        return render_template('updateskills.html',i=sdetails)
    return redirect(url_for('ulogin'))
@app.route('/addcertification',methods=['GET','POST'])
def addcertification():
    if session.get('user'):
        if request.method=="POST":
            id1_pic=genotp()
            certification_name=request.form['certification_name']
            certification_image=request.files['certification_image']
            filename=id1_pic+'.jpg'
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select freelancer_id from freelancer where username=%s',[session['user']])
            fid=cursor.fetchone()[0]
            cursor.execute('insert into certifications (freelancer_id,certification_name,certificate_image) values (%s,%s,%s)',[fid,certification_name,id1_pic])
            #path = r"C:\Users\U$ER\Downloads\freelancer_marketplace\static"
            path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
            if not os.path.exists(path):
                os.makedirs(path,exist_ok=True)
            #project_image_file.save(os.path.join(path, filename))
            
            certification_image.save(os.path.join(path, filename))
            mydb.commit()
            flash('certification details added')
            return render_template('users_dashboard.html')
        return render_template('addcertification.html')
    return redirect(url_for('ulogin'))
#=================== update certification
@app.route('/updatecertification',methods=['GET','POST'])
def updatecertification():
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select freelancer_id from freelancer where username=%s',[session['user']])
        fid=cursor.fetchone()[0]
        cursor.execute('select * from certifications where freelancer_id=%s',[fid])
        cdetails=cursor.fetchall()
        if request.method=="POST":
            id1_pic=genotp()
            certification_name=request.form['certification_name']
           
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select freelancer_id from freelancer where username=%s',[session['user']])
            fid=cursor.fetchone()[0]
            cursor.execute('''UPDATE certifications SET certification_name= %s WHERE freelancer_id = %s''', (certification_name, fid))
            # path = r"E:\freelancer_marketplace\static"
            # certification_image.save(os.path.join(path, filename))
            mydb.commit()
            flash('certification details added')
            return render_template('users_dashboard.html')
        return render_template('updatecertification.html',cdetails=cdetails)
    return redirect(url_for('ulogin'))







@app.route('/personal_account')
def personal_account():
    if session.get('user'):
        return render_template('users_dashboard.html')
    return redirect(url_for('ulogin'))

#======================view personal details
@app.route('/viewpersonaldetails')
def view_personaldetails():
    if session.get('user'):
        cursor = mydb.cursor(buffered=True)

        # Fetch user details
        cursor.execute('SELECT * FROM freelancer WHERE username = %s', [session['user'],])
        user_data = cursor.fetchall()
        cursor.execute('select freelancer_id from freelancer where username=%s',[session['user']])
        fid=cursor.fetchone()[0]
        if fid:
        # Fetch projects of the user
            cursor.execute('SELECT * FROM projects WHERE freelancer_id = %s', [fid])
            projects = cursor.fetchall()
            # Fetch skills of the user
            cursor.execute('SELECT * FROM skills WHERE freelancer_id = %s', [fid])
            skills = cursor.fetchall()
            # Fetch certifications of the user
            cursor.execute('SELECT * FROM certifications WHERE freelancer_id = %s', [fid])
            certifications = cursor.fetchall()

            cursor.close()
            return render_template('viewpersonalaccount.html', user_data=user_data, projects=projects, skills=skills, certifications=certifications)
        else :
            flash('Please add the details first')
            return redirect(url_for('freelancer_management'))
    
    return redirect(url_for('ulogin'))
#=========================update freelancer management
@app.route('/updatefreelancer_management',methods=['GET','POST'])
def updatefreelancer_management():
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from freelancer where username=%s',[session['user']])
        fdetails=cursor.fetchall()
        if request.method=="POST":
            id1_pic=genotp()
            name=request.form['name']
            email=request.form['email']
            pimage=request.files['profile_image']
            availability=request.form['availability']
            location=request.form['location']
            experience=request.form['experience']
            institution_name=request.form['institution_name']
            year=request.form['year']
            amount=request.form['amount']
            working=request.form['working_hours']
            # datetime object containing current date and time
            filename=id1_pic+'.jpg'
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select freelancer_id from freelancer where username=%s',[session['user']])
            fid=cursor.fetchone()[0]
            cursor.execute('''UPDATE freelancer SET name = %s, email = %s,profile_image=%s, availability = %s, location = %s, experience = %s, institution_name = %s, year = %s, amount = %s, working_hours = %s WHERE freelancer_id = %s''', (name, email,id1_pic, availability, location, experience, institution_name, year, amount, working, fid))
            # path = r"E:\freelancer_marketplace\static"
            path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
            if not os.path.exists(path):
                os.makedirs(path,exist_ok=True)
            #project_image_file.save(os.path.join(path, filename))
            pimage.save(os.path.join(path, filename))
            mydb.commit()
            cursor.close()
            flash('details updated successfully')
            return render_template('users_dashboard.html')
        
            
        return render_template('updatefreelanceraccount.html',fdetails=fdetails)

    return redirect(url_for('ulogin'))
#=======================enter company project details
@app.route('/entercomapnyprojectdetails',methods=['GET','POST'])
def entercomapnyprojectdetails():
    if session.get('company'):
        if request.method=="POST":
            project_name = request.form['project_name']
            description = request.form['description']
            bid_amount = request.form['bid_amount']
            skills = request.form['skills']
            requirements = request.form['requirements']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            job_location=request.form['job_location']
            # Convert bid_amount to decimal
            bid_amount_decimal = float(bid_amount)

            # Convert start_date and end_date to datetime objects
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            print(project_name,description,bid_amount,skills,requirements,start_date,end_date,job_location,bid_amount_decimal,start_date_obj,end_date_obj)
            print(session.get('company'))
            # Insert project details into company_projects table
            cursor = mydb.cursor(buffered=True)
            insert_query = 'INSERT INTO company_projects(gst_number, project_name, description, bid_amount, skills, requirements,job_location, start_date, end_date) VALUES(%s, %s, %s,%s, %s, %s, %s, %s, %s)'
            cursor.execute(insert_query, (session['company'], project_name, description, bid_amount_decimal, skills, requirements,job_location, start_date_obj, end_date_obj))
            mydb.commit()
            cursor.close()
            return redirect(url_for('company_dashboard'))  # Redirect to dashboard or any other page

        return render_template('enterprojectdetails.html')  # Render the form template

    return redirect(url_for('blogin'))
#=================company dashboard
@app.route('/company_dashboard',methods=['GET','POST'])
def company_dashboard():
    if session.get('company'):
        return render_template('company_dashboard.html')
    return redirect(url_for('blogin'))
#================= view the project details
@app.route('/viewprojectdetails')
def viewprojectdetails():
    if session.get('company'):
        cursor=mydb.cursor(buffered=True)
        # print('=====================',session['company'])
        cursor.execute('select * from company_projects where gst_number=%s', (session['company'],))
        projectdetails = cursor.fetchall()
        cursor.close()
        return render_template('viewprojectdetails.html',p=projectdetails)
    return redirect(url_for('blogin'))
#====================view everyone of the project details
@app.route('/viewprojecteveryone')
def viewprojecteveryone():
    
    cursor=mydb.cursor(buffered=True)
    # print('=====================',session['company'])
    cursor.execute('select * from company_projects')
    projectdetails = cursor.fetchall()
    cursor.close()
    return render_template('viewprojecteveryone.html',p=projectdetails)

#=============================reviews and ratings to the particular user
@app.route('/reviews_ratings/<id1>',methods=['GET','POST'])
def reviews_ratings(id1):
    #print("===============================",id1)
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from reviews where freelancer_id=%s',(id1,))
    reviews=cursor.fetchall()
    cursor = mydb.cursor(buffered=True)
    if request.method=="POST":
        name = request.form['name']
        review_text = request.form['review']
        rating = int(request.form['ratings'])  # Convert to integer for decimal field
        review_date = datetime.now().date()  # Get current date
        review_time = datetime.now().time()  # Get current time

        # Insert data into the reviews table
        cursor.execute('''INSERT INTO reviews (freelancer_id, reviewer_name, review_text, rating, review_date, review_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (id1, name, review_text, rating, review_date, review_time))

        mydb.commit()
        flash('review submitted successfully')
        return redirect(url_for('viewallfreelancers'))
    
    return redirect(url_for('viewallfreelancers'))
#=========================view all freelancers
@app.route('/viewallfreelancers')
def viewallfreelancers():
    cursor = mydb.cursor(buffered=True)
    
    cursor.execute('''
        SELECT f.name, f.profile_image, f.availability, f.experience, f.amount, s.skill_name AS skills, f.freelancer_id
        FROM freelancer AS f
        LEFT JOIN skills AS s ON f.freelancer_id = s.freelancer_id;
    ''')
    freelancers = cursor.fetchall()
    print('============================',freelancers)
    return render_template('viewallfreelancers.html', freelancers=freelancers)

#=================================view freelancers of the particular freelancer
@app.route('/viewfeeelancers/<id1>',methods=['GET','POST'])
def viewfreelancers(id1):
    print('=================',id1)
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from reviews where freelancer_id=%s',(id1,))
    reviews=cursor.fetchall()
    cursor.execute(''' SELECT f.freelancer_id,
        f.name AS freelancer_name,
        f.email AS freelancer_email,
        f.account_creation_date,
        f.profile_image,
        f.availability,
        f.location AS freelancer_location,
        f.experience,
        f.institution_name,
        f.year,
        f.username,
        f.amount,
        f.working_hours,
        p.project_id,
        p.project_name,
        p.description AS project_description,
        p.project_image,
        p.completion_date AS project_completion_date,
        s.skill_id,
        s.skill_name,
        c.certification_id,
        c.certification_name,
        c.certificate_image
    FROM 
        freelancer AS f
    LEFT JOIN 
        projects AS p ON f.freelancer_id = p.freelancer_id
    LEFT JOIN 
        skills AS s ON f.freelancer_id = s.freelancer_id
    LEFT JOIN 
        certifications AS c ON f.freelancer_id = c.freelancer_id WHERE 
            f.freelancer_id = %s;
    ''', (id1,))
    
 
    print("=================",id1)

    details=cursor.fetchall()
    print('===================================',details)
    # print('==============================',details)
    return render_template('viewfreelancer.html', detail=details,id1=id1,reviews=reviews)

@app.route('/contactus/<id1>',methods=['GET','POST'])
def contactus(id1):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select gst_number from company_projects where project_id=%s',(id1,))
    cnumber=cursor.fetchone()
    if request.method == "POST":
        name = request.form['name']
        message = request.form['message']
        email = request.form['email']
        phone = request.form['phnumber']

        # Insert data into the contactus table
        cursor.execute('''INSERT INTO contactus (gst_number, name, message, email, phone_number,projectid)
            VALUES (%s, %s, %s, %s, %s,%s)
        ''', (cnumber[0], name, message, email, phone,id1))

        mydb.commit()
        flash('Your message has been submitted successfully.')
        return redirect(url_for('viewprojecteveryone'))
#===================view business people contact us data
@app.route('/readcontactus')
def readcontactus():
    if session.get('company'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from contactus where gst_number=%s',[session['company'],])
        g=cursor.fetchall()
        return render_template('readcontactus.html',g=g)
    return redirect(url_for('blogin'))

app.run(use_reloader=True,debug=True)