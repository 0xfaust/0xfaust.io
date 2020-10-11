# debian golang base image
FROM golang

# installation directory
RUN mkdir -p /opt/services/api
WORKDIR /opt/services/api

# copy project code
COPY . /opt/services/api

# build api server
RUN go build -o ./src/server ./src

CMD ["./src/server"]