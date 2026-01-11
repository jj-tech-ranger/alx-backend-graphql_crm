import requests
import datetime

# Define the GraphQL endpoint
URL = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/order_reminders_log.txt"

# GraphQL query for orders within the last 7 days
query = """
query {
  allOrders(orderDate_Gte: "%s") {
    id
    customer {
      email
    }
  }
}
""" % (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()

try:
    response = requests.post(URL, json={'query': query})
    data = response.json()
    orders = data['data']['allOrders']

    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for order in orders:
            log_entry = f"{timestamp} - Order ID: {order['id']}, Email: {order['customer']['email']}\n"
            f.write(log_entry)

    print("Order reminders processed!")  #
except Exception as e:
    print(f"Error: {e}")