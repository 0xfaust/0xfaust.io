# official python base image
FROM python:3.7

# installation directory
RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

# install dependencies
RUN pip install django

# copy project code
COPY . /opt/services/djangoapp/src

# expose port 8000
EXPOSE 8000

# start django in container
CMD ["python", "/opt/services/djangoapp/src/faust/manage.py", "runserver", "0.0.0.0:8000"]