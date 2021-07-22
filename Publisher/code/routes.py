from flask import Blueprint, request
from flask.wrappers import Response

blueprint = Blueprint("routes", "__main__")

@blueprint.route("/start_period", methods=["PUT"])
def start_period():
    data = request.get_json()

    medication = data["medication"]
    patient = data["patient"]
    event_time = data["event_time"]

    print(f"{medication}, {patient}, {event_time}")

    return Response(status=200)

    # Publish the event via the queue  

@blueprint.route("/stop_period", methods=["PUT"])
def stop_period():
    return Response(status=200)

@blueprint.route("/cancel_start_period", methods=["PUT"])
def cancel_start_period():
    return Response(status=200)

@blueprint.route("/cancel_stop_period", methods=["PUT"])
def cancel_stop_period():
    return Response(status=200)