import datetime
from gql import gql, Client  #
from gql.transport.requests import RequestsHTTPTransport  #

def log_crm_heartbeat():
    log_path = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql')
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql('{ hello }')
    
    try:
        client.execute(query)
        status = "CRM is alive"
    except Exception:
        status = "CRM is alive but GraphQL is unresponsive"

    with open(log_path, "a") as f:
        f.write(f"{timestamp} {status}\n") #

def update_low_stock():
   
    pass
