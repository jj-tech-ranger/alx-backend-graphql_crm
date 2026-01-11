# CRM Automation and Task Scheduling

This project implements various automation tasks using system crons, django-crontab, and Celery with Celery Beat.

## Prerequisites
1. **Install Redis**: 
   Ensure Redis is installed and running on your system.
   - On Ubuntu/Debian: `sudo apt install redis-server`
   - On macOS: `brew install redis`
2. **Install Dependencies**:
   Run the following command to install required libraries:
   ```bash
   pip install -r requirements.txt
