import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, g, request, url_for, redirect, session
import sqlite3
import random
import pandas as pd
import base64

DATABASE = 'tthpl.db'
DEBUG = True
SECRET_KEY = 'jksdfsdfghjklsertyugfvbfghjkdfjiosdf'
upload_folder='static/images/'


app = Flask(__name__)
app.config['upload_folder']=upload_folder
app.config.from_object(__name__)
app.config.from_envvar('TTHPL_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
		

@app.route("/")
def index():
	return render_template("index.html",error=request.args.get('error'))
	
	
		

@app.route("/foundation")
def foundation():
	return render_template("foundation.html")

	
@app.route("/oat")
def oat():
	return render_template("oat.html")
	
		

@app.route("/insaf")
def insaf():
	return render_template("insaf.html")
	
		

@app.route("/activity/<e>")
def activity(e):
	return render_template("activity.html",tab=e)
	
		
	
@app.route("/team")
def team():
	return render_template("team.html")
	
		

@app.route("/faq")
def faq():
	return render_template("faq.html")
	
		


@app.route('/register/<e>')
def register(e):
	return render_template("register.html",tab=e)


	
@app.route("/school-login")
def school_login():
	#id=session.get('school_id')
	#if bool(id):
	#	return redirect(url_for('school_loggedin',school_id=id))
	#else:
		return render_template("school-login.html")
		
		

@app.route("/student-login")
def student_login():
	#id=session.get('stud_id')
	#if bool(session.get('stud_id')):
	#	return redirect(url_for('stud_loggedin',stud_id=id))
	return render_template("student-login.html")
		

	
@app.route("/s_login", methods = ['GET','POST'])
def s_login():
	error = None
	if request.method == 'POST':
		email='admin@tthpl.com'
		pwd='tthpladminpwd'
		if request.form['email']== email and request.form['pwd']== pwd:
			id=base64.b64encode("1".encode())
			return redirect(url_for('loggedin',id=id))
		else:
			exists = g.db.execute('select * from school where Email = ? and Password = ? ',[request.form['email'],request.form['pwd']])
			l=exists.fetchall()
			if len(l):
				id=str(l[0][19])
				uid=base64.b64encode(id.encode())
				return redirect(url_for('school_loggedin',school_id=uid))
			else:
				error = 'Invalid Login. Try Again.'
				return redirect(url_for('school_login',error=error))
	
	
@app.route("/stud_login", methods = ['GET','POST'])
def stud_login():
	error = None
	if request.method == 'POST':
		email='admin@tthpl.com'
		pwd='tthpladminpwd'
		if request.form['email']== email and request.form['pwd']== pwd:
			id=base64.b64encode("1".encode())
			return redirect(url_for('loggedin',id=id))
		else:
			exists = g.db.execute('select * from student where Email = ? and Password = ? ',[request.form['email'],request.form['pwd']])
			l=exists.fetchall()
			if len(l):
				id=str(l[0][17])
				uid=base64.b64encode(id.encode())
				return redirect(url_for('stud_loggedin',stud_id=uid))
			else:
				error = 'Invalid Login. Try Again.'
				return redirect(url_for('student_login',error=error))
	
	
@app.route("/loggedin")
def loggedin():
	if(request.args.get('id')):
		school_posts = g.db.execute('select * from school ').fetchall()
		student_posts = g.db.execute('select * from student ').fetchall()
		volunteer_posts = g.db.execute('select * from volunteer ').fetchall()
		internship_posts = g.db.execute('select * from internship ').fetchall()
		business_posts = g.db.execute('select * from business ').fetchall()
		
		
		try:
			os.remove('static/files/school.xlsx')
			os.remove('static/files/student.xlsx')
			os.remove('static/files/volunteer.xlsx')
			os.remove('static/files/intern.xlsx')
			os.remove('static/files/business.xlsx')
			os.remove('static/files/donation.xlsx')
		except OSError:
			pass
		
		donate = g.db.execute('select * from donate').fetchall()	
		d_columns = ['Id', 'FirstName', 'LastName', 'Phone', 'Address', 'City', 'State', 'Zip', 'Email']
		
		d_df = pd.DataFrame(data=list(donate),columns=d_columns)
		d_writer = pd.ExcelWriter('static/files/donation.xlsx')
		d_df.to_excel(d_writer, sheet_name='main')
		d_writer.save()

		
		school = g.db.execute('select Id, SId, SchoolName, Board, Type, PhoneNumber, Address, City, State, Zip, Email, Password, Website, c1Name, c1Designation, c1Phone, c1Email, c2Name, c2Designation, c2Phone, c2Email from school').fetchall()	
		sc_columns = ['Id', 'SId', 'SchoolName', 'Board', 'Type', 'PhoneNumber', 'Address', 'City', 'State', 'Zip', 'Email', 'Password', 'Website', 'c1Name', 'c1Designation', 'c1Phone', 'c1Email', 'c2Name', 'c2Designation', 'c2Phone', 'c2Email']
		
		sc_df = pd.DataFrame(data=list(school),columns=sc_columns)
		sc_writer = pd.ExcelWriter('static/files/school.xlsx')
		sc_df.to_excel(sc_writer, sheet_name='main')
		sc_writer.save()
		
		
		student = g.db.execute('select Id, FirstName, LastName, Dob, Gender, Class, Section, RollNo, SchoolName, PhoneNumber, PName, ParentMobile, ParentWork, Address, City, State, Zip, Email, Password, Percentage from student').fetchall()	
		st_columns = ['Id', 'FirstName', 'LastName', 'Dob', 'Gender', 'Class', 'Section', 'RollNo', 'SchoolName', 'StudentPhoneNumber', 'PName', 'ParentMobile', 'ParentWork', 'Address', 'City', 'State', 'Zip', 'Email', 'Password', 'Percentage']
		
		st_df = pd.DataFrame(data=list(student),columns=st_columns)
		st_writer = pd.ExcelWriter('static/files/student.xlsx')
		st_df.to_excel(st_writer, sheet_name='main')
		st_writer.save()
		
		
		volunteer = g.db.execute('select Id, FirstName, LastName, Dob, PhoneNumber, Address, City, State, Zip, Email, Skills, MaritalStatus, Mentoring, Tutoring, Teaching, Counselling, CompetitionActivities, FundRaising, ProjectsEvents, Sporting, PreferredDays, PreferredTiming from volunteer').fetchall()	
		v_columns = ['Id', 'FirstName', 'LastName', 'Dob', 'PhoneNumber', 'Address', 'City', 'State', 'Zip', 'Email', 'Skills', 'MaritalStatus', 'Mentoring', 'Tutoring', 'Teaching', 'Counselling', 'CompetitionActivities', 'FundRaising', 'ProjectsEvents', 'Sporting', 'PreferredDays', 'PreferredTiming']
		
		v_df = pd.DataFrame(data=list(volunteer),columns=v_columns)
		v_writer = pd.ExcelWriter('static/files/volunteer.xlsx')
		v_df.to_excel(v_writer, sheet_name='main')
		v_writer.save()
		
		
		intern = g.db.execute('select Id, FirstName, LastName, Dob, Gender, PhoneNumber, Address, City, State, Zip, Email, Languages, University, AdditionalCourses, SpecificSkills, Months, FromDate, ToDate, Interest, Location, Motivation from internship').fetchall()	
		i_columns = ['Id', 'FirstName', 'LastName', 'Dob', 'Gender', 'PhoneNumber', 'Address', 'City', 'State', 'Zip', 'Email', 'Languages', 'University', 'AdditionalCourses', 'SpecificSkills', 'Months', 'FromDate', 'ToDate', 'Interest', 'Location', 'Motivation']
		
		i_df = pd.DataFrame(data=list(intern),columns=i_columns)
		i_writer = pd.ExcelWriter('static/files/intern.xlsx')
		i_df.to_excel(i_writer, sheet_name='main')
		i_writer.save()
		
		
		business = g.db.execute('select Id, FirstName, LastName, Dob, Occupation, Gender, PhoneNumber, Address, City, State, Zip, Email, PAN, Location from business').fetchall()	
		b_columns = ['Id', 'FirstName', 'LastName', 'Dob', 'Occupation', 'Gender', 'PhoneNumber', 'Address', 'City', 'State', 'Zip', 'Email', 'PAN', 'Location']
		
		b_df = pd.DataFrame(data=list(business),columns=b_columns)
		b_writer = pd.ExcelWriter('static/files/business.xlsx')
		b_df.to_excel(b_writer, sheet_name='main')
		b_writer.save()
		
		return render_template("loggedin.html",school_posts=school_posts,student_posts=student_posts,volunteer_posts=volunteer_posts,internship_posts=internship_posts,business_posts=business_posts,donate_posts=donate)
	else:
		return redirect(url_for('index'))
	
		

@app.route("/school_loggedin")
def school_loggedin():
	uid=request.args.get('school_id')
	id=base64.b64decode(uid.decode())
	school = g.db.execute('select * from school where Id=?',[id]).fetchall()
	school_code=school[0][20]
	stud = g.db.execute('select * from student where SchoolName=? order by Class',[school_code]).fetchall()
	return render_template("school_loggedin.html",posts=school[0],stud_posts=stud)	
		

@app.route("/stud_loggedin")
def stud_loggedin():
	uid=request.args.get('stud_id')
	id=base64.b64decode(uid.decode())
	stud = g.db.execute('select * from student where Id=?',[id]).fetchall()
	rank = g.db.execute('select * from rank where Stud_Id=?',[id]).fetchall()
	return render_template("stud_loggedin.html",posts=stud[0],rank=rank[0])

	
	
	
@app.route("/school_logout")
def school_logout():
	return redirect(url_for('index'))		
	
	
@app.route("/stud_logout")
def stud_logout():
	return redirect(url_for('index'))	

		

@app.route("/school_reg", methods = ['GET', 'POST'])
def school_reg():
	error = None
	if request.method == 'POST':
		exists = g.db.execute('select * from school where SchoolName = ?',[request.form['sname']])
		if len(exists.fetchall()):
			error = 'School already exists'
			return redirect(url_for('register(school)',error=error))
		else:
			g.db.execute('insert into school values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[request.form['sname'],request.form['board'],request.form['type'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['pwd'],request.form['website'],request.form['c1name'],request.form['c1designation'],request.form['c1phone'],request.form['c1email'],request.form['c2name'],request.form['c2designation'],request.form['c2phone'],request.form['c2email'],None,request.form['sid']])
			g.db.commit()
			return redirect(url_for('index'))
	return error
		

@app.route("/student_reg", methods = ['GET', 'POST'])
def student_reg():
	error = None
	if request.method == 'POST':
		file=request.files['pic']
		filename=str(random.randrange(0,1000))+str(random.randrange(0,1000))+secure_filename(file.filename)
		abs_filename=os.path.join(app.config['upload_folder'],filename)
		file.save(abs_filename)
		exists = g.db.execute('select * from student where Email = ?',[request.form['email']])
		if len(exists.fetchall()):
			error = 'Student already exists'
			return redirect(url_for('register(student)',error=error))
		else:
			g.db.execute('insert into student values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[request.form['fname'],request.form['lname'],request.form['dob'],request.form['gender'],request.form['class'],request.form['section'],request.form['rollno'],request.form['sname'],request.form['pname'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['percent'],abs_filename,None,request.form['pwd'],request.form['mobile'],request.form['work'],None])
			g.db.commit()
			return redirect(url_for('index'))
	return error

	
		

@app.route("/business_reg", methods = ['GET', 'POST'])
def business_reg():
	error = None
	if request.method == 'POST':
		file=request.files['pic']
		filename=str(random.randrange(0,1000))+str(random.randrange(0,1000))+secure_filename(file.filename)
		abs_filename=os.path.join(app.config['upload_folder'],filename)
		file.save(abs_filename)
		
		r_file=request.files['resume']
		r_filename=str(random.randrange(0,1000))+str(random.randrange(0,1000))+secure_filename(r_file.filename)
		r_abs_filename=os.path.join(app.config['upload_folder'],r_filename)
		r_file.save(r_abs_filename)
		
		exists = g.db.execute('select * from business where FirstName = ?',[request.form['fname']])
		if len(exists.fetchall()):
			error = 'Business Partner already exists'
			return redirect(url_for('register(business)',error=error))
		else:
			g.db.execute('insert into business values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[request.form['fname'],request.form['lname'],request.form['dob'],request.form['occupation'],abs_filename,request.form['gender'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['pan'],r_abs_filename,request.form['location'],None])
			g.db.commit()
			return redirect(url_for('index'))
	return error

	
		

@app.route("/volunteer_reg", methods = ['GET', 'POST'])
def volunteer_reg():
	error = None
	if request.method == 'POST':
		exists = g.db.execute('select * from volunteer where FirstName = ?',[request.form['fname']])
		if len(exists.fetchall()):
			error = 'Volunteer already exists'
			return redirect(url_for('register',e='volunteer',error=error))
		else:
			mentor = 'mentor' in request.form
			tutor = 'tutor' in request.form
			teaching = 'teaching' in request.form
			counselling = 'counselling' in request.form
			organising = 'organising' in request.form
			fund = 'fund' in request.form
			projects = 'projects' in request.form
			sporting = 'sporting' in request.form
			g.db.execute('insert into volunteer values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[request.form['fname'],request.form['lname'],request.form['dob'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['skill'],request.form['marital'],mentor,tutor,teaching,counselling,organising,fund,projects,sporting,request.form['days'],request.form['time'],None])
			g.db.commit()
			return redirect(url_for('index'))
	return error

	
		

@app.route("/intern_reg", methods = ['GET', 'POST'])
def intern_reg():
	error = None
	if request.method == 'POST':
		file=request.files['pic']
		filename=str(random.randrange(0,1000))+str(random.randrange(0,1000))+secure_filename(file.filename)
		abs_filename=os.path.join(app.config['upload_folder'],filename)
		file.save(abs_filename)
		exists = g.db.execute('select * from internship where FirstName = ?',[request.form['fname']])
		if len(exists.fetchall()):
			error = 'Intern already exists'
			return redirect(url_for('register(internship)',error=error))
		else:
			g.db.execute('insert into internship values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[request.form['fname'],request.form['lname'],request.form['dob'],abs_filename,request.form['gender'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['language'],request.form['university'],request.form['courses'],request.form['skills'],request.form['months'],request.form['from'],request.form['to'],request.form['interest'],request.form['location'],request.form['motivation'],None])
			g.db.commit()
			return redirect(url_for('index'))
	return error



@app.route("/school_update", methods = ['GET', 'POST'])
def school_update():
	if request.method == 'POST':
		g.db.execute('update school set SchoolName=?, Board=?, Type=?, PhoneNumber=?, Address=?, City=?, State=?, Zip=?, Email=?, Website=?, c1Name=?, c1Designation=?, c1Phone=?, c1Email=?, c2Name=?, c2Designation=?, c2Phone=?, c2Email=?, SId=? where Id=?',[request.form['sname'],request.form['board'],request.form['type'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['website'],request.form['c1name'],request.form['c1designation'],request.form['c1phone'],request.form['c1email'],request.form['c2name'],request.form['c2designation'],request.form['c2phone'],request.form['c2email'],request.form['sid'],request.form['id']])
		g.db.commit()
		id=base64.b64encode("1".encode())
		return redirect(url_for('loggedin',id=id))
	

@app.route("/school_pers_update", methods = ['GET', 'POST'])
def school_pers_update():
	if request.method == 'POST':
		g.db.execute('update school set SchoolName=?, Board=?, Type=?, PhoneNumber=?, Address=?, City=?, State=?, Zip=?, Email=?, Password=?, Website=?, c1Name=?, c1Designation=?, c1Phone=?, c1Email=?, c2Name=?, c2Designation=?, c2Phone=?, c2Email=?, SId=? where Id=?',[request.form['sname'],request.form['board'],request.form['type'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['pwd'],request.form['website'],request.form['c1name'],request.form['c1designation'],request.form['c1phone'],request.form['c1email'],request.form['c2name'],request.form['c2designation'],request.form['c2phone'],request.form['c2email'],request.form['sid'],request.form['id']])
		g.db.commit()
		id=request.form['id'];
		uid=base64.b64encode(id.encode())
		return redirect(url_for('school_loggedin',school_id=uid))
	

@app.route("/student_update", methods = ['GET', 'POST'])
def student_update():
	if request.method == 'POST':
		 # path = g.db.execute('select Photo from student where Id=?',[request.form['id']]).fetchall()
		 # os.remove(path[0][0])
		 # file=request.files['pic']
		 # filename=str(random.randrange(0,1000))+str(random.randrange(0,1000))+secure_filename(file.filename)
		 # abs_filename=os.path.join(app.config['upload_folder'],filename)
		 # file.save(abs_filename)
		
		g.db.execute('update student set FirstName=?, LastName=?, Dob=?, Gender=?, Class=?, Section=?, RollNo=?, SchoolName=?, PName=?, PhoneNumber=?, Address=?, City=?, State=?, Zip=?, Email=?, Percentage=?, ParentMobile=?, ParentWork=? where Id=?',[request.form['fname'],request.form['lname'],request.form['dob'],request.form['gender'],request.form['class'],request.form['section'],request.form['rollno'],request.form['sname'],request.form['pname'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['percent'],request.form['mobile'],request.form['work'],request.form['id']])
		g.db.commit()
		id=base64.b64encode("1".encode())
		return redirect(url_for('loggedin',id=id))


@app.route("/student_pers_update", methods = ['GET', 'POST'])
def student_pers_update():
	if request.method == 'POST':
		# path = g.db.execute('select Photo from student where Id=?',[request.form['id']]).fetchall()
		# os.remove(path[0][0])
		# file=request.files['pic']
		# filename=str(random.randrange(0,1000))+str(random.randrange(0,1000))+secure_filename(file.filename)
		# abs_filename=os.path.join(app.config['upload_folder'],filename)
		# file.save(abs_filename)
		
		g.db.execute('update student set FirstName=?, LastName=?, Dob=?, Gender=?, Class=?, Section=?, RollNo=?, SchoolName=?, PName=?, PhoneNumber=?, Address=?, City=?, State=?, Zip=?, Email=?, Password=?, Percentage=?, ParentMobile=?, ParentWork=? where Id=?',[request.form['fname'],request.form['lname'],request.form['dob'],request.form['gender'],request.form['class'],request.form['section'],request.form['rollno'],request.form['sname'],request.form['pname'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['pwd'],request.form['percent'],request.form['mobile'],request.form['work'],request.form['id']])
		g.db.commit()
		id=request.form['id']
		uid=base64.b64encode(id.encode())
		return redirect(url_for('stud_loggedin',stud_id=uid))
		

@app.route("/volunteer_update", methods = ['GET', 'POST'])
def volunteer_update():
	if request.method == 'POST':
		mentor = 'mentor' in request.form
		tutor = 'tutor' in request.form
		teaching = 'teaching' in request.form
		counselling = 'counselling' in request.form
		organising = 'organising' in request.form
		fund = 'fund' in request.form
		projects = 'projects' in request.form
		sporting = 'sporting' in request.form
		g.db.execute('update volunteer set FirstName=?, LastName=?, Dob=?, PhoneNumber=?, Address=?, City=?, State=?, Zip=?, Email=?, Skills=?, MaritalStatus=?, Mentoring=?, Tutoring=?, Teaching=?, Counselling=?, CompetitionActivities=?, FundRaising=?, ProjectsEvents=?, Sporting=?, PreferredDays=?, PreferredTiming=? where Id=?',[request.form['fname'],request.form['lname'],request.form['dob'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['skill'],request.form['marital'],mentor,tutor,teaching,counselling,organising,fund,projects,sporting,request.form['days'],request.form['time'],request.form['id']])
		g.db.commit()
		id=base64.b64encode("1".encode())
		return redirect(url_for('loggedin',id=id))
	

@app.route("/intern_update", methods = ['GET', 'POST'])
def intern_update():
	if request.method == 'POST':
		# path = g.db.execute('select Picture from internship where Id=?',[request.form['id']]).fetchall()
		# os.remove(path[0][0])
		# file=request.files['pic']
		# filename=str(random.randrange(0,1000))+str(random.randrange(0,1000))+secure_filename(file.filename)
		# abs_filename=os.path.join(app.config['upload_folder'],filename)
		# file.save(abs_filename)
		
		g.db.execute('update internship set FirstName=?, LastName=?, Dob=?, Gender=?, PhoneNumber=?, Address=?, City=?, State=?, Zip=?, Email=?, Languages=?, University=?, AdditionalCourses=?, SpecificSkills=?, Months=?, FromDate=?, ToDate=?, Interest=?, Location=?, Motivation=? where Id=?',[request.form['fname'],request.form['lname'],request.form['dob'],request.form['gender'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['language'],request.form['university'],request.form['courses'],request.form['skills'],request.form['months'],request.form['from'],request.form['to'],request.form['interest'],request.form['location'],request.form['motivation'],request.form['id']])
		g.db.commit()
		id=base64.b64encode("1".encode())
		return redirect(url_for('loggedin',id=id))
	

@app.route("/business_update", methods = ['GET', 'POST'])
def business_update():
	if request.method == 'POST':
		# path = g.db.execute('select Picture from business where Id=?',[request.form['id']]).fetchall()
		# os.remove(path[0][0])
		# file=request.files['pic']
		# filename=str(random.randrange(0,1000))+str(random.randrange(0,1000))+secure_filename(file.filename)
		# abs_filename=os.path.join(app.config['upload_folder'],filename)
		# file.save(abs_filename)
		
		
		# r_path = g.db.execute('select Resume from business where Id=?',[request.form['id']]).fetchall()
		# os.remove(r_path[0][0])
		# r_file=request.files['resume']
		# r_filename=str(random.randrange(0,1000))+str(random.randrange(0,1000))+secure_filename(r_file.filename)
		# r_abs_filename=os.path.join(app.config['upload_folder'],r_filename)
		# r_file.save(r_abs_filename)
		
		g.db.execute('update business set FirstName=?, LastName=?, Dob=?, Occupation=?,  Gender=?, PhoneNumber=?, Address=?, City=?, State=?, Zip=?, Email=?, PAN=?, Location=? where Id=?',[request.form['fname'],request.form['lname'],request.form['dob'],request.form['occupation'],request.form['gender'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['pan'],request.form['location'],request.form['id']])
		g.db.commit()
		id=base64.b64encode("1".encode())
		return redirect(url_for('loggedin',id=id))
	
	
	
@app.route("/remove_school", methods = ['GET', 'POST'])
def remove_school():
	g.db.execute('delete from school where Id = ?',[request.form['remove']])
	g.db.commit()
	id=base64.b64encode("1".encode())
	return redirect(url_for('loggedin',id=id))
	
	
@app.route("/remove_student", methods = ['GET', 'POST'])
def remove_student():
	g.db.execute('delete from student where Id = ?',[request.form['remove']])
	g.db.commit()
	id=base64.b64encode("1".encode())
	return redirect(url_for('loggedin',id=id))
	
	
@app.route("/remove_volunteer", methods = ['GET', 'POST'])
def remove_volunteer():
	g.db.execute('delete from volunteer where Id = ?',[request.form['remove']])
	g.db.commit()
	id=base64.b64encode("1".encode())
	return redirect(url_for('loggedin',id=id))
	
	
@app.route("/remove_intern", methods = ['GET', 'POST'])
def remove_intern():
	g.db.execute('delete from internship where Id = ?',[request.form['remove']])
	g.db.commit()
	id=base64.b64encode("1".encode())
	return redirect(url_for('loggedin',id=id))
	
	
@app.route("/remove_business", methods = ['GET', 'POST'])
def remove_business():
	g.db.execute('delete from business where Id = ?',[request.form['remove']])
	g.db.commit()
	id=base64.b64encode("1".encode())
	return redirect(url_for('loggedin',id=id))
	

@app.route("/pic_upload", methods = ['GET', 'POST'])
def pic_upload():
	error = None
	file=request.files['pic']
	filename=file.filename
	if(filename==""):
		error="Upload Photo before Submitting!!"
	else:
		 path = g.db.execute('select Photo from student where Id=?',[request.form['id']]).fetchall()
		 os.remove(path[0][0])
		 filename=str(random.randrange(0,1000))+str(random.randrange(0,1000))+secure_filename(filename)
		 abs_filename=os.path.join(app.config['upload_folder'],filename)
		 file.save(abs_filename)
		 g.db.execute('update student set Photo=? where Id=?',[abs_filename,request.form['id']])
		 g.db.commit()
	id=request.form['id']
	uid=base64.b64encode(id.encode())
	return redirect(url_for('stud_loggedin',stud_id=uid,error=error))
	
	
@app.route("/donate", methods = ['GET', 'POST'])
def donate():
	error = None
	if request.method == 'POST':
		g.db.execute('insert into donate values (?,?,?,?,?,?,?,?,?)',[None,request.form['fname'],request.form['lname'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email']])
		g.db.commit()
		return redirect(url_for('foundation'))
	return error
	
	
@app.route("/donate_update", methods = ['GET', 'POST'])
def donate_update():
	if request.method == 'POST':
		g.db.execute('update donate set FirstName=?, LastName=?, PhoneNumber=?, Address=?, City=?, State=?, ZipCode=?, Email=? where Id=?',[request.form['fname'],request.form['lname'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['id']])
		g.db.commit()
		id=base64.b64encode("1".encode())
		return redirect(url_for('loggedin',id=id))
		
	
@app.route("/remove_donator", methods = ['GET', 'POST'])
def remove_donator():
	g.db.execute('delete from donate where Id = ?',[request.form['remove']])
	g.db.commit()
	id=base64.b64encode("1".encode())
	return redirect(url_for('loggedin',id=id))
		

@app.route("/oat_ranks")
def oat_ranks():
	g.db.execute('delete from rank')
	g.db.commit()
	students = g.db.execute('select Id, Score from student').fetchall()
	length= len(students)
	for count in range(length):
		g.db.execute('insert into rank values (?,?,?,?,?,?)',[students[count][0],students[count][1],None,None,None,None])
		count=count+1
	for i in range(11):
		nation = g.db.execute('select Id from student where Class=? order by Score desc',[i]).fetchall()
		l= len(nation)
		for j in range(l):
			g.db.execute('update rank set NationalRank=? where Stud_Id=?',[j+1,nation[j][0]])
		states=g.db.execute('select distinct State from student where Class=?',[i]).fetchall()
		m=len(states)
		for k in range(m):
			state=g.db.execute('select Id from student where State=? and Class=? order by Score desc',[states[k][0],i]).fetchall()
			x=len(state)
			for a in range(x):
				g.db.execute('update rank set StateRank=? where Stud_Id=?',[a+1,state[a][0]])
		schools=g.db.execute('select distinct SchoolName from student where Class=?',[i]).fetchall()
		n=len(schools)
		for o in range(n):
			school=g.db.execute('select Id from student where SchoolName=? and Class=? order by Score desc',[schools[o][0],i]).fetchall()
			y=len(school)
			for b in range(y):
				g.db.execute('update rank set SchoolRank=? where Stud_Id=?',[b+1,school[b][0]])
			sections=g.db.execute('select distinct Section from student where SchoolName=? and Class=?',[schools[o][0],i]).fetchall()
			p=len(sections)
			for c in range(p):
				section=g.db.execute('select Id from student where Section=? and SchoolName=? and Class=? order by Score desc',[sections[c][0],schools[o][0],i]).fetchall()
				z=len(section)
				for d in range(z):
					g.db.execute('update rank set ClassRank=? where Stud_Id=?',[d+1,section[d][0]])
	g.db.commit()
	return redirect(url_for('index'))



	
@app.route('/clean')
def clean():
	g.db.execute('delete from school')
	g.db.execute('delete from student')
	g.db.execute('delete from business')
	g.db.execute('delete from volunteer')
	g.db.execute('delete from internship')
	g.db.commit()
	return "Database cleaned!!"

if __name__ == '__main__' :
        app.debug = True
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
