#!/bin/bash
# System Resource Monitor Script v1.0.0

# Colors for better readability if supported
printf "\n\033[1;34m--- System Resource Report ---\033[0m\n"

# Uptime
UPTIME=$(uptime -p)
printf "\033[1;32mUptime:\033[0m %s\n" "$UPTIME"

# Load Average
LOAD=$(uptime | awk -F'load average:' '{ print $2 }' | sed 's/^ //')
printf "\033[1;32mSystem Load:\033[0m %s\n" "$LOAD"

# RAM & Swap
MEM=$(free -h | awk '/^Mem:/ {print $3 " / " $2}')
SWAP=$(free -h | awk '/^Swap:/ {print $3 " / " $2}')
printf "\033[1;32mMemory Usage:\033[0m %s\n" "$MEM"
printf "\033[1;32mSwap Usage:\033[0m   %s\n" "$SWAP"

# Disk Usage
DISK=$(df -h / | awk 'NR==2 {print $3 " / " $2 " (" $5 ")"}')
printf "\033[1;32mDisk Usage:\033[0m   %s\n" "$DISK"

printf "\033[1;34m------------------------------\033[0m\n\n"
