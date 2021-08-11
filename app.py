from flask import Flask, render_template,request,json, redirect, url_for
import pymysql.cursors,os
import numpy as np
# import smtplib
# import jinja2
#sudo /etc/init.d/apache2 stop  command to stop apache
 
#current job: To add/delete requested movies with admin in admin_action function
#Error in select seats page (costumer)
#Error in theatre owner page delete movies


PEOPLE_FOLDER = os.path.join('static', 'movie_imgs')

 
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='beatcovid',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

# app.jinja_env.filters['zip'] = zip				#used for using zip function in jinja
# env = jinja2.Environment()
# app.jinja_env.globals.update(zip=zip)

@app.route("/signup")
def signup():
	return render_template('signup.html')

@app.route('/signedin',methods=['POST', 'GET'])
def signUp():
	if request.method=='POST':
		name=request.form['name']
		username=request.form['username']
		password=request.form['password']
		user=request.form['user']
		email=request.form['email']
		with connection.cursor() as cursor:
			if user=='Customer':
				sql = "INSERT INTO AllUsers (Name,username,password,Email) VALUES (%s, %s,%s,%s)"
				cursor.execute(sql, (name,username,password,email))
				connection.commit()
				return render_template('signedup.html')
			elif user=='Theatre Owner':
				sql = "INSERT INTO Theatre_Owners (Name,username,password,Email) VALUES (%s, %s,%s,%s)"
				cursor.execute(sql, (name,username,password,email))
				connection.commit()
				return redirect(url_for('theatredetails', username=username))
			elif user=='Admin':
				sql = "INSERT INTO Admins (Name,username,password,Email) VALUES (%s, %s,%s,%s)"
				cursor.execute(sql, (name,username,password,email))
				connection.commit()
				return render_template('signedup.html')

@app.route("/theatredetails/<username>")
def theatredetails(username):
	return render_template('theatredetails.html',username=username)
       
@app.route("/theatredetails/<username>/input",methods=['POST', 'GET'])
def input(username):
	if request.method=='POST':
		with connection.cursor() as cursor:
			theatre_name=request.form['name']
			address=request.form['address']
			sql='UPDATE Theatre_Owners SET Theatre_Name=%s WHERE username=%s'
			cursor.execute(sql,(theatre_name,username))
			connection.commit()
			sql2='INSERT INTO Theatres (Name,Owner,Address) VALUES (%s,%s,%s)'
			cursor.execute(sql2,(theatre_name,username,address))
			connection.commit()
			return render_template('signedup.html')


@app.route("/login")
def login():
	return render_template('login.html')

@app.route('/loggingin',methods=['POST', 'GET'])
def loggingin():
	flag1=True
	flag2=True
	if request.method=='POST':
		usern=request.form['username']
		passwo=request.form['password']
		tou=request.form['user']
		try:
			with connection.cursor() as cursor:
				if tou=='Customer':
					sql1 = "SELECT * from AllUsers WHERE username=%s"
					sql2 = "SELECT * from AllUsers WHERE password=%s"
				elif tou=='Theatre Owner':
					sql1 = "SELECT * from Theatre_Owners WHERE username=%s"
					sql2 = "SELECT * from Theatre_Owners WHERE password=%s"
				elif tou=='Admin':
					sql1 = "SELECT * from Admins WHERE username=%s"
					sql2 = "SELECT * from Admins WHERE password=%s"
				cursor.execute(sql1,(usern,))
				user = cursor.fetchall()
				cursor.execute(sql2,(passwo,))
				passw = cursor.fetchall()
				if not user:
					flag1=False
				if not passw:
					flag2=False
				if flag1==True and flag2==True:
					if tou=='Customer':
						return redirect(url_for('loggedin', name=usern))
					elif tou=='Theatre Owner':
						return redirect(url_for('loggedin_to', name=usern))
					elif tou=='Admin':
						return redirect(url_for('loggedin_ad', name=usern))
				else:
					return "Wrong username, password or designation"
		except:
			connection.close()

