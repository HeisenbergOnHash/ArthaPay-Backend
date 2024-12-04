import random,json,bcrypt, logging
from http import HTTPStatus
from app.utils.Database.queries import *
from app.utils.Database.connection import MySQLDatabase
# from app.services.neobiz import neobiz_payments

class backend:
  def fetch_admin(data):
    results = MySQLDatabase.fetch_results(fetch_admin_query, (data,))
    if results.get('data'):
      return results.get('data', [{}])[0], (results.get('status') if isinstance(results.get('status'), list) else [results.get('status', HTTPStatus.INTERNAL_SERVER_ERROR)])[0]
    else:return {"Message": "User Not Found"},  HTTPStatus.NOT_FOUND

  def fetch_user(data):
    results = MySQLDatabase.fetch_results(fetch_user_query, (data,))
    if results.get('data'):
      return results.get('data', [{}])[0], (results.get('status') if isinstance(results.get('status'), list) else [results.get('status', HTTPStatus.INTERNAL_SERVER_ERROR)])[0]
    else:return {"Message": "User Not Found"},  HTTPStatus.NOT_FOUND

  def authenticate(username, password, role):
      query = authenticate_admin_query if role == "admin" else authenticate_user_query
      results = MySQLDatabase.fetch_results(query, (username,))
      if results.get('data') and bcrypt.checkpw(password.encode('utf-8'), results['data'][0]['password'].encode('utf-8')):
          return {"successMsg": "User authenticated successfully"}, HTTPStatus.OK
      return {"errorMsg": "Invalid password"}, HTTPStatus.UNAUTHORIZED

  def fetch_wallet_balance(data):
    results = MySQLDatabase.fetch_results(fetch_user_balance, (data,))
    if results.get('data'):
      return results.get('data', [{}])[0], (results.get('status') if isinstance(results.get('status'), list) else [results.get('status', HTTPStatus.INTERNAL_SERVER_ERROR)])[0]
    else:return {"errorMsg": "Data Not Found"}, HTTPStatus.NOT_FOUND

  def transaction_authorizer(data):
    results = MySQLDatabase.fetch_results(transaction_authorizer_query, (data.get('username'),))
    if results.get("data"):
      if results['data'][0]['kyc_status'] != "Verified":return False,"Transaction Rights are On Hold"
      if int(results['data'][0]['t_pin']) != int(data.get('t_pin')):return False,"Incorrect Transaction Pin"
      else:return True, "Authorized"
    else:return False, "Error Fetching the Data to Authorize Transaction"

  def Do_Transaction(data):
    status, story = backend.transaction_authorizer(data)
    if not status:return story, HTTPStatus.OK
