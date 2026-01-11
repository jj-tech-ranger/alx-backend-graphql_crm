import datetime
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """Logs a heartbeat message to verify the CRM application's health."""
    log_path = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"
    
    with open(log_path, "a") as f:
        f.write(message)

def update_low_stock():
    """Triggers a GraphQL mutation to restock products with stock < 10."""
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
        response = client.execute(mutation)
        updated_items = response['updateLowStockProducts']['updatedProducts']
        
        with open(log_path, "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for product_name in updated_items:
                f.write(f"{timestamp} - Restocked: {product_name} (New Stock: 20)\n")
                
    except Exception as e:
        print(f"Error executing stock update: {e}")
