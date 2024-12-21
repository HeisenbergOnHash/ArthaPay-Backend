import requests,re,logging
from http import HTTPStatus

def ruaanyafintech(payload, token):
  url = "https://api.ruaanyafintech.com/api/ruyaan/icici/payout"

  data = {
          "token"     :   token,
          "apitxnid"  :   payload.get("transaction_id"),
          "amount"    :   payload.get("amount"),
          "name"      :   payload.get("beneficiary_name"),
          "account"   :   payload.get("bank_account"),
          "ifsc": re.sub(r'[a-z]', lambda match: match.group(0).upper(), payload.get("ifsc")),
          "mode"      :   "IMPS"
          }

  try:
    response = requests.post(url, json=data)
    logging.info(f"Response status code: {response.status_code}, Response content: {response.text}")

    if response.status_code == HTTPStatus.OK:return response.json(), HTTPStatus.OK
    else:return response.json(), response.status_code

  except requests.exceptions.RequestException as e:
    logging.error(f"An error occurred during the request: {e}")
    return {"status": "Error occurred during the request to service provider" }, HTTPStatus.INTERNAL_SERVER_ERROR