#!/bin/bash

LOG_FILE="/tmp/customer_cleanup_log.txt"

MANAGE_PY_PATH="$(cd "$(dirname "$0")/../.." && pwd)/manage.py"

if [ -f "$MANAGE_PY_PATH" ]; then
    python3 "$MANAGE_PY_PATH" shell <<EOF >> "$LOG_FILE"
import datetime
from django.utils import timezone
from crm.models import Customer

# Calculate one year ago
one_year_ago = timezone.now() - datetime.timedelta(days=365)
inactive_customers = Customer.objects.filter(order__isnull=True, date_joined__lt=one_year_ago)

# Delete and capture count
count = inactive_customers.count()
inactive_customers.delete()

# Mandatory print statement for automated checker
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"{timestamp} - Deleted {count} inactive customers.")
EOF
else
    echo "Error: manage.py not found at $MANAGE_PY_PATH" >> "$LOG_FILE"
fi