@app.route('/admin/<name>',methods=['POST','GET'])
def loggedin_ad(name):
	with connection.cursor() as cursor:
		sql='SELECT username FROM Admins WHERE username=%s'
		cursor.execute(sql,name)
		usern=cursor.fetchall()
		sql1='SELECT Name,URL,Theatre_ID,Request_type FROM Requested_Movies'
		cursor.execute(sql1)
		requests=cursor.fetchall()
		add_req=[]
		del_req=[]
		for request in requests:
			th_id=request['Theatre_ID']
			sql2='SELECT Name FROM Theatres WHERE ID=%s'
			cursor.execute(sql2,th_id)
			theatre_name=cursor.fetchall()
			request['Theatre_Name']=theatre_name[0]['Name']
			if request['Request_type']=='add':
				add_req.append(request)
			elif request['Request_type']=='delete':
				del_req.append(request)
		return render_template("adminstart.html",usern=name, add_req=add_req, add_size=len(add_req), del_req=del_req, del_size=len(del_req))

# @app.route('/admin/<name>/action',methods=['POST','GET'])
# def admin_action(name):
# 	if request.method=='POST':
# 		with connection.cursor() as cursor:
# 			if request.form['submit_button']=='Add Movies':
# 				selected_movies = request.form.getlist('add')
# 				to_add=[]
# 				for string in selected_movies:
# 					temp=string.split()
# 					if len(temp)>3:
# 						movie_name=''
# 						temp_new=[]
# 						for i in range(0,len(temp)-2):
# 							movie_name=movie_name+temp[i]+" "
# 						temp_new.append(movie_name)
# 						for i in range(len(temp)-2,len(temp)):
# 							temp_new.append(temp[i])
# 						to_add.append(temp_new)
# 					else:
# 						to_add.append(temp)
# 				print(to_add)
# 				for movie in to_add:
# 					sql='SELECT ID,Theatre_ID from Requested_Movies WHERE Name=%s AND URL=%s AND Theatre_ID=%s'
# 					cursor.execute(sql,(movie[0],movie[1],movie[2]))
# 					mov_the=cursor.fetchall()
# 					sql1='SELECT * FROM Requested_times WHERE Movie_ID=%s AND Theatre_ID=%s'
# 					cursor.execute(sql1,(mov_the[0]['ID'],mov_the[0]['Theatre_ID']))
# 					times=cursor.fetchall()
# 					sql='DELETE FROM Requested_times WHERE Movie_ID=%s AND Theatre_ID=%s'
# 					cursor.execute(sql,(mov_the[0]['ID'],mov_the[0]['Theatre_ID']))
# 					connection.commit()
# 					for time in times:
# 						sql2='INSERT INTO MovieTheatresTimes(Movie_ID,Theatre_ID,MovTime) VALUES (%s,%s,%s)'
# 						cursor.execute(sql2,(time['Movie_ID'],time['Theatre_ID'],time['MovTime']))
# 						connection.commit()
# 					sql3='SELECT * FROM Movies WHERE Name=%s'
# 					cursor.execute(sql3,(movie[0]))
# 					check=cursor.fetchall()
# 					if not check:
# 						sql='SELECT * from Requested_Movies WHERE Name=%s AND URL=%s AND Theatre_ID=%s'
# 						cursor.execute(sql,(movie[0],movie[1],movie[2]))
# 						mov=cursor.fetchall()
# 						sql2='INSERT INTO Movies(ID,Name, Description, Cast, Rating,Language,Image_location,URL) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
# 						cursor.execute(sql2,(mov[0]['ID'],mov[0]['Name'],mov[0]['Description'],mov[0]['Cast'],mov[0]['Rating'],mov[0]['Language'],mov[0]['Image_location'],mov[0]['Name'].replace(" ","")))
# 						connection.commit()
# 					sql3='DELETE FROM Requested_Movies WHERE Name=%s AND URL=%s AND Theatre_ID=%s'
# 					cursor.execute(sql3,(movie[0],movie[1],movie[2]))
# 					connection.commit()
# 				return "Success"
# 			if request.form['submit_button']=='Delete Movies':
# 				selected_movies = request.form.getlist('del')
# 				to_del=[]
# 				for string in selected_movies:
# 					temp=string.split()
# 					if len(temp)>3:
# 						movie_name=''
# 						temp_new=[]
# 						for i in range(0,len(temp)-2):
# 							movie_name=movie_name+temp[i]+" "
# 						temp_new.append(movie_name)
# 						for i in range(len(temp)-2,len(temp)):
# 							temp_new.append(temp[i])
# 						to_del.append(temp_new)
# 					else:
# 						to_del.append(temp)
# 					print("aaaaaaaaaaaa")
# 					print(to_del)
# 				for movie in to_del:
# 					sql='SELECT ID FROM Requested_Movies WHERE Name=%s AND URL=%s AND Theatre_ID=%s'
# 					cursor.execute(sql,(movie[0].strip(),movie[1],movie[2]))
# 					mov_the=cursor.fetchall()
# 					print(mov_the)
# 					sql='DELETE FROM Requested_Movies WHERE Name=%s AND URL=%s AND Theatre_ID=%s'
# 					cursor.execute(sql,(movie[0].strip(),movie[1],movie[2]))
# 					connection.commit()
# 					print("aaaaaaaaaaaa")
# 					sql1='DELETE FROM MovieTheatresTimes WHERE Movie_ID=%s AND Theatre_ID=%s'
# 					cursor.execute(sql1,(mov_the[0]['ID'],movie[2]))
# 					connection.commit()
# 					print("aaaaaaaaaaaa")
# 					sql2='SELECT * FROM MovieTheatresTimes WHERE Movie_ID=%s'
# 					cursor.execute(sql2,(mov_the[0]['ID']))
# 					check=cursor.fetchall()
# 					print("aaaaaaaaaaaa")
# 					if not check:
# 						sql3='DELETE FROM Movies WHERE Name=%s'
# 						cursor.execute(sql3,(movie[0].strip()))
# 						connection.commit()
# 						print("aaaaaaaaaaaa")
# 				return "Success"

