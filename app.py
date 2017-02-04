from flask import Flask, render_template, g, request, url_for, redirect, session
import sqlite3

DATABASE = 'tthpl.db'
DEBUG = True
SECRET_KEY = 'jksdfsfghjkdfjiosdf'


app = Flask(__name__)
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
	if bool(session.get('s_id')):
		return redirect(url_for('school_loggedin'))
	if bool(session.get('abp_id')):
		return redirect(url_for('abp_loggedin'))
	return render_template("index.html")
	
	
		

@app.route("/foundation")
def foundation():
	if bool(session.get('s_id')):
		return redirect(url_for('school_loggedin'))
	if bool(session.get('abp_id')):
		return redirect(url_for('abp_loggedin'))
	return render_template("foundation.html")
	
		

@app.route("/oat")
def oat():
	if bool(session.get('s_id')):
		return redirect(url_for('school_loggedin'))
	if bool(session.get('abp_id')):
		return redirect(url_for('abp_loggedin'))
	return render_template("oat.html")
	
		

@app.route("/insaf")
def insaf():
	if bool(session.get('s_id')):
		return redirect(url_for('school_loggedin'))
	if bool(session.get('abp_id')):
		return redirect(url_for('abp_loggedin'))
	return render_template("insaf.html")
	
		

@app.route("/activity")
def activity():
	if bool(session.get('s_id')):
		return redirect(url_for('school_loggedin'))
	if bool(session.get('abp_id')):
		return redirect(url_for('abp_loggedin'))
	return render_template("activity.html")
	
		
	
@app.route("/team")
def team():
	if bool(session.get('s_id')):
		return redirect(url_for('school_loggedin'))
	if bool(session.get('abp_id')):
		return redirect(url_for('abp_loggedin'))
	return render_template("team.html")
	
		

@app.route("/faq")
def faq():
	if bool(session.get('s_id')):
		return redirect(url_for('school_loggedin'))
	if bool(session.get('abp_id')):
		return redirect(url_for('abp_loggedin'))
	return render_template("faq.html")
	
		

@app.route("/register")
def register():
	return render_template("register.html")
	
		

