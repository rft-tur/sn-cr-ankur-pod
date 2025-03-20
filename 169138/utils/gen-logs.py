import json
import random
from datetime import datetime, timedelta

# File to save logs
LOG_FILE = 'traefik_logs.json'
LOG_COUNT = 1000

# Start time for logs (last 2 hours)
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=2)

# Status and method options for the logs
STATUS_CODES = [200, 201, 400, 401, 403, 404, 500, 502, 503]
METHODS = ['GET', 'POST', 'PUT', 'DELETE']
PATHS = ['/api/user', '/api/order', '/api/product', '/login', '/register']

# Function to generate a single log entry
def generate_log_entry(timestamp):
    return {
        "timestamp": timestamp.isoformat() + "Z",
        "status": random.choice(STATUS_CODES),
        "method": random.choice(METHODS),
        "path": random.choice(PATHS),
        "duration_ms": random.randint(10, 1000),
        "client_ip": f"192.168.1.{random.randint(1, 255)}"
    }

def generate_logs():
    logs = []
    current_time = start_time

    for _ in range(LOG_COUNT):
        # Introduce a gap to simulate downtime with 10% probability
        if random.random() < 0.1:
            gap = timedelta(minutes=random.randint(5, 20))
            current_time += gap
        
        # Ensure the timestamp stays within the last 2 hours
        if current_time > end_time:
            break
        
        log = generate_log_entry(current_time)
        logs.append(log)
        
        # Increment time for next log (normal progression)
        current_time += timedelta(seconds=random.randint(1, 10))
    
    # Write logs to file
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

    print(f"Generated {len(logs)} Traefik logs in '{LOG_FILE}'")

if __name__ == "__main__":
    generate_logs()
