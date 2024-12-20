import requests,re,logging
from http import HTTPStatus

def ruaanyafintech(payload, token):
  url = "https://api.ruaanyafintech.com/api/ruyaan/icici/payout"

  data = {
          "token"     :   token,
          "apitxnid"  :   payload.get("transfer_id"),
          "amount"    :   payload.get("amount"),
          "name"      :   payload.get("beneficiary_name"),
          "account"   :   payload.get("bank_account"),
          "ifsc": re.sub(r'[a-z]', lambda match: match.group(0).upper(), payload.get("ifsc")),
          "mode"      :   "IMPS"
          }

  try:
    response = requests.post(url, json=data)
    
    logging.info(f"Response status code: {response.status_code}")
    logging.info(f"Response content: {response.text}")

    if response.status_code == HTTPStatus.OK:
        logging.info("YO YO Honey Singerr")
        return {"message": "Yo Yo Honey Sing"}, HTTPStatus.OK
    else:
        logging.error(f"Request failed with status code: {response.status_code}")
        return {"message": "Failed to process the request"}, response.status_code

  except requests.exceptions.RequestException as e:
    logging.error(f"An error occurred during the request: {e}")
    return {"message": "Error occurred during the request"}, HTTPStatus.INTERNAL_SERVER_ERROR