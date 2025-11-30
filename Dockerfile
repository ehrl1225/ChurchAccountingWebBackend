FROM ubuntu:latest
LABEL authors="js"

ENTRYPOINT ["top", "-b"]