from http import HTTPStatus
import random,json,bcrypt, logging
from app.utils.Database.queries import *
from app.utils.services.ruaanya import ruaanyafintech
from app.utils.Database.connection import MySQLDatabase


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
      if results['data'][0]['kyc_status'] != "Verified":return False, {"message": "Transaction Rights are On Hold"}
      if int(results['data'][0]['t_pin']) != int(data.get('t_pin')):return False,{"message": "Incorrect Transaction Pin"}
      else:return True, {"message":"Authorized"}
    else:return False, {"message":"Error Fetching the Data to Authorize Transaction"}

  def insert_transaction_request(data):
    required_fields = ['username', 'beneficiary_name', 'bank_account', 'ifsc', 'amount', 'transfer_id','status']
    data['status'] = 'processing';missing_fields = [field for field in required_fields if data.get(field) is None]
    if missing_fields:return False, {"message": f"Missing Fields: {', '.join(missing_fields)}, Transaction Aborted"}
    data_tuple = tuple(data[field] for field in required_fields)
    results = MySQLDatabase.execute_query(insert_transaction_request_query, data_tuple)
    if results.get('status') == HTTPStatus.OK:return True, {"message": "Transaction request inserted"}
    else:return False, {"message": "Failed to insert transaction request"}
  
  def Do_Transaction(data):
    status, story = backend.transaction_authorizer(data)
    if not status:return story, HTTPStatus.OK
    status, story = backend.insert_transaction_request(data)
    if not status:return story, HTTPStatus.OK
    response, code = ruaanyafintech(data, "xwczDWHTZukLxOKPIxshFyuQuV4nPX")
    return response, code