@app.route("/school_reg", methods = ['GET', 'POST'])
def school_reg():
	error = None
	if request.method == 'POST':
		exists = g.db.execute('select * from school where SchoolName = ?',[request.form['sname']])
		if len(exists.fetchall()):
			error = 'School already exists'
		else:
			g.db.execute('insert into school values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[request.form['sname'],request.form['board'],request.form['type'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['pwd'],request.form['website'],request.form['c1name'],request.form['c1designation'],request.form['c1phone'],request.form['c1email'],request.form['c2name'],request.form['c2designation'],request.form['c2phone'],request.form['c2email']])
			g.db.commit()
			return redirect(url_for('index'))
	return error
	
@app.route("/school-login")
def school_login():
	if bool(session.get('s_id')):
		return redirect(url_for('school_loggedin'))
	if bool(session.get('abp_id')):
		return redirect(url_for('abp_loggedin'))
	return render_template("school-login.html")
	
	
@app.route("/s_login", methods = ['GET','POST'])
def s_login():
	error = None
	if request.method == 'POST':
		if request.form['email']== 'admin@tthpl.com' and request.form['pwd']== 'tthpladminpwd':
			session['id']='admin'
			return redirect(url_for('loggedin'))
		else:
			exists = g.db.execute('select * from school where Email = ? and Password = ? ',[request.form['email'],request.form['pwd']])
			l=exists.fetchall()
			if len(l):
				session['s_id']=l[0][0]
				return redirect(url_for('school_loggedin'))
			else:
				error = 'Invalid'
	return error

	
@app.route("/loggedin")
def loggedin():
	school_posts = g.db.execute('select * from school ').fetchall()
	student_posts = g.db.execute('select * from student ').fetchall()
	volunteer_posts = g.db.execute('select * from volunteer ').fetchall()
	internship_posts = g.db.execute('select * from internship ').fetchall()
	business_posts = g.db.execute('select * from business ').fetchall()
	return render_template("loggedin.html",school_posts=school_posts,student_posts=student_posts,volunteer_posts=volunteer_posts,internship_posts=internship_posts,business_posts=business_posts)
	
	
@app.route("/logout")
def logout():
    session.pop('s_id', None)
    return redirect(url_for('index'))
		
	
		

@app.route("/student_reg", methods = ['GET', 'POST'])
def student_reg():
	error = None
	if request.method == 'POST':
		exists = g.db.execute('select * from student where FirstName = ?',[request.form['fname']])
		if len(exists.fetchall()):
			error = 'Student already exists'
		else:
			g.db.execute('insert into student values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[request.form['fname'],request.form['lname'],request.form['dob'],request.form['gender'],request.form['class'],request.form['section'],request.form['rollno'],request.form['sname'],request.form['pname'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['percent'],request.form['pic']])
			g.db.commit()
			return redirect(url_for('index'))
	return error

	
		

@app.route("/business_reg", methods = ['GET', 'POST'])
def business_reg():
	error = None
	if request.method == 'POST':
		exists = g.db.execute('select * from business where FirstName = ?',[request.form['fname']])
		if len(exists.fetchall()):
			error = 'Business Partner already exists'
		else:
			g.db.execute('insert into business values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[request.form['fname'],request.form['lname'],request.form['dob'],request.form['occupation'],request.form['pic'],request.form['gender'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['pan'],request.form['resume'],request.form['location']])
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
		else:
			mentor = 'mentor' in request.form
			tutor = 'tutor' in request.form
			teaching = 'teaching' in request.form
			counselling = 'counselling' in request.form
			organising = 'organising' in request.form
			fund = 'fund' in request.form
			projects = 'projects' in request.form
			sporting = 'sporting' in request.form
			g.db.execute('insert into volunteer values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[request.form['fname'],request.form['lname'],request.form['dob'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['skill'],request.form['marital'],mentor,tutor,teaching,counselling,organising,fund,projects,sporting,request.form['days'],request.form['time']])
			g.db.commit()
			return redirect(url_for('index'))
	return error

	
		

@app.route("/intern_reg", methods = ['GET', 'POST'])
def intern_reg():
	error = None
	if request.method == 'POST':
		exists = g.db.execute('select * from internship where FirstName = ?',[request.form['fname']])
		if len(exists.fetchall()):
			error = 'Intern already exists'
		else:
			g.db.execute('insert into internship values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[request.form['fname'],request.form['lname'],request.form['dob'],request.form['pic'],request.form['gender'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['zip'],request.form['email'],request.form['language'],request.form['university'],request.form['courses'],request.form['skills'],request.form['months'],request.form['from'],request.form['to'],request.form['interest'],request.form['location'],request.form['motivation']])
			g.db.commit()
			return redirect(url_for('index'))
	return error

	

@app.route("/news")
def news():
	if bool(session.get('s_id')):
		return redirect(url_for('school_loggedin'))
	if bool(session.get('abp_id')):
		return redirect(url_for('abp_loggedin'))
	return render_template("news.html")	
	
		

@app.route("/contact")
def contact():
	if bool(session.get('s_id')):
		return redirect(url_for('school_loggedin'))
	if bool(session.get('abp_id')):
		return redirect(url_for('abp_loggedin'))
	return render_template("contact.html")	

	
		

@app.route("/ABP-login")
def ABP_login():
	if bool(session.get('s_id')):
		return redirect(url_for('school_loggedin'))
	if bool(session.get('abp_id')):
		return redirect(url_for('abp_loggedin'))
	return render_template("ABP-login.html")
		

	
@app.route('/clean')
def clean():
	g.db.execute('delete from school')
	g.db.execute('delete from posts')
	g.db.commit()
	return "Database cleaned!!"


if __name__ == '__main__' :
	app.run()