# @app.route('/theatre_owner/<name>', methods=['POST','GET'])
# def loggedin_to(name):
# 	with connection.cursor() as cursor:
# 		sql='SELECT Name FROM Theatres where Owner=%s'
# 		cursor.execute(sql,(name))
# 		theatre_name=cursor.fetchall()
# 		sql1='SELECT Name FROM Movies'
# 		cursor.execute(sql1)
# 		movies=cursor.fetchall()
# 		sql2='SELECT Name FROM Requested_Movies WHERE Request_type=%s'
# 		cursor.execute(sql2,('delete'))
# 		delete=cursor.fetchall()
# 		if delete:
# 			for i in delete[:]:
# 				if i in movies:
# 					movies.remove(i)
# 		return render_template("theatre_owner_start.html",name=name,theatre_name=theatre_name,movies=movies)

# @app.route('/theatre_owner/<name>/request',methods=['POST', 'GET'])
# def requesting(name):
# 	if request.method=='POST':
# 		with connection.cursor() as cursor:
# 			if request.form['submit_button'] == 'Add Movie Timings':
# 				mov_name=request.form['name']
# 				desc=request.form['description']
# 				cast=request.form['cast']
# 				rat=request.form['rating']
# 				lang=request.form['language']
# 				loc=request.form['location']
# 				nos=request.form['nos']
# 				url=name.replace(" ", "")
# 				mov_name_no_spaces=mov_name.replace(" ","")
# 				mov_id=mov_name_no_spaces[0]+mov_name_no_spaces[1]+mov_name_no_spaces[int(len(mov_name_no_spaces)/2)]+mov_name_no_spaces[len(mov_name_no_spaces)-2]+mov_name_no_spaces[len(mov_name_no_spaces)-1]
# 				sql1='SELECT ID FROM Theatres WHERE Owner=%s'
# 				cursor.execute(sql1,(name))
# 				th_id=cursor.fetchall()
# 				sql2='INSERT INTO Requested_Movies (ID,Name,Description,Cast,Rating,Language,Image_location,URL,Theatre_ID,Request_type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
# 				cursor.execute(sql2,(mov_id,mov_name,desc,cast,rat,lang,loc,url,th_id[0]['ID'],'add'))
# 				connection.commit()
# 				return render_template('timings.html',nos=int(nos),mov_name=mov_name,name=name)
# 			if request.form['submit_button'] == 'Submit Delete Request':	
# 				mov_name=request.form['movies']
# 				sql1='SELECT ID FROM Movies WHERE Name=%s'
# 				cursor.execute(sql1,(mov_name))
# 				mov_id=cursor.fetchall()
# 				sql1='SELECT ID FROM Theatres WHERE Owner=%s'
# 				cursor.execute(sql1,(name))
# 				th_id=cursor.fetchall()
# 				sql='INSERT INTO Requested_Movies (ID,Name,URL,Theatre_ID,Request_type) VALUES (%s,%s,%s,%s,%s)'
# 				cursor.execute(sql,(mov_id[0]['ID'],mov_name,name,th_id[0]['ID'],'delete'))
# 				connection.commit()
# 				return render_template("submitted.html",name=name)


