import datetime
import requests


def log_crm_heartbeat():
    log_path = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"  #

    with open(log_path, "a") as f:
        f.write(message)


def update_low_stock():
    url = "http://localhost:8000/graphql"
    mutation = """
    mutation {
      updateLowStockProducts {
        updatedProducts
        message
      }
    }
    """
    try:
        response = requests.post(url, json={'query': mutation})
        # Log results to /tmp/low_stock_updates_log.txt
    except Exception as e:
        pass