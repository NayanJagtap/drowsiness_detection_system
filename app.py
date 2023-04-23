

from re import L
from sqlite3 import Cursor
from ssl import SSLSession
from urllib import request
from flask import Flask,render_template,request,redirect,url_for,session,Response
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import random
import MySQLdb.cursors
import cv2
import mysql.connector
import json
from playsound import playsound

app=Flask(__name__)
#camera=cv2.VideoCapture(0)
app.secret_key="login"
#database connection details

# Establish a connection to the MySQL database
db = mysql.connector.connect(
  host="db4free.net",
  user="nayanjagtap",
  password="nayanjagtap",
  database="nayanjagtap"
)


app.config['MYSQL_HOST']='db4free.net'
app.config['MYSQL_USER']='nayanjagtap'
app.config['MYSQL_PASSWORD']='nayanjagtap'
app.config['MYSQL_DB']='nayanjagtap'

mysql=MySQL(app)
def generate_frames():
   while True:
            
#         ## read the camera frame
     #success,frame=camera.read()
    
        
     
        #this is opencv library for basic image processing functions
#to install opencv "c conda-forge opencv"
#or !pip install opencv-python
            import cv2
            #this is for array related functions
            import numpy as np

            #installing cmake
            #!pip install cmake

            #checking python version
            #!python --version



            #   installing dlib via file
            # !pip install "C:\Users\NAYAN DINKAR JAGTAP\Downloads\Dlib-python whl packages\Dlib-python whl packages\dlib-19.22.99-cp38-cp38-win_amd64.whl"


            #dlib is used for deeplearning based modules and face landmark detection
            import dlib


            #installing imutils
            #!pip install imutils


            from imutils import face_utils
            sound_file_path = 'static/alarm.mp3'


            #initializing the camera and taking the instance
            cap=cv2.VideoCapture(0)

            #intializing the face detector and landmark detector
            detector=dlib.get_frontal_face_detector()
            #get frontal face detector is an inbuilt function of dlib library which gives dlib's machine learning frontal face detector
            #which is more accurate than harr cascasde of opencv,it do not requires any input as a file

            #this will help in predicting 68 crutial land marks like eye-brows,lips,etc and it is commonly used in augumented reality like 
            #snapchat filters
            predictor=dlib.shape_predictor( "C:\\Users\\NAYAN DINKAR JAGTAP\\Desktop\\Project\\project pp\\new\\archive\\shape_predictor_68_face_landmarks.dat")
               
            #current states of variables
            sleep=0
            drowsy=0
            active=0
            status=""
            color=(0,0,0)

            #the distance between two points,lets say one point is at one end of right eye and other point is at one end of the left eye so 
            #the distance between both the points can be calculated by eucledian distance,but here is the inbuit formula for that.
            def compute(ptA,ptB):
                dist=np.linalg.norm(ptA-ptB)
                return dist

            #one eye has 6 crutial points
            #     .  .    
            #  .        .
            #     .  .
            def blinked(a,b,c,d,e,f): 
                up=compute(b,d)+compute(c,e) #adding both short distances
                down=compute(a,f) #computing distance between the long distance 
                ratio=up/(2.0*down)
                
            #this ratio will help us in determining whether the eye is closed,blinking or not etc 
            #after experimenting 0.25 is the determined ratio or a threshold ratio  if greater than 0.25 then eye is opened else closed

            #checking whether the eye is blonking or not
                if(ratio>0.25):
                    return 2
                elif(ratio>0.21 and ratio<=0.25):
                    return 1
                else:
                    return 0
                
            while True:
                _,frame= cap.read()
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces=detector(gray) #calling frontal face detector
                #detected face in faces array
                face_frame=frame.copy()
                for face in faces: #the rectangle generated will be because of this 
                    x1=face.left()          #these are the coordinates for the rectangle
                    y1=face.top()
                    x2=face.right()
                    y2=face.bottom()
                    
                    face_frame=frame.copy()
                    cv2.rectangle(face_frame,(x1,y1),(x2,y2),(0,255,0),2)
                    
                    landmarks=predictor(gray,face)
                    landmarks=face_utils.shape_to_np(landmarks) #shaped into numpyarray
                    
                    left_blink=blinked(landmarks[36],landmarks[37],landmarks[38],landmarks[41],landmarks[40],landmarks[39])
                    right_blink=blinked(landmarks[42],landmarks[43],landmarks[44],landmarks[47],landmarks[46],landmarks[45])
                    
                    #judging whether the driver is blinling,sleepy,active etc
                    
                    if(left_blink==0 or right_blink==0):   #in the blinked function there are 6 parameters of the eyes a,b,c,d,e,f,ratio
                        #is calculated and 0,1,2 is returned according to it these three conditions will execute
                        sleep+=1
                        drowsy=0
                        active=0
                        if(sleep>6):   #if sleepy status exceeds 6 frames then
                            status="!!!SLEEPING!!!"
                            color=(255,0,0)
                            playsound(sound_file_path)


                    elif(left_blink==1 or right_blink==1):
                        sleep=0
                        active=0
                        drowsy+=1
                        if(drowsy>6):
                            status="DROWSY !"
                            color=(0,0,225)
                            sound_file_drowsy = 'static/drowsy.mp3'
                            playsound(sound_file_drowsy)
                            
                                
                    else:
                        drowsy=0
                        sleep=0
                        active+=1
                        if(active>6):
                            status="ACTIVE:"
                            color=(0,255,0)

                    cv2.putText(frame,status,(100,100),cv2.FONT_HERSHEY_SIMPLEX,1.2,color,3)#text putting(conditions,status etc),colors putting

                    for n in range(0,68):
                        (x,y)=landmarks[n]
                        cv2.circle(face_frame,(x,y),1,(255,0,0),-1)  #these are the landmarks 
                
                # cv2.imshow("FRAME",frame)
                # cv2.imshow("RESULT OF DETECTOR",face_frame)
                ret,buffer=cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()
                yield(b'--frame\r\n' b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')

                # key=cv2.waitKey(1)
                # if key==0:
                #    break

    

    
        
        
        


            
        #     ret,buffer=cv2.imencode('.jpg',frame)
        #     frame=buffer.tobytes()

        # yield(b'--frame\r\n'
        #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# @app.route('/')
# def videopage():
#     return render_template('videopage.html')

@app.route('/')
def first():
    return render_template('first.html')

@app.route('/second')
def second():
    return render_template('second.html')


@app.route('/third')
def third():
    return render_template('third.html')

@app.route('/loginforowner')
def loginforowner():
    return render_template('loginforowner.html')

# @app.route('/DriverLogin')
# def DriverLogin():
#     return render_template('DriverLogin.html')



@app.route('/login_validation',methods=['GET','POST'])
def login_validation():
    msg=' something went wrong'
     # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method=='POST' and 'email' in request.form and 'password' in request.form:
        email=request.form['email']
        password=request.form['password']
        # Check if account exists using MySQL
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
                # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['user_id']
            session['email'] = account['email']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('loginforowner.html',msg='')

@app.route('/login_validation/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        #return render_template('homepage.html', email=session['email'])
        return redirect(url_for('drivers'))
    # User is not loggedin redirect to login page
    return redirect(url_for('loginforowner'))






##########################################################################################################
####### for homepage.html ##############
@app.route('/drivers')
def drivers():
    # Execute a SELECT query to fetch the names from the drivers table
    cursor=db.cursor()
    query = 'SELECT name, vehicle FROM drivers'
    cursor.execute(query)
    data = cursor.fetchall()
    names = []
    for row in data:
        names.append(row)
    # Render the template with the list of names
    return render_template('homepage.html', names=names)


    

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        firstName = request.form['firstName']
        secondName=request.form['secondName']
        phoneNo=request.form['phoneNo']
        email=request.form['email']
        password=request.form['password']
        vehicleno=request.form['vehicleno']
        query = "SELECT * FROM users WHERE email = %s AND vehicleno = %s"
        param = (email,vehicleno)
        cursor = db.cursor()
        cursor.execute(query,param)
        result = cursor.fetchone()
        if result:
            print("Data already exists")
            return "Data already exists"
        else:
            query = "INSERT INTO users (firstName,secondName,phoneNo,email,password,vehicleno) VALUES (%s, %s,%s,%s,%s,%s)"
            params = (firstName,secondName,phoneNo,email,password,vehicleno)
            cursor.execute(query, params)
            db.commit()
            print("Data inserted successfully")
            return "Data inserted successfully"
    else:
        return render_template('registration.html')




#################################################################################################################################################

@app.route('/video', methods=['GET', 'POST'])
def video():
    if request.method == 'POST' and 'submit' in request.form:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('popup.html', show_popup=True)




#############################################################


##########################################################
@app.route('/directlydriverlogin')
def directlydriverlogin():
    return render_template('DriverLogin.html')
#############################################################


with open('config.json','r') as f:
    params=json.load(f)['params']

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']=params['gmail-user']
app.config['MAIL_PASSWORD']=params['gmail-password']
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail =Mail(app)
otp=random.randint(0000,9999)

@app.route('/DriverLogin' ,methods=['GET', 'POST'])
def DriverLogin():
    email=request.form['email']
    msg = Message("OTP" , sender='nayandinkarjagtap@gmail.com',recipients=[email])
    msg.body=str(otp)
    mail.send(msg)
    return render_template("DriverLogin.html")

@app.route('/validate',methods=["POST"])
def validate():
    password=request.form['otp']
    if otp==int(password):
         return redirect(url_for('video'))
    return render_template('DriverLogin.html',msg="OTP is Wrong! try again")

if __name__=="__main__":
   # app.run(debug=True)
    app.run(port=5000)