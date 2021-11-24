#!/bin/bash
echo "======POSTHOOK======"
python3 /dockerRoot/scripts/main.py remove $CERTBOT_DOMAIN "_acme-challenge" $CERTBOT_VALIDATION
echo $CERTBOT_DOMAIN
echo $CERTBOT_VALIDATION
echo "======/POSTHOOK======"

