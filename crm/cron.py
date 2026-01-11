import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    log_path = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    
    status = "CRM is alive"
    try:
        transport = RequestsHTTPTransport(url='http://localhost:8000/graphql')
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql('{ hello }')
        client.execute(query)
    except Exception:
        status = "CRM is alive (GraphQL unresponsive)"

    with open(log_path, "a") as f:
        f.write(f"{timestamp} {status}\n")

def update_low_stock():
    url = "http://localhost:8000/graphql"
    log_path = "/tmp/low_stock_updates_log.txt" 
    
    transport = RequestsHTTPTransport(url=url)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    mutation = gql("""
        mutation {
          updateLowStockProducts {
            updatedProducts
            message
          }
        }
    """)
    
    try:
        result = client.execute(mutation)
        updated_items = result['updateLowStockProducts']['updatedProducts']
        
        with open(log_path, "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for item in updated_items:
                f.write(f"{timestamp} - Updated: {item}\n")
    except Exception as e:
        print(f"Error: {e}")
