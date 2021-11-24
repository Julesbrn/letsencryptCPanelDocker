#!/bin/bash
echo "======PREHOOK======"
python3 /dockerRoot/scripts/main.py add $CERTBOT_DOMAIN "_acme-challenge" $CERTBOT_VALIDATION
echo $CERTBOT_DOMAIN
echo $CERTBOT_VALIDATION
echo "======/PREHOOK======"

