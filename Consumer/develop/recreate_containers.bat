REM This script should be used while development for recreating the containers of the application.
REM It shutdown the application's container, cleans resources and restarts the docker-compose process.

docker stop consumer
docker container prune -f
docker rmi consumer_consumer
docker-compose down
docker volume prune -f
docker-compose up