#!/bin/bash

# Define the absolute path to your project and log file
PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Execute Django shell command to delete customers with no orders in the last year
# Logs output with a timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting cleanup..." >> $LOG_FILE
python3 "$PROJECT_DIR/manage.py" shell <<EOF >> $LOG_FILE
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer
import sys

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__isnull=True, date_joined__lt=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()
print(f"Deleted {count} inactive customers.")
EOF