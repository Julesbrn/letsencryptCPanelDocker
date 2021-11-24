#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
#lets.110321@e.darkmesa.net

current_time=$(date "+%Y.%m.%d-%H.%M.%S")

emailAddress="lets.110321@e.darkmesa.net"
FILES="/dockerRoot/domains/*"
mkdir -p "/dockerRoot/certbot_tmp/"
mkdir -p "/dockerRoot/logs/"

if [ "$(ls -A /dockerRoot/domains/)" ]; 
then
  for f in $FILES
  do
    echo "f: ${f}"
    tmp1="${f/\/dockerRoot\/domains\//}" #remove the file path
    echo "tmp1: ${tmp1}"
    tmp2="${tmp1/\.json/}" #remove the .json
    echo "tmp2: ${tmp2}"
    tmp3="${tmp2/\_/.}" #change the _ to a . so we can use the domain. e.g. example_com.json -> example.com
    echo "Processing: ${tmp3}"
    certbot certonly -d "${tmp3}" -d "*.${tmp3}" -n \
      --manual-auth-hook /dockerRoot/scripts/hooks/prehook.sh \
      --manual-cleanup-hook /dockerRoot/scripts/hooks/posthook.sh \
      --preferred-challenges dns \
      --config-dir /dockerRoot/certbot_tmp/config \
      --work-dir /dockerRoot/certbot_tmp/work \
      --logs-dir /dockerRoot/certbot_tmp/log \
      --manual \
      --email "${emailAddress}" \
      --agree-tos  \
      --manual-public-ip-logging-ok \
      --cert-path /dockerRoot/certs/

  # >> "/dockerRoot/logs/log_${tmp3}_${current_time}"
    mkdir -p "/dockerRoot/certs/${tmp3}"
    cp "/dockerRoot/certbot_tmp/config/live/${tmp3}" -Lr /dockerRoot/certs/
    #-Lr -> copy actual files and recursive
  done
else
  echo "No domain info found."
fi