# @app.route('/theatre_owner/<name>/<mov_name>/<nos>',methods=['POST','GET'])
# def submitted(name,mov_name,nos):
# 	if request.method=='POST':
# 		times=[]
# 		for i in range(int(nos)):
# 			times.append(request.form[str(i)])
# 		with connection.cursor() as cursor:
# 			sql1='SELECT ID FROM Theatres WHERE Owner=%s'
# 			cursor.execute(sql1,(name))
# 			th_id=cursor.fetchall()
# 			sql2='SELECT ID FROM Requested_Movies WHERE Name=%s AND Theatre_ID=%s AND Request_type=%s'
# 			cursor.execute(sql2,(mov_name,th_id[0]['ID'],'add'))
# 			mov_id=cursor.fetchall()
# 			for i in range(int(nos)):
# 				sql3='INSERT INTO Requested_times (Movie_ID,Theatre_ID,MovTime) VALUES (%s,%s,%s)'
# 				cursor.execute(sql3,(mov_id[0]['ID'],th_id[0]['ID'],times[i]))
# 				connection.commit()				
# 			return render_template("submitted.html",name=name)



# @app.route('/<name>')
# def loggedin(name):
# 	full_filename=[]
# 	with connection.cursor() as cursor:
# 		sql='SELECT Name, Image_location, URL FROM Movies'
# 		cursor.execute(sql)
# 		info=cursor.fetchall()
# 		for movie in info:
# 			full_filename.append(os.path.join(app.config['UPLOAD_FOLDER'], movie['Image_location']))
# 		return render_template("MovieList.html",name=name, full_filename=full_filename,info=info,size=len(info))

# @app.route('/<name>/searchresult',methods=['POST', 'GET'])
# def searching(name):
# 	if request.method=='POST':
# 		lang=request.form['searchbar']
# 		# try:
# 		with connection.cursor() as cursor:
# 			sql = "SELECT * from Movies WHERE Language=%s"
# 			cursor.execute(sql,(lang,))
# 			lang_mov=cursor.fetchall()
# 			sql = "SELECT Image_Location from Movies WHERE Language=%s"
# 			cursor.execute(sql,(lang,))
# 			loc=cursor.fetchall()
# 			file_name=[]
# 			full_filename=[]
# 			for i in loc:
# 				file_name.append(i['Image_Location'])
# 			for i in file_name:
# 				full_filename.append(os.path.join(app.config['UPLOAD_FOLDER'], i))
# 			l=len(lang_mov)
# 			if not lang_mov:
# 				return "No %s movies this week" % lang
# 			if lang_mov:
# 				return render_template("search.html",lang_mov=lang_mov,lang=lang, full_filename=full_filename,l=l,name=name)

# @app.route('/<name>/movie/<mov_name>')
# def movie(name,mov_name):
# 	with connection.cursor() as cursor:
# 		sql = "SELECT * from Movies WHERE URL=%s"
# 		cursor.execute(sql,(mov_name,))
# 		movie_info=cursor.fetchall()
# 		rating=str(movie_info[0]['Rating'])
# 		full_filename = os.path.join(app.config['UPLOAD_FOLDER'], movie_info[0]['Image_location'])
# 		sql = "SELECT * from MovieTheatresTimes WHERE Movie_ID=%s"
# 		cursor.execute(sql,(movie_info[0]['ID'],))
# 		time=cursor.fetchall()
# 		time_dup=time.copy()
# 		theatres=[]
# 		for i in range(0,len(time_dup)):
# 			num=time_dup[i]['Theatre_ID']
# 			if num!=0:
# 				theatres.append(num)
# 			for j in range(0,len(time_dup)):
# 				if time_dup[j]['Theatre_ID']==num:
# 					time_dup[j]['Theatre_ID']=0
# 		sql = "SELECT * from MovieTheatresTimes WHERE Movie_ID=%s"
# 		cursor.execute(sql,(movie_info[0]['ID'],))
# 		time=cursor.fetchall()
# 		print(theatres)
# 		theatre_names=[]
# 		final=[]
# 		lengths=[]
# 		for i in range(0,len(theatres)):
# 			sql = "SELECT Name from Theatres WHERE ID=%s"
# 			cursor.execute(sql,(theatres[i],))
# 			temp=cursor.fetchall()
# 			theatre_names.append(temp[0]['Name'])
# 			times=[]
# 			for j in range(0,len(time)):
# 				if theatres[i]==time[j]['Theatre_ID']:
# 					times.append(time[j]['MovTime'])
# 			print(times)
# 			final.append(times)
# 		for i in range(0,len(final)):
# 			lengths.append(len(final[i]))
# 		l=len(theatre_names)
# 		print(final)
# 		return render_template('movie.html',full_filename=full_filename,movie_info=movie_info,rating=rating,theatre_names=theatre_names,final=final,l=l,lengths=lengths,theatres=theatres,name=name)

