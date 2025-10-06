import json
import time
import os
from datetime import datetime
from kafka import KafkaProducer

# ---------------- CONFIG ----------------
FUTURE_EVENTS_FILE = "C:/Users/Russel.GabrielThomas/future_events.json"

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
TOPIC_NAME = "raw_table"


# ---------------- HELPERS ----------------
def load_future_events():
    """Load future events from disk."""
    if os.path.exists(FUTURE_EVENTS_FILE):
        with open(FUTURE_EVENTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_future_events(events):
    now = datetime.now()

    future_only = [
        ev
        for e in events
        for ev in (e if isinstance(e, list) else [e])  # flatten
        if isinstance(ev, dict)
        and "event_time" in ev
        and datetime.strptime(ev["event_time"], "%Y-%m-%d %H:%M:%S") >= now
    ]

    print(f"💾 Saving {len(future_only)} future events...")
    # write back to disk
    with open("future_events.json", "w") as f:
        json.dump(future_only, f, indent=2)


def send_to_kafka(event):
    """Send event to Kafka."""
    producer.send(TOPIC_NAME, event)
    print(f"Sent to Kafka: {event['event_type']} at {event['event_time']}")


# ---------------- STREAM LOOP ----------------
def stream_future_events_only():
    """Continuously check and send due events from future_events.json."""
    future_events = load_future_events()
    print(f"Loaded {len(future_events)} future events from disk.")
    print(type(future_events), len(future_events))
    print(type(future_events[0]))


    while True:
        now = datetime.now()

        # Find events whose time has come
        due_events = [
            e for e in future_events
            if "event_time" in e
            and datetime.strptime(e["event_time"], "%Y-%m-%d %H:%M:%S") <= now
        ]

        # Send due events to Kafka
        for ev in due_events:
            send_to_kafka(ev)

        # Keep only not-yet-due events
        future_events = [e for e in future_events if e not in due_events]

        # Persist updated queue
        save_future_events(future_events)

        print(f"✅ Sent {len(due_events)} events | {len(future_events)} still queued")
        time.sleep(1)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    try:
        print("▶️ Starting future events streaming...")
        stream_future_events_only()
    except KeyboardInterrupt:
        print("⏹️ Stopping gracefully...")
        save_future_events(load_future_events())
