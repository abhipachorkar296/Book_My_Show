from flask import Flask, render_template,request,json , redirect , url_for
import pymysql.cursors,os
import numpy as ny
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask_table import Table, Col

UPLOAD_FOLDER = os.path.join('static','images')
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password= '',
                             db='Bookmyshow',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)

@app.route('/',methods=['POST', 'GET'])
def loginup():
    return render_template('login.html')

# @app.route('/' ,methods=['POST','GET'])
# def home():
#     if request.method == 'POST':
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM ...")
#             data = cursor.fetccd NDhall() 
#     return render_template("home.html" , data = data)


@app.route('/login',methods=['POST', 'GET'])
def login():
    # print("Reachedeee")
    msg = ''
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        category = request.form['category']
        # print
        try:
            with connection.cursor() as cursor:
                if category == 'customer':
                    cursor.execute('SELECT * FROM customer_info WHERE email_id = %s AND password = %s', (email, password))
                    account = cursor.fetchone()

                    if account:
                        print('a')
                        print(account)
                        # session['loggedin'] = True
                        # session['id'] = account['id']
                        # session['email'] = account['email_id']
                        # session['password'] = account['password']
                        # msg = 'Logged successful'
                        print('b')
                        return redirect(url_for('customer' , name = account['email_id']))
                    else:
                        msg = 'Incorrect username/password'
            
                elif category == 'theater_owner':
                    print("Inside")
                    cursor.execute('SELECT * FROM Theater_owners_info WHERE email_id = %s AND password = %s', (email, password))
                    account = cursor.fetchone()

                    if account:
                        print("Fetched")
                        session['loggedin'] = True
                        session['id'] = account['id']
                        session['email'] = account['email_id']
                        msg = 'logged successful'
                        return redirect(url_for(theater))
                    else:
                        msg = 'Incorrect username/password'
                else:
                    print('Admin') 
        except:
            print('error login')
    return render_template('login.html',msg = msg)


@app.route('/signUp',methods=['POST', 'GET'])
def signUp():
    print("ff")
    if request.method=='POST':
        name = request.form['name']
        print(name)
        print(request.form)
        email=request.form['email']
        password=request.form['password']
        category = request.form['category']
        try:
            with connection.cursor() as cursor:
                if category == 'customer':
            
                    print(email,password)
                  # Read a single record
                    sql = "INSERT INTO  customer_info (name,email_id,password) VALUES (%s,%s, %s)"
                   
                    cursor.execute(sql, (name, email,password))
                    connection.commit()
                elif category == 'theater_owner':
                    print(email,password)
                  # Read a single record
                    sql = "INSERT INTO  Theater_owners_info (name,email_id,password) VALUES (%s,%s, %s)"
                   
                    cursor.execute(sql, (name,email,password))
                    connection.commit()
                else:
                    print('admin')
                print("RR")
        except Exception as e:
            print(e)
            return "saved successfully."
        return render_template('login.html')
    return render_template('signupform.html')
       
@app.route('/theater_specification', methods=['POST' , 'GET'])
def theater():
    if request.method=='POST':
        image = request.form['#image']
        address = request.form['Address']
        specifications = request.form['specifications']
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO  theater_speecifications ('''image''' , address , specifications) VALUES(%s,%s,%s)"
                cursor.execute(sql , ('''image''' , address , specifications))
                connection.commit()
        finally:
            connection.close()
            return "saved successfully"
    return render__template('theater_specifications.html')

@app.route('/<name>',methods=['POST','GET'])
def customer(name):
    print(name)
    filename = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT image,movie_name FROM show_list')
        account  = cursor.fetchall()
        os.path.dirname(os.path.abspath(__file__))
        for movie in account:
            filename.append(os.path.join(UPLOAD_FOLDER, movie['image']))
        print(account)
        print(filename)    
    return render_template('MovieList.html', session = account , filename = filename , size = len(account) , name = name)
    # return 'hi'

app.route('/<name>/movie/<movie_name>',methods=['POST','GET']) 
def movie(name,movie_name):
    arr = [0,0,0,0]
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM show_list WHERE movie_name = %s' , (movie_name))
        account = cursor.fetchone()
        if account:
            arr=[account[0]['9:00am'],account[0]['12:00pm'],account[0]['3:00pm'],account[0]['6:00pm']] 
        return render_template('show_list.html' , account = account ,arr = arr)
# @app.route('/<name>/movie/<movie_name>/<time>',methods=['POST'])
# def book(name , movie_name, time):
#     show_list = request.form.getlist('remember')
#     n = len(show_list)



# @app.route('/search-movie',methods = ['POST' , 'GET'] )
# def send_mail():
#     message = Mail(
#         from_email='pranitpawar@gmail.com'
#         to_email=email_id
#         subject=subject
#         html_content='content')
#     try:
#         sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#         response = sg.send(message)
#         #to be continued...
#     except Exception as e:
#         print(e.error)

if __name__ == "__main__":
    app.run(debug=True)

