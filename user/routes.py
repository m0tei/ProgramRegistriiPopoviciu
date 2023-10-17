from flask import Flask
from app import app
from user.models import User, Entry, Table

@app.route('/user/signup', methods=['POST'])
def signup():
  return User().signup()

@app.route('/user/signout')
def signout():
  return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
  return User().login()

@app.route('/entry/add', methods=['POST'])
def addEntry():
  return Entry().add()

@app.route('/table/download/<year>', methods=['GET'])
def downloadExcel(year):
  return Table().download(year)