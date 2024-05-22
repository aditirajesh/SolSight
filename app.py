from flask import Flask,render_template,request,redirect,url_for,session,flash,jsonify # type: ignore
import pandas as pd
import os
import matplotlib.pyplot as plt
from PIL import Image

#from werkzeug.utils import secure_filename
from xgboostpast import xg_boost_past
app = Flask(__name__)
app.secret_key = os.urandom(24)


def makeimg(us,src,data):
    fig, ax = plt.subplots()
    x=[]
    real = []
    predict =[]
    for i in data:
        x.append(list(i.keys())[0])
        predict.append(list(i.values())[0][0])
        real.append(list(i.values())[0][1])
    ax.set_title(f'Predicted vs actual yield for {src}')
    ax.plot(x, predict, label = 'predicted yield')
    ax.plot(x,real,label='actual yield')
    ax.legend()
    fig.canvas.draw()
    buf = fig.canvas.tostring_rgb()
    width, height = fig.canvas.get_width_height()
    pil_image = Image.frombytes("RGB", (width, height), buf)
    path =f'{os.getcwd()}/static/{us}/{src}.png'
    pil_image.save(path)

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
    paths =f'\datasets\{username}'
    n = f'\static\{username}'
    cwd = os.getcwd()
    s = cwd + paths
    p = cwd+n
    try:
        os.mkdir(s)
        os.mkdir(p)
    except:
        print()


@app.route('/')
def home():
    m=''
    if 'user' in session:
        return render_template("home.html",user = session['user'])
    return render_template("home.html",user = m)

@app.route('/signin', methods=['POST','GET'])
def signin():
   m = ''
   if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if getpass(username)==password:
            session['user'] = username
            return redirect( url_for("home"))
        else:
            m = 'invalid username or password'
            return render_template("signin.html",message = m)          
   return render_template("signin.html",message=m)

@app.route('/analytics')
def analytics():
    if 'user' in session:
        path = f'datasets/{session['user']}'
        pred = {}
        fur = {}
        effic = []
        files = [f for f in os.listdir(path)]
        pds = {}
        for f in files:
            d = (open(f'{path}/{f}',mode = 'r').read())
            f = f.split('.')[0]
            pds[f] = d
            pred[f],a = (xg_boost_past(session['user'],f))
            effic.append(a)
            fur[f] = a
            makeimg(session['user'],f,pred[f])
        return render_template("analy.html",pred = pred,user=session['user'],ef = fur,pds = pds)
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
            session['user'] = username
            return redirect( url_for("home"))
   return render_template("sign_up.html")


@app.route('/upload',methods = ['GET','POST'])
def upload():
    m =''
    if 'user' in session:
        if request.method == 'POST':
            # Get the source name from the form
            source_name = request.form['name']
            
            # Get the uploaded file
            file = request.files['file']
            df = pd.read_csv(file)
            # If a file was uploaded
            if list(df.columns) == ['DATE', 'AMBIENT_TEMP', 'MODULE_TEMP', 'SUN_HOURS', 'YIELD']:
                # Change the filename to the source name
                filename = (source_name + '.csv')  # Assuming it's a CSV file
                
                # Save the file with the new name
                path = os.path.join(f'datasets/{session['user']}', filename)
                df.to_csv(path,index=False)
                
                m = "File uploaded sucessfuly"
                return render_template('upload.html',message = m)
            else:
                m = "File is of incorrect format... Please upload of the format : \n 'DATE', 'AMBIENT_TEMP', 'MODULE_TEMP', 'SUN_HOURS', 'YIELD'"
                return render_template('upload.html',message = m) 
        else:
            return render_template('upload.html',message=m)
    else:
        return redirect( url_for('signin') )
    
@app.route('/get_data/<src>')
def get_data(src):
    if 'user' in session:
        path = f'datasets/{session['user']}/{src}.csv'
        data = {"csvText": open(path).read()}
        return jsonify(data)

if __name__ == '__main__':  
  app.run(debug = True)