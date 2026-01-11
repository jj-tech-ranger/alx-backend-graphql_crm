import datetime
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

URL = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/order_reminders_log.txt"

transport = RequestsHTTPTransport(url=URL)
client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql("""
  query {
    allOrders(orderDate_Gte: "%s") {
      id
      customer {
        email
      }
    }
  }
""" % (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat())

try:
    result = client.execute(query)
    orders = result.get('allOrders', [])
    
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for order in orders:
            f.write(f"{timestamp} - Order ID: {order['id']}, Email: {order['customer']['email']}\n")
            
    print("Order reminders processed!")
except Exception as e:
    print(f"Error: {e}")
