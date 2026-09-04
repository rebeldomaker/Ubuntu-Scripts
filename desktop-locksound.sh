#!/bin/bash

last_event_time=0
debounce_delay=2 # 2 seconds delay

# todo maybe remove later. Monitor GNOME ScreenSaver signals
dbus-monitor --session "type='signal',interface='org.gnome.ScreenSaver'" | \
while read -r x; do
    current_time=$(date +%s)
    if [ $((current_time - last_event_time)) -lt $debounce_delay ]; then
        continue
    fi
    case "$x" in 
        *"boolean true"*) 
            paplay /usr/share/sounds/Yaru/stereo/desktop-logoff.oga
            last_event_time=$(date +%s)
            ;;
        *"boolean false"*) 
            paplay /usr/share/sounds/Yaru/stereo/desktop-login.oga
            last_event_time=$(date +%s)
            ;;
    esac
done
