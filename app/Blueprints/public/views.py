from http import HTTPStatus
from . import public_blueprint 
from flask import jsonify,session,request
from app.utils.services.get_info import get_system_details
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, set_access_cookies,unset_jwt_cookies

@public_blueprint.route('/', methods=['GET'])
def public_info():
    return jsonify(message="Public Information version 1.0 from LenDenPay", data = get_system_details()), 200

@public_blueprint.route('/tokenRefresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    response = jsonify({"msg": "Token refreshed"})
    set_access_cookies(response, new_access_token)
    return response , 200


@public_blueprint.route('/CallBack', methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        received_data = request.args.to_dict()
        print(f"Received GET data: {received_data}")
        return jsonify(message="Callback received via GET", data=received_data), 200

    elif request.method == 'POST':
        try:
            received_data = request.json 
            if not received_data:
                return jsonify(message="No data received in POST request"), 400

            print(f"Received POST data: {received_data}")
            return jsonify(message="Callback received via POST", data=received_data), 200

        except Exception as e:
            print(f"Error processing POST data: {e}")
            return jsonify(message="Error processing POST request", error=str(e)), 500
