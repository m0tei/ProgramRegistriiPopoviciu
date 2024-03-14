from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo
import os

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

MONGO_DB_HOST = os.getenv("MONGO_DB_HOST", "localhost")
MONGO_DB_PORT = int(os.getenv("MONGO_DB_PORT", 27017))

client = pymongo.MongoClient(MONGO_DB_HOST,MONGO_DB_PORT)
db = client.databasePopoviciu
# Database

# Verify connection with MongoDB
#if db.list_collection_names():
#  print("Connected to MongoDB server: " + str(MONGO_DB_HOST) + ":" + str(MONGO_DB_PORT))
#else:
#  print("Failed to connect to MongoDB server. Check your host and port.")

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# Routes
from user import routes

@app.route('/')
def home(): 
  return render_template('home.html')

@app.route('/admin/dashboard/')
@login_required
def admin_dashboard():
    if not session.get("role") == "admin":
        return redirect("/")
    return render_template('admin-dashboard.html')

@app.route('/user/dashboard/')
@login_required
def user_dashboard():
    if not session.get("role") == "user":
        return redirect("/")
    return render_template('user-dashboard.html')