# @app.route('/<name>/movie/<mov_name>/<Theatre_ID>/<time>')
# def time(name,mov_name,Theatre_ID,time):
# 	with connection.cursor() as cursor:
# 		sql1 = "SELECT ID from Movies WHERE URL=%s"
# 		cursor.execute(sql1,(mov_name,))
# 		mov_id=cursor.fetchall()
# 		print(type(mov_id))
# 		print(mov_id)
# 		sql = "	SELECT SLNO FROM MovieTheatresTimes WHERE Movie_ID=%s AND Theatre_ID=%s AND MovTime=%s"
# 		cursor.execute(sql,(mov_id[0]['ID'],Theatre_ID,time,))
# 		slno=cursor.fetchall()
# 		seats = np.load('seats_%s.npy' % slno[0]['SLNO']) 
# 	return render_template('seatbooking.html',seats=seats,mov_name=mov_name,Theatre_ID=Theatre_ID,time=time,name=name)

# @app.route('/<name>/movie/<mov_name>/<Theatre_ID>/<time>/booked',methods=['POST', 'GET'])
# def booked(name,mov_name,Theatre_ID,time):
# 	if request.method=='POST':
# 		selected_seats = request.form.getlist('seatmatrix')
# 		with connection.cursor() as cursor:
# 			sql1 = "SELECT ID from Movies WHERE URL=%s"
# 			cursor.execute(sql1,(mov_name,))
# 			mov_id=cursor.fetchall()
# 			print(type(mov_id))
# 			print(mov_id)
# 			sql = "	SELECT SLNO FROM MovieTheatresTimes WHERE Movie_ID=%s AND Theatre_ID=%s AND MovTime=%s"
# 			cursor.execute(sql,(mov_id[0]['ID'],Theatre_ID,time,))
# 			slno=cursor.fetchall()
# 			seats = np.load('seats_%s.npy' % slno[0]['SLNO']) 
# 			i=0 
# 			for dictionary in seats:
# 				for j in selected_seats:
# 					if j in dictionary:
# 						seats[i][j] = 1
# 				i=i+1  
# 			print(seats)
# 			sql2="SELECT * FROM AllUsers WHERE username=%s"
# 			cursor.execute(sql2,(name,))
# 			info=cursor.fetchall()
# 			np.save('seats_%s' % slno[0]['SLNO'],seats)
# 			s = smtplib.SMTP('smtp.gmail.com', 587)
# 			s.starttls()
# 			s.login("gaumo62@gmail.com", "iamtheflash")
# 			message = "Thank you for booking. Your seat numbers are "
# 			message.join(selected_seats)
# 			s.sendmail("gaumo62@gmail.com","%s" % info[0][Email], message)
# 			s.quit()
# 			return "Success Email ID is %s" % info[0]['Email']

# @app.route('/<username>/edit_profile')
# def edit_profile(username):
# 	with connection.cursor() as cursor:
# 		sql = "SELECT * FROM AllUsers WHERE username=%s"
# 		cursor.execute(sql,(username,))
# 		info=cursor.fetchall() 
# 		return render_template('edit.html',info=info)

# @app.route('/<username_old>/edited',methods=['POST', 'GET'])
# def edited(username_old):
# 	if request.method=='POST':
# 		name=request.form['name']
# 		username=request.form['username']
# 		password=request.form['password']
# 		user=request.form['user']
# 		email=request.form['email']
# 		with connection.cursor() as cursor:
# 			sql = "UPDATE AllUsers SET Name=%s, username=%s, password=%s, Type=%s, Email=%s WHERE username=%s"
# 			cursor.execute(sql, (name,username,password,user,email,username_old))
# 			connection.commit()
# 			return render_template('edited.html')


if __name__ == "__main__":
	app.run(debug=True)