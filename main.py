# from flask import Flask,render_template
# import mysql.connector
import requests
import pickle
import numpy as np
from flask import *
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myfyp'
mysql = MySQL(app)




@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/home')
def Home():
    return render_template('home.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    msg1 = 'Welcome to Cyber Beep Application'
    msg2 = 'Credentials Mismatch'
    email = request.form.get('email')
    password = request.form.get('password')
    Cursor = mysql.connection.cursor()
    # Cursor.execute("""SELECT FROM `signup` WHERE `email` LIKE '{}' AND `password` LIKE '{}' """.format(email,password))
    Cursor.execute('SELECT * FROM signup WHERE email = % s AND password = % s', (email, password,))
    users = Cursor.fetchall()
    if len(users)>0:
        # flash("You are successfull logged in")
        return render_template('getBeep.html')

    else:
        return render_template('login.html')

@app.route('/add_user',methods=['POST'])
def Add_user():
    msg = None
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    Cursor = mysql.connection.cursor()
    # Cursor.execute("INSERT INTO signup VALUES (Null,'{}','{}','{}')".format(name,email,password,))
    Cursor.execute('INSERT INTO signup VALUES ( % s, % s, % s)', (name, email, password,))
    mysql.connection.commit()
    msg ='Successfully Registered, Now Login First to Proceed further'
    return render_template('login.html',msg=msg)

@app.route('/getBeep')
def GetBeep():

    return render_template('getBeep.html')

@app.route('/predict', methods=['POST'])
def Predict():

    location_dict = {'activity united states': 0, 'afghanistan': 1, 'agencies united states': 2, 'america': 3, 'argentina': 4, 'arizona': 5, 'arkansas': 6, 'around united kingdom': 7, 'arstechnica': 8, 'atlanta': 9, 'attributesas': 10, 'australia': 11, 'baghdad': 12, 'bagheri': 13, 'barcelona': 14, 'beaumont': 15, 'birmingham': 16, 'bloomberg': 17, 'bootx64': 18, 'boston': 19, 'brazil': 20, 'britain': 21, 'britain germany': 22, 'brywek': 23, 'bulgaria': 24, 'cairo': 25, 'california': 26, 'canada': 27, 'cdc united states national health': 28, 'chicago': 29, 'china': 30, 'cisco': 31, 'cnrp': 32, 'colombia': 33, 'cupertino': 34, 'curve25519': 35, 'dearth': 36, 'dublin': 37, 'emotetthe united states federal bureau': 38, 'estonia': 39, 'eu': 40, 'europe united states': 41, 'europol united kingdom': 42, 'ever united states': 43, 'exedonkey kong': 44, 'extradited united states': 45, 'florida': 46, 'france': 47, 'fraudsters united states': 48, 'gamaredon': 49, 'georgia': 50, 'germany': 51, 'goalsthe united states federal bureau': 52, 'grandoreiro': 53, 'hamburg': 54, 'hangzhou': 55, 'happydon': 56, 'harden': 57, 'hollywood': 58, 'hong kong': 59, 'https': 60, 'hungary': 61, 'india': 62, 'indiana': 63, 'indonesia': 64, 'inqtana': 65, 'interfacewe': 66, 'interpol united states': 67, 'iowa': 68, 'ireland': 69, 'israel': 70, 'italy': 71, 'japan': 72, 'kamkar': 73, 'komdsecko': 74, 'korea': 75, 'koum': 76, 'krypton magnet': 77, 'kurdistan': 78, 'las vegas': 79, 'las vegas anton': 80, 'las vegas week': 81, 'las vegas year': 82, 'lithuania': 83, 'london': 84, 'los angeles': 85, 'luba': 86, 'magiclick': 87, 'malaysia': 88, 'marc': 89, 'markey': 90, 'massachusetts': 91, 'mcnamara': 92, 'mexico': 93, 'mhtml': 94, 'miami beach': 95, 'michigan': 96, 'minnesota': 97, 'moscow': 98, 'ms11': 99, 'nebraska': 100, 'networksthe united states federal bureau': 101, 'new york': 102, 'new york city': 103, 'new york times': 104, 'new zealand': 105, 'nigeria': 106, 'north africa': 107, 'north korea': 108, 'northeastern united states': 109, 'o3xzf': 110, 'oakland': 111, 'ohio': 112, 'orlando': 113, 'pakistani city lahore': 114, 'palo alto': 115, 'panama': 116, 'paris': 117, 'patch united states': 118, 'pennsylvania': 119, 'people united states': 120, 'poland': 121, 'princeton': 122, 'prntqdl64': 123, 'processthe united states federal bureau': 124, 'regina': 125, 'risksthe united kingdom': 126, 'russia': 127, 's6': 128, 'samsung knox': 129, 'samsung sony': 130, 'san bernardino': 131, 'san diego': 132, 'san francisco': 133, 'saudi arabia': 134, 'seattle': 135, 'singapore': 136, 'somalia': 137, 'south africa': 138, 'south carolina': 139, 'south korea': 140, 'spain': 141, 'st louis county': 142, 'st louis moerlein': 143, 'st louis public library week': 144, 'statesthe united states federal reserve': 145, 'switzerland germany': 146, 'sydney': 147, 'syria': 148, 'sysadmin': 149, 'taiwan': 150, 'targetsin': 151, 'texas': 152, 'thailand': 153, 'tibet': 154, 'tls_fallback_scsv': 155, 'tokyo': 156, 'toronto': 157, 'turkey': 158, 'uk': 159, 'uk germany': 160, 'united arab emirates': 161, 'united kingdom': 162, 'united kingdom united states': 163, 'united states': 164, 'united states canada': 165, 'united states debix inc': 166, 'united states department': 167, 'university york': 168, 'univia': 169, 'utah': 170, 'v6': 171, 'vaccineinterpol united states': 172, 'vietnam': 173, 'vulnerabilitiesthe united states federal bureau': 174, 'washington': 175, 'webl': 176, 'wild united states': 177, 'windowsdir': 178, 'withcan': 179, 'xpdcqbs3g2': 180, 'xrp': 181, 'xvmbc': 182, 'yearthe united states federal bureau': 183, 'zoophilia': 184, 'zwienenberg': 185}
    organization_dict = {"GOVERNMENT SECTOR FOR PUBLIC JUSTICE": 0, 'AIR AND SPACE': 1, 'BANKING': 2, 'CAMERA': 3, 'CYBERSECURITY SECTOR': 4, 'E-COMMERCE': 5, 'EDUCATIONAL INSTITUTE': 6, 'FINANCE': 7, 'FINANCIAL SERVICE PROVIDER': 8, 'GOVT': 9, 'HARDWARE MANUFACTURER': 10, 'HEALTH': 11, 'IT COMPANY': 12, 'LAPTOP': 13, 'MARKETING': 14, 'MEDIA': 15, 'MOBILE COMPANY': 16, 'NEWS': 17, 'OPTICAL RETAILING COMPANY': 18, 'POLICE & ARM FORCES': 19, 'POLITICAL': 20, 'STOCK EXCHANGE': 21, 'TAX AGENCY': 22, 'TRANSPORTATION': 23, 'VEHICLE': 24}
    attacks_dict = {'Web Attacks': 0, 'Brute Force': 1, 'DNS SPOOFING': 2, 'Daniel of Service Attack': 3, 'Drive By Attack': 4, 'Insider Threat': 5, 'Malware Attacks': 6, 'Man In the Middle Attack': 7, 'Online Fraud': 8, 'Password Attacks': 9, 'Phishing Attack': 10, 'Ransomware Attacks': 11, 'SQL Injection': 12, 'Session Hijacking': 13, 'Spear Phishing Attacks': 14, 'Trojan Attacks': 15, 'URL Interpretation': 16}
    public_private_dict = {"Public": 0, 'Private': 1, 'Public Sector': 2}

    print("Data = ", request.form.get('location'), request.form.get('sector'), request.form.get('PP'))

    location = location_dict[request.form.get('location')]
    sector = organization_dict[request.form.get('sector')]
    public_private = public_private_dict[request.form.get('PP')]

    print("Data = ", location, sector, public_private)

    model = pickle.load(open('model', 'rb'))

    pridicted_value = get_key(attacks_dict, round(model.predict(np.array([[location, sector, public_private]]))[0]))

    print("Prediction = ", pridicted_value)

    return 0

def get_key(my_dict, val):
    for key, value in my_dict.items():
         if val == value:
             return key

if __name__ =="__main__":
    app.run(debug=True)
