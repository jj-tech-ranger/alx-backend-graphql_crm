import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport)
    query = gql("{ totalStats }")
    
    try:
        result = client.execute(query)
        stats = eval(result['totalStats'])
        
        log_path = "/tmp/crm_report_log.txt"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = f"{timestamp} - Report: {stats['customers']} customers, {stats['orders']} orders, {stats['revenue']} revenue\n"
        
        with open(log_path, "a") as f:
            f.write(report)
    except Exception as e:
        print(f"Error: {e}")
