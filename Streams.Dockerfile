FROM ubuntu:latest

ARG buildPath

WORKDIR /app

COPY ${buildPath}/binaries/streams_exec /app/streams

RUN chmod +x /app/streams

CMD ["/app/streams"]