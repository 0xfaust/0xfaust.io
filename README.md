# 0xfaust.io
Sandbox Website for Testing :rocket:  
  
![Release Badge](https://img.shields.io/github/v/tag/0xfaust/0xfaust.io?color=red&label=release&sort=semver) 
![Docker Build Badge](https://img.shields.io/docker/cloud/build/0xfaust/0xfaust.io) 
![Site Status Badge](https://img.shields.io/website?down_message=down&label=site+status&up_message=up&url=http://0xfaust.io:8000)  
Site: [0xfaust.io:8000](http://0xfaust.io:8000)  
DockerHub: [0xfaust/0xfaust.io](https://hub.docker.com/r/0xfaust/0xfaust.io)  
   
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Make sure you have installed all of the following prerequisites on your development machine. These instructions presume that you are working on a Linux based host but the project has been tested on OSX and it should work on Windows machines with some modifications.

- [Git](https://git-scm.com/downloads) for pulling the repository and for any contributions to the project
- [Docker](https://docs.docker.com/get-docker/) Engine for  for building and containerising the applications 
- [Docker Compose](https://docs.docker.com/get-docker/) for defining and running multi-container applications

### Installing
#### Entire Project (Recommended)
1. Clone this repository to get all of the files necessary for building the project  
```$ git clone https://github.com/0xfaust/0xfaust.io```  
2. Make copies of the Environment Variable files  
```$ cd 0xfaust.io && cp .env.template .env && cp config/postgres/.env.template config/postgres/.env```
3. Configure the ```.env``` and ```config/postgres/.env``` files for your environment.
4. Build and run all of the Docker Containers in detached mode.  
```$ docker-compose up -d --build```   
5. The site can then be accessed via [localhost:8000](http://localhost:8000) in your browser.

#### Application Container Only (Dev)
1. Pull the 0xfaust/0xfaust.io Docker Image from Dockerhub  
```$ docker pull 0xfaust/0xfaust.io```
2. Create and run the Docker Container in detached mode, with port 8000 exposed and a [Django 'Secret Key'](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-SECRET_KEY) environment variable set.  
```$ docker run -d -p 8000:8000 -e DJANGO_SECRET_KEY=<RANDOM KEY> 0xfaust/0xfaust.io```
3. The site can then be accessed via [localhost:8000](http://localhost:8000) in your browser.

## Deployment
There are a few additional considerations and modifications that need to be made in order to host the project on a live system. Some of the considerations are outlined in Django's [Deployment Checklist](https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/) and most of them have already been addressed using Environment Variables. Here are some additional steps to go from ```localhost``` to your server's IP.
1. In ```config/nginx/conf.d/local.conf```, change ```localhost``` to the IP of your server.
2. In ```src/faust/settings.py``` change ```localhost``` to the list of IP address's and domains, e.g.  
```ALLOWED_HOSTS = ['xxx.xxx.xxx.xxx','0xfaust.io','www.0xfaust.io']```

## Built With

* [Django](https://www.djangoproject.com/) - Web Framework
* [Nginx](https://www.nginx.com/) - Reverse Proxy
* [Postgress](https://www.postgresql.org/) - Database Management System
* [GUnicorn](https://gunicorn.org/) - Web Server Gateway Interface
* [Datadog](https://www.datadoghq.com/) - Monitoring Service
* [Keras](https://keras.io/) - Neural Networks

## Versioning

A basic [SemVer](http://semver.org/) system is used for versioning. For the versions available, see the [tags and releases](https://github.com/0xfaust/0xfaust.io/releases) on this repository.
