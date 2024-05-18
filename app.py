from flask import Flask,render_template,request,redirect,url_for,session # type: ignore
import pandas as pd
import os
#from werkzeug.utils import secure_filename
from xgboostpast import xg_boost_past
app = Flask(__name__)
app.secret_key = os.urandom(24)

def getpass(username):
    users = pd.read_csv('userdata.csv')
    if username in list(users['username']):
        
        for _,i in users.iterrows():
            if i['username']==username:
                return i['password']
    else:
        print('yoooo')

def add_data(username,name,password):
    users = pd.read_csv('userdata.csv')
    if username in list(users['username']):
        return
    users.loc[len(users.index)] = [username,name,password]
    users.to_csv('userdata.csv',index=False)
    paths =f'/datasets/{username}'
    cwd = os.getcwd()
    path = os.path.join(cwd,paths)
    try:
        os.mkdir(path)
    except:
        print()


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signin', methods=['POST','GET'])
def signin():
   if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if getpass(username)==password:
            session['user'] = username
            return redirect( url_for("home")) 
   return render_template("signin.html")

@app.route('/analytics')
def analytics():
    if 'user' in session:
        path = f'datasets/{session['user']}'
        pred = {}
        files = [f for f in os.listdir(path)]
        for f in files:
            pred[f] = (xg_boost_past(session['user'],f))
        return render_template("analy.html",pred = pred)
    else:
        return redirect( url_for('signin') )
@app.route('/signup', methods=['POST','GET'])
def signup():
   if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        cpassword = request.form['cpassword']
        
        if password==cpassword:
            add_data(username,name,password)

            return redirect( url_for("home"))
   return render_template("sign_up.html")


@app.route('/upload',methods = ['GET','POST'])
def upload():
    if 'user' in session:
        if request.method == 'POST':
            # Get the source name from the form
            source_name = request.form['name']
            
            # Get the uploaded file
            file = request.files['file']
            
            # If a file was uploaded
            if file:
                # Change the filename to the source name
                filename = (source_name + '.csv')  # Assuming it's a CSV file
                
                # Save the file with the new name
                file.save(os.path.join(f'datasets/{session['user']}', filename))
                
                return 'File uploaded successfully!'
        else:
            return render_template('upload.html')
    else:
        return redirect( url_for('signin') )
@app.route('/ml')
def ml():
    return render_template('ml.html')

if __name__ == '__main__':  
  app.run(debug = True)