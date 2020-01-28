# Start with a Python alpine base image.
FROM python:3.6-buster

# Some stuff that everyone has been copy-pasting
# since the dawn of time.
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install -y supervisor

# Install some necessary things.
# RUN apt-get install -f gcc linux-headers libc-dev postgresql-dev curl openjdk8-jre supervisor
# RUN apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/main --no-cache py3-psycopg2
# RUN echo "http://dl-cdn.alpinelinux.org/alpine/latest-stable/community" >> /etc/apk/repositories
# RUN apk update
# RUN apk --no-cache add docker

#install docker
RUN apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg2
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
RUN apt-get update
RUN apt-get -y install docker-ce

ADD ./requirements.txt /requirements.txt

# Install our requirements.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all our files into the image.
RUN mkdir /code
WORKDIR /code
COPY ./Django /code/
COPY ./wrapper.sh /code/wrapper.sh
COPY ./run_django.sh /code/run_django.sh
RUN chmod 770 /code/wrapper.sh /code/run_django.sh
COPY ./run_background_tasks.sh /code/run_background_tasks.sh
RUN chmod 770 /code/run_background_tasks.sh

# suporvisor is used to let the container both run django in gunicorn and backgroun tasks
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

# the port to expose
EXPOSE 80

# the comman to be executed by this container and all of it's chilren. Carefull to never overwrite this as it won't work.
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisor.conf"]
