from datetime import datetime
import logging
from flask import Blueprint, request
from flask.wrappers import Response

blueprint = Blueprint("routes", "__main__")

# TODO This logic can be replaced with more advanced technology like "Swagger"
def validate_request()-> Response:
    """
        Validate the request is OK. 
        This means all fields are provided and the "action_activation_date" is in format of "%d-%m-%Y"
    """

    data = request.get_json()

    for field in ["medication_name", "patient_id", "action_activation_date"]:
       if data.get(field) is None:
           return Response(f"'{field}'' has not been provided", status=400)
    
    try:
        datetime.strptime(data["action_activation_date"], "%d-%m-%Y")
        return Response(status=200)
    except:
        return Response(f"Illegal format of 'action_activation_date'", status=400)

@blueprint.route("/start_period", methods=["PUT"])
def start_period():
    response = validate_request()
    
    if response.status == 200:
        data = request.get_json()

        medication = data["medication_name"]
        patient = data["patient_id"]
        event_time = data["action_activation_date"]

        # TODO: Publish the event via the queue  
        logging.info("Publishing the event...")
        response = Response(status=200)


    return response


@blueprint.route("/stop_period", methods=["PUT"])
def stop_period():
    return Response(status=200)

@blueprint.route("/cancel_start_period", methods=["PUT"])
def cancel_start_period():
    return Response(status=200)

@blueprint.route("/cancel_stop_period", methods=["PUT"])
def cancel_stop_period():
    return Response(status=200)