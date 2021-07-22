FROM python:3.9.6-slim-buster

# Install required library libmysqlclient 
# (and build-essential for building mysqlclient python extension)
RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*
    
ADD scripts /scripts

ADD consumer /consumer
WORKDIR /consumer
RUN pip install -r requirements.txt

EXPOSE 8000
#CMD ["python", "/consumer/manage.py", "runserver"]