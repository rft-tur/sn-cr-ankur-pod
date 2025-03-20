import json
from datetime import datetime, timedelta

LOG_FILE = 'traefik_logs.json'
GAP_THRESHOLD = timedelta(minutes=10)
PRE_GAP_SAMPLE_SIZE = 5


def load_logs():
    """Load and parse Traefik access logs from the configured JSON file.
    
    Returns:
        list: List of log entries as dictionaries with parsed timestamps
        
    Raises:
        FileNotFoundError: If the log file cannot be located
        JSONDecodeError: If the log file contains invalid JSON
    """
    with open(LOG_FILE, 'r') as f:
        logs = json.load(f)
    return logs


def detect_gaps(logs):
    """Analyze log timestamps to identify service interruption gaps.
    
    Args:
        logs (list): List of log entries containing timestamp and duration_ms
        
    Returns:
        list: Dictionaries containing gap details with structure:
            - start_time (str): ISO formatted gap start time
            - end_time (str): ISO formatted gap end time
            - gap_duration_minutes (float): Duration of gap in minutes
            - avg_pre_gap_duration (float): Average request duration in ms
              for preceding requests
    """
    gaps = []
    if len(logs) < 2:
        return gaps

    for log in logs:
        log['timestamp'] = datetime.fromisoformat(
            log['timestamp'].replace('Z', '+00:00')
        )

    logs.sort(key=lambda x: x['timestamp'])

    for i in range(1, len(logs)):
        prev_time = logs[i - 1]['timestamp']
        curr_time = logs[i]['timestamp']
        gap = curr_time - prev_time

        if gap >= GAP_THRESHOLD:
            # Calculate average duration of preceding requests
            start_idx = max(0, i - PRE_GAP_SAMPLE_SIZE)
            sample_entries = logs[start_idx:i]
            durations = [entry['duration_ms'] for entry in sample_entries]
            avg_duration = sum(durations) / len(durations) if durations else 0

            gaps.append({
                'start_time': prev_time.isoformat().replace('+00:00', 'Z'),
                'end_time': curr_time.isoformat().replace('+00:00', 'Z'),
                'gap_duration_minutes': gap.total_seconds() / 60,
                'avg_pre_gap_duration': avg_duration
            })

    return gaps


def main():
    """Orchestrate log analysis workflow and present results."""
    logs = load_logs()
    gaps = detect_gaps(logs)

    if gaps:
        print(f"\nDetected {len(gaps)} service gap(s):")
        for gap in gaps:
            print(
                f"• {gap['start_time']} → {gap['end_time']} "
                f"({gap['gap_duration_minutes']:.1f} min gap)\n"
                f"  Avg. response time pre-gap: "
                f"{gap['avg_pre_gap_duration']:.1f}ms\n"
            )
    else:
        print("\nNo significant service gaps detected.")


if __name__ == "__main__":
    main()