# official python base image
FROM python:3.7

# installation directory
RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

# install dependencies
RUN pip install django gunicorn

# copy project code
COPY . /opt/services/djangoapp/src

# expose port 8000
EXPOSE 8000

# start django in container
CMD ["gunicorn", "--chdir", "faust", "--bind", ":8000", "faust.wsgi:application"]