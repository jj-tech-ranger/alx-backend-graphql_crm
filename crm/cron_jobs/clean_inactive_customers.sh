#!/bin/bash

LOG_FILE="/tmp/customer_cleanup_log.txt"
MANAGE_PY="$(cd "$(dirname "$0")/../.." && pwd)/manage.py"

python3 "$MANAGE_PY" shell <<EOF >> "$LOG_FILE"
import datetime
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - datetime.timedelta(days=365)
inactive_customers = Customer.objects.filter(order__isnull=True, date_joined__lt=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"{timestamp} - Deleted {count} inactive customers.")
EOF
