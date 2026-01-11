from datetime import datetime
import requests
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    url = "http://localhost:8000/graphql"
    log_path = "/tmp/crm_report_log.txt"
    
    transport = RequestsHTTPTransport(url=url)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    query = gql("""
        query {
          totalStats
        }
    """)
    
    try:
        result = client.execute(query)
        stats = result.get('totalStats', {})
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = f"{timestamp} - Report: {stats.get('customers', 0)} customers, {stats.get('orders', 0)} orders, {stats.get('revenue', 0)} revenue\n"
        
        with open(log_path, "a") as f:
            f.write(report)
    except Exception as e:
        print(f"Error generating report: {e}")
