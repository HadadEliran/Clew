from django.http import HttpRequest, HttpResponse
from .models import MedicationPeriodEvent
from .entities import Action
from .period_calculator import PeriodCalculator

def get_periods(request: HttpRequest)-> HttpResponse:

    # Validate that patient id and medication name has been provided
    if request.GET.get("patient_id") is None:
        return HttpResponse("Not provided patient id", status=400)
    if request.GET.get("medication_name") is None:
        return HttpResponse("Not provided medication name", status=400)

    actions = __get_actions(request.GET["patient_id"], request.GET["medication_name"])

    periods = PeriodCalculator().calculate(actions)
    jsons = [period.as_dict() for period in periods]

    return HttpResponse(f"{str(jsons)}")

def __get_actions(patient_id_val, medication_name_val):
    # Load all events of this patient with the medication and order then according "activation date".
    # We will extract only the "action type" and "activation date"
    actions_as_rows = MedicationPeriodEvent.objects.filter(patient_id=patient_id_val,
                                                           medication_name=medication_name_val)\
                                                   .order_by("action_activation_date")\
                                                   .values("action_type", "action_activation_date")
    actions = []
    
    for row in actions_as_rows:
        actions.append(Action(row["action_type"], row["action_activation_date"]))
    return actions

def get_events(request: HttpRequest)-> HttpResponse:
    # from consumer.consumer_app.models import MedicationPeriodEvent
    results = MedicationPeriodEvent.objects.filter(patient_id=request.GET["patient_id"],
                                                   medication_name=request.GET["medication_name"])\
                                           .order_by("action_activation_date")\
                                           .values("action_type", "action_activation_date")
    results = list(results)
    return HttpResponse(f"{results}")
    

def add_event(request: HttpRequest)-> HttpResponse:
    """
        This function adds an event with the details from a HTTP request. 
        The request should contain these fields:
        - "action_type" - "START", "STOP", "CANCEL_START", "CANCEL_STOP".
        - "patient_id" 
        - "medication_name".

        The "activation date" will be generated randomally.
    """

    import random
    import datetime

    # Generate random month and day in month
    month = random.choice(range(1,13))
    day = random.choice(range(1,31))

    event:MedicationPeriodEvent = MedicationPeriodEvent.objects.create(
                                                 action_type=request.POST["action_type"],
                                                 patient_id=request.POST["patient_id"], 
                                                 medication_name=request.POST["medication_name"],
                                                 action_activation_date=datetime.date(2021, month, day))

    # Save the event in the db.                                
    event.save()
    
    return HttpResponse("Event has been created!")