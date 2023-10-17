from flask import Flask, jsonify, request, session, redirect, send_file, render_template
from passlib.hash import pbkdf2_sha256
from app import db
import pymongo
import uuid
import datetime
import openpyxl

today_date = datetime.date.today()
current_year = str(today_date.year)
this_year_db = getattr(db, current_year, None)

class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signup(self):
    print(request.form)

    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password'),
      "role": request.form.get('admin')
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    if(user["role"]=="on"):
      user["role"]="admin"
    else:
      user["role"]="user"

    # Check for existing email address
    if db.users.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400

    if db.users.insert_one(user):
      return jsonify({ "error": "Account added" }), 200

    return jsonify({ "error": "Signup failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):

    user = db.users.find_one({
      "email": request.form.get('email')
    })

    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
      return self.start_session(user)

    
    
    return jsonify({ "error": "Invalid login credentials" }), 401
  

class Table:
  def download(self,year):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    specific_year = getattr(db, year, None)
    all_documents = specific_year.find()

    if(all_documents):
      return render_template('error.html', year=year)
    
    header = ["ID","Data", "Nr. și data documentului", "De unde provine documentul", "Continut pe scurt", "Compartiment repartzat", "Data expedierii", "Destinatar", "Nr. de inregistrare la care se conex. doc. si indic. dos."]

    sheet.append(header)

    for line in all_documents:
      del line["user"]
      del line["date"]
      line_formated = list(line.values())
      sheet.append(line_formated)
        

    workbook.save(str(datetime.date.today()) + ".xlsx")

    workbook.close()

    file_path = str(datetime.date.today()) +".xlsx"

    return send_file(file_path, as_attachment=True),200

class Entry:
  def add(self):
      # find the last id tag
      last_document = this_year_db.find_one(sort=[("_id", pymongo.DESCENDING)])
      if(last_document):
        last_id = last_document['_id']
      else:
        last_id = 0

      entry = {
        "_id": last_id + 1,
        "user": session['user'],
        "date": str(datetime.date.today()),
        "data_inregistrarii": str(request.form.get('data')),
        "nr_și_data_documentului ": request.form.get('nr_si_data'),
        "de_unde_provine_documentul": request.form.get('provine_doc'),
        "continutul_documentului": request.form.get('cont_scurt'),
        "repartizare": request.form.get('comp_repartizat'),
        "data_expedierii": str(request.form.get('data_expedierii')),
        "destinatar": request.form.get('destinatar'),
        "nr_de_inregistrare_conex_doc_indic_dos.": request.form.get('nr_inregistrare'),
      }

      if(this_year_db.insert_one(entry)):
        return jsonify({ "error": "Entry added" }), 200
      
      return jsonify({ "error": "Entry added failed!" }), 400
