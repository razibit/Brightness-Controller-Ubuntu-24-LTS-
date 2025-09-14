#!/bin/bash

# Quick Brightness Test Script
echo "=========================================="
echo "   Brightness Control Test"
echo "=========================================="
echo ""

# Check current brightness
echo "Current brightness:"
cat /sys/class/backlight/*/brightness
echo ""

echo "Max brightness:"
cat /sys/class/backlight/*/max_brightness
echo ""

# Test brightness change
echo "Testing brightness change to 50%..."
MAX_BRIGHT=$(cat /sys/class/backlight/*/max_brightness)
HALF_BRIGHT=$((MAX_BRIGHT / 2))

echo "Setting brightness to $HALF_BRIGHT..."
echo $HALF_BRIGHT | sudo tee /sys/class/backlight/*/brightness > /dev/null

echo ""
echo "New brightness:"
cat /sys/class/backlight/*/brightness

echo ""
echo "If the brightness changed, the hardware control is working!"
echo "You can now use the Brightness Controller app."