This system is responsible to manage "medication periods" for patients.

             ------------------------------   Architecture    ------------------------------
The system consists from 2 application - "publisher" and "consumer".
* publisher *
A Flask application that has 4 endpoints - "start_action", "stop_action", "cancel_start_action" and "cancel_stop_action".
The application gets a HTTP request, converts it to an event and publishes to a RabbitMQ.
The application server listens on port 5000 and runs on a Docker container.

* consumer *
A Django application that has 3 endpoints - "get_periods", "get_events", "add_event".
It runs on a Docker container on port 8000.
The application is connected to a MySQL server that runs on another Docker container.

                    --------------------   Starting the services    -------------------
Run "docker-compose up --build" from the "consumer" and "publisher" directories.

             -------------------------------   Insert events    -------------------------------
The communication between the "publisher" and "consumer" isn't ready. 
Therefore, for inserting events you would use the "add_event" endpoint or execute a sql script against the MySQL server.
The script is under "consumer/develop". The MySQL server listens on port 4000 with user and password of "admin".

                -------------------------   Format of requests    -------------------------
* publisher *
Every endpoints gets a PUT request with the same arguments as json in the "BODY": 
"medication_name", "patient_id" and "action_activation_date". The date should be in format of "%d-%m-%Y".
For example: "http://127.0.0.1:5000/start_period"

* consumer *
The main endpoint is "get_periods" that handles GET requests with "patient_id" and "medication_name" as path variables.
For example: "http://localhost:8000/get_periods?patient_id=Haim&medication_name=Raphapen"

                       -------------------------   Tests    -------------------------
There are unit tests that fully covers the algorithm of getting periods (has been written according TDD).
The tests are under "consumer/consumer_app/tests".

            -----------------------   Special cases when getting periods    ----------------------
Could be special cases when getting periods (e.g. sequence of "stop" or "start"; "cancel start" after "stop", etc.)
Therefore, the application works according these base assumptions:
    1. Every action before the first "start" should be ignored.
    2. "start" as the last action should be ignored.
    3. "cancel_start" after a "stop" should be ignored (when wasn't a "start" between).
    4. "cancel_stop" after a "start" should be ignored (when wasn't a "stop" between).
    5. In case of sequence of "start" or "stop" - 
        we should take the action with the latest activation date.
    6. There isn't a guide for dealing with "start" and "stop" with the same activation date.