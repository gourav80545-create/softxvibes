#!/bin/bash

# Sync time with NTP before starting the bot
echo "Syncing system time with NTP..."
ntpdate -s time.google.com || ntpdate -s pool.ntp.org || ntpdate -s time.cloudflare.com || echo "NTP sync failed, continuing with system time"

# Force time sync using systemd-timesyncd if available
if command -v timedatectl &> /dev/null; then
    timedatectl set-ntp true 2>/dev/null || true
fi

# Alternative: Set time from HTTP if NTP fails
if ! ntpdate -s time.google.com 2>/dev/null; then
    echo "NTP failed, trying HTTP time sync..."
    HTTP_TIME=$(curl -s --head http://google.com | grep Date | sed -e 's/Date: //g' | cut -d' ' -f3-6)
    if [ ! -z "$HTTP_TIME" ]; then
        date -s "$HTTP_TIME" 2>/dev/null || true
        echo "Time set from HTTP: $HTTP_TIME"
    fi
fi

# Wait for time to stabilize
echo "Waiting for time to stabilize..."
sleep 20

# Start the bot
echo "Starting bot..."
python bot.py
