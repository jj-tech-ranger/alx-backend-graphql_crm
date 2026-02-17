#!/bin/bash

# Navigate to project root (adjust path if needed)
PROJECT_DIR="$(dirname "$(dirname "$(realpath "$0")")")"
cd "$PROJECT_DIR" || exit 1

# Navigate to project root
# cd "C:/Users/HP/Desktop/ALX Prodev program/alx-backend-graphql_crm" || exit 1

# Run Django shell command to delete inactive customers
DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff).distinct()
count = qs.count()
qs.delete()
print(count)
")

# Log result with timestamp
echo \"\$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $DELETED_COUNT\" >> /tmp/customer_cleanup_log.txt
