FROM debian:stable-slim

#RUN apt update && apt install -y cerbot
RUN apt update && apt install -y certbot

RUN mkdir /dockerRoot

#/dockerRoot/certbot_tmp -> tmp dir used by certbot
#/dockerRoot/domains/ -> directory with domain info jsons
#/dockerRoot/certs/ -> This is where the certs will be copied

COPY ./main.py /dockerRoot/scripts/main.py
COPY ./runCertbot.sh /dockerRoot/scripts/runCertbot.sh
COPY ./runAllDomains.sh /dockerRoot/scripts/runAllDomains.sh

COPY ./hooks/ /dockerRoot/scripts/hooks/

#CMD python /app/app.py
CMD tail -f /dev/null
