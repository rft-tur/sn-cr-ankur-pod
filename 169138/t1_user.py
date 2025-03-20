import json
from datetime import datetime, timedelta

LOG_FILE = 'traefik_logs.json'
GAP_THRESHOLD = timedelta(minutes=10)

def loadLogs():
    with open(LOG_FILE, 'r') as f:
        logs = json.load(f)
    return logs

def detectGaps(logs):
    gaps = []
    if len(logs) < 2:
        return gaps
    
    for log in logs:
        log['timestamp'] = datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00'))
    
    logs.sort(key=lambda x: x['timestamp'])
    
    for i in range(1, len(logs)):
        prevTime = logs[i - 1]['timestamp']
        curr_time = logs[i]['timestamp']
        gap = curr_time - prevTime
        
        if gap >= GAP_THRESHOLD:
            gaps.append({
                'start_time': prevTime.isoformat() + 'Z',
                'end_time': curr_time.isoformat() + 'Z',
                'gap_duration_minutes': gap.total_seconds() / 60
            })
    
    return gaps

def main():
    logs = loadLogs()
    gaps = detectGaps(logs)

    if gaps:
        print(f"\nDetected {len(gaps)} gap(s) of 10+ minutes:\n")
        for gap in gaps:
            print(f"> From {gap['start_time']} to {gap['end_time']} ({gap['gap_duration_minutes']:.2f} minutes)")
    else:
        print("\nNo gaps of 10+ minutes detected.")

if __name__ == "__main__":
    main()
