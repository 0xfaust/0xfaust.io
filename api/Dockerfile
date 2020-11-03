# debian golang base image
FROM golang

# installation directory
RUN mkdir -p /opt/services/api
WORKDIR /opt/services/api

# copy project code
COPY . /opt/services/api

# build api server
RUN go get gopkg.in/DataDog/dd-trace-go.v1/ddtrace
RUN go get github.com/DataDog/datadog-go/statsd
RUN go get "golang.org/x/xerrors"
RUN go get github.com/google/uuid
RUN go get "golang.org/x/time/rate"
RUN go build -o ./src/server ./src

CMD ["./src/server"]