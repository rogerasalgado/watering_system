#!/usr/bin/with-contenv bashio

DATA_DIR="/data"

mkdir -p "$DATA_DIR"

# -----------------------------
# config.json (seed inicial)
# -----------------------------
if [ ! -f "$DATA_DIR/config.json" ]; then
  bashio::log.info "Creating default config.json"

  cat <<'EOF' > "$DATA_DIR/config.json"
{
    "BROKER_ADDRESS":"broker.mqtt-dashboard.com",
    "BROKER_PORT":"1883",
    "SUBSCRIBE_TOPIC":"CHANGE_ME",
    "PUBLISH_TOPIC":"CHANGE_ME"
}
EOF
fi

# -----------------------------
# schedule.json (seed inicial)
# -----------------------------
if [ ! -f "$DATA_DIR/schedule.json" ]; then
  bashio::log.info "Creating default schedule.json"

  cat <<'EOF' > "$DATA_DIR/schedule.json"
[
    {"zone": 1, "day": [0, 1, 2, 3, 4, 5, 6], "start_time": "7:00", "duration": 300},
    {"zone": 2, "day": [0, 1, 2, 3, 4, 5, 6], "start_time": "10:06", "duration": 600},
    {"zone": 3, "day": [0, 1, 2, 3, 4, 5, 6], "start_time": "7:17", "duration": 150},
    {"zone": 4, "day": [0, 1, 2, 3, 4, 5, 6], "start_time": "7:20", "duration": 150},
    {"zone": 5, "day": [0, 1, 2, 3, 4, 5, 6], "start_time": "22:00", "duration": 600}
]
EOF
fi

# -----------------------------
# start Python controller
# -----------------------------
bashio::log.info "Starting watering system controller"
python /app/watering_system_controller.py