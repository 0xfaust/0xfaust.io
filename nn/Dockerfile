# official debian base image
FROM debian:latest

# installation directory
RUN mkdir -p /opt/services/keras
WORKDIR /opt/services/keras
COPY requirements.txt /opt/services/keras

# install dependencies
RUN apt-get update -y
RUN apt-get install -y python3-dev python3-pip build-essential
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir

# copy project code
COPY . /opt/services/keras

# run training loop
CMD ["python3", "./src/covnet.py", "> /dev/null"]