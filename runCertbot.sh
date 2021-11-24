#!/bin/bash
echo "Processing: $1"
certbot certonly -d "$1" -d "*.$1" -n \
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

mkdir -p "/dockerRoot/certs/$1"
cp "/dockerRoot/certbot_tmp/config/live/$1" -Lr /dockerRoot/certs/
#-Lr -> copy actual files and recursive