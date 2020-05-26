# official python base image
FROM python:3.7

# installation directory
RUN mkdir -p /opt/services/django
WORKDIR /opt/services/django
COPY requirements.txt /opt/services/django

# install dependencies
RUN pip install -r requirements.txt

# copy project code
COPY . /opt/services/django

# expose port 8000
EXPOSE 8000

# start django in container
CMD ["ddtrace-run", "gunicorn", "--chdir", "src", "--bind", ":8000", "faust.wsgi:application"]
