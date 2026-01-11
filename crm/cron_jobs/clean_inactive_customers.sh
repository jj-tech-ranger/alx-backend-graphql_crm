#!/bin/bash

MANAGE_PY="/home/user/alx-backend-graphql_crm/manage.py"
LOG_FILE="/tmp/customer_cleanup_log.txt"

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Execute cleanup via manage.py shell
python3 "$MANAGE_PY" shell <<EOF
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__isnull=True, date_joined__lt=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()

with open("$LOG_FILE", "a") as f:
    f.write(f"$TIMESTAMP - Deleted {count} inactive customers.\n")
EOF
