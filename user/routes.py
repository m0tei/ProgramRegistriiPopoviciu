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

@app.route('/entry/delete/<id>', methods=['DELETE'])
def deleteEntry(id):
  return Entry().delete(id)

@app.route('/table/download/', methods=['GET'])
def verifyDownload():
  return Table().verifyDownload()

@app.route('/table/download/<year>', methods=['GET'])
def downloadExcel(year):
  return Table().download(year)

@app.route('/table/show/', methods=['GET'])
def getData():
  return Table().showTable()

@app.route('/table/collections', methods=['GET'])
def collectionList():
  return Table().collectionList()

@app.route('/table/last_element', methods = ['GET'])
def last_element():
  return Table().last_element()