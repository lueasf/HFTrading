FROM ubuntu:latest

ARG buildPath

WORKDIR /app

COPY ${buildPath}/binaries/aeronmd /app/aeronmd

RUN chmod +x /app/aeronmd

CMD ["/app/aeronmd", "-Daeron_print_configuration=true"]