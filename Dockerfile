# official python base image
FROM python:3.7

# installation directory
RUN mkdir -p /opt/services/django/src
WORKDIR /opt/services/django/src
COPY requirements.txt /opt/services/django/src

# install dependencies
RUN pip install -r requirements.txt

# copy project code
COPY . /opt/services/django/src

# expose port 8000
EXPOSE 8000

# start django in container
CMD ["gunicorn", "--chdir", "src", "--bind", ":8000", "faust.wsgi:application"]