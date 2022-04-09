import email
import re
from flask import Flask, render_template,request,redirect,url_for, flash,jsonify,session
import os
import pymongo
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from forms import RegistrationForm,LoginForm
import urllib.request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = '4a194391cf6c3fd5ab1fdcbfe53ec81e'

client = pymongo.MongoClient('mongodb+srv://timeline:timeline@timeline.lnis3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.registration     
todos = db.registration_details
fsd = db.fullstack_registrations


db= MongoEngine()
db.init_app(app)
UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf' ])

def allowed_file(filename):
     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def redirect_url():
    return request.args.get('next') or \
    request.referrer or \
    url_for('index')

@app.route("/list")    
def lists ():    
    #Display the all Tasks    
    todos_l = todos.find()    
    a1="active"    
    return render_template('admin.html',a1=a1,todos=todos_l,)  

@app.route("/")    
@app.route("/uncompleted")    
def tasks ():    
    #Display the Uncompleted Tasks    
    todos_l = todos.find({"done":"no"})    
    a2="active"    
    return render_template('index.html',a2=a2,todos=todos_l)

@app.route("/action", methods=['POST'])    
def action ():    
    name=request.values.get("name") 
    email=request.values.get("email") 
    contact=request.values.get("contact")  
    age=request.values.get("age")  
    gender=request.values.get("gender")  
    Qualification=request.values.get("Qualification")  
    internship=request.values.get("internship")  
    certificate=request.values.get("certificate")  
    resume=request.values.get("resume")     
        
    todos.insert_one({ "name": name,"email" : email,"contact": contact,"age" : age,"gender": gender, "Qualification" : Qualification, "internship": internship, "certificate" : certificate,"resume" : resume})    
    return redirect("/main") 

@app.route("/action1", methods=['POST'])    
def action1 ():    
    name=request.values.get("name") 
    email=request.values.get("email") 
    contact=request.values.get("contact")  
    age=request.values.get("age")  
    gender=request.values.get("gender")  
    Qualification=request.values.get("Qualification")  
    internship=request.values.get("internship")  
    certificate=request.values.get("certificate")  
    resume=request.values.get("resume")     
        
    fsd.insert_one({ "name": name,"email" : email,"contact": contact,"age" : age,"gender": gender, "Qualification" : Qualification, "internship": internship, "certificate" : certificate,"resume" : resume})    
    return redirect("/main")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'tamo@fynd' and form.password.data == '1234':
            flash('You have been logged in!', 'success')
        return redirect(url_for('admin'))
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', title='Login', form=form)



@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        session['dob'] = form.dob.data
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Register', form=form ,data=[('gender', 'Gender'), ('gender', 'female'), ('gender', 'male')], data2=[('Qualification', 'Qualification'), ('Qualification', 'HSC'), ('Qualification', 'M.TECH'),('Qualification', 'B.TECH'),('Qualification', 'DIPLOMA'),('Qualification', 'BSC-IT')] )

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['resume']
    filename = secure_filename(file.filename)
   
    if file and allowed_file(file.filename):
       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       usersave = RegistrationForm(resume=file.filename)
       usersave.save()
       flash('File successfully uploaded ' + file.filename + ' to the database!')
       return redirect('/')
    else:
       flash('Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif') 
    return redirect('/index.html')

@app.route('/signup/')
def signup():
   return render_template('signup.html')

@app.route('/signup2/')
def signup2():
   return render_template('signup2.html')

@app.route('/admin/')
def admin():
   return render_template('admin.html')

@app.route('/checkregister/')
def checkregister():
   return render_template('checkregister.html')

@app.route('/checkpython/')
def checkpython():
   return render_template('checkpython.html')

@app.route('/main/')
def mainpage():
   return render_template('index.html')


@app.route("/getvalues", methods=['POST'])
def getvalues():
    y = todos.find()

@app.route('/fetch')
def query_records():
    return  render_template('/register1.html')

@app.route('/file/<resume>')
def file(resume):
    return db.send_file(resume)

@app.route('/get_values')
def index():
    reg_list = todos.find().limit(10)     
    return render_template('/checkpython.html', reg_list = reg_list)

@app.route('/get_values_fsd')
def indexfsd():
    reg_list1 = fsd.find().limit(10)     
    return render_template('/checkfullstack.html', reg_list1 = reg_list1)

if __name__ == '__main__':    
     app.run(debug=True) 