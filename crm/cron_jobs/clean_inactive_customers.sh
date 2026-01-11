#!/bin/bash

# Define log file path
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Dynamically find manage.py to avoid "doesn't exist" errors
MANAGE_PY_PATH=$(find . -name "manage.py" | head -n 1)

if [ -f "$MANAGE_PY_PATH" ]; then
    # Execute Python command via Django shell
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

# Log with timestamp and mandatory print statement
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"{timestamp} - Deleted {count} inactive customers.")
EOF
else
    echo "Error: manage.py not found" >> "$LOG_FILE"
fi
