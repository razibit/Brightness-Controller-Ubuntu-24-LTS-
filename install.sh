#!/bin/bash

# Brightness Controller Installation Script
# For Ubuntu 24 LTS

echo "=========================================="
echo "   Brightness Controller Setup Script"
echo "=========================================="
echo ""

# Function to check if command was successful
check_status() {
    if [ $? -eq 0 ]; then
        echo "✓ $1 - Success"
    else
        echo "✗ $1 - Failed"
        echo "Please check the error messages above."
        exit 1
    fi
}

# Update package list
echo "Updating package list..."
sudo apt update
check_status "Package list update"

# Install Python GTK dependencies
echo ""
echo "Installing Python GTK dependencies..."
sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0
check_status "Python GTK installation"

# Install optional brightness control tools
echo ""
echo "Installing optional brightness control tools..."
sudo apt install -y brightnessctl
check_status "brightnessctl installation"

# Make the brightness controller executable
echo ""
echo "Making brightness controller executable..."
chmod +x brightness_controller.py
check_status "Making script executable"

# Create applications directory if it doesn't exist
mkdir -p ~/.local/share/applications

# Create desktop entry
echo ""
echo "Creating desktop entry..."
cat > ~/.local/share/applications/brightness-controller.desktop << EOF
[Desktop Entry]
Name=Brightness Controller
Comment=Control screen brightness when default slider doesn't work
Exec=/home/apostrophe/Downloads/Owmegle-linux/brightness_controller.py
Icon=display-brightness
Terminal=false
Type=Application
Categories=Utility;Settings;
StartupNotify=true
EOF

check_status "Desktop entry creation"

# Update desktop database
echo ""
echo "Updating desktop database..."
update-desktop-database ~/.local/share/applications/
check_status "Desktop database update"

# Set up brightness control permissions (optional but recommended)
echo ""
echo "Setting up brightness control permissions..."
echo "This allows the app to control brightness without asking for password every time."

# Check if brightness control exists
if [ -d "/sys/class/backlight" ]; then
    BACKLIGHT_DIRS=$(find /sys/class/backlight -name "brightness" 2>/dev/null)
    if [ ! -z "$BACKLIGHT_DIRS" ]; then
        echo "Found brightness controls:"
        for dir in $BACKLIGHT_DIRS; do
            device=$(basename $(dirname "$dir"))
            echo "  - $device"
        done
        
        # Create udev rule for brightness control
        echo "Creating udev rule for brightness permissions..."
        sudo tee /etc/udev/rules.d/90-brightness.rules > /dev/null << EOF
# Allow users in video group to control backlight
ACTION=="add", SUBSYSTEM=="backlight", KERNEL=="*", RUN+="/bin/chgrp video /sys/class/backlight/%k/brightness"
ACTION=="add", SUBSYSTEM=="backlight", KERNEL=="*", RUN+="/bin/chmod g+w /sys/class/backlight/%k/brightness"
EOF
        
        # Add user to video group
        sudo usermod -a -G video $USER
        
        # Apply udev rules
        sudo udevadm control --reload-rules
        sudo udevadm trigger
        
        echo "✓ Brightness permissions configured"
        echo "Note: You may need to log out and back in for group changes to take effect."
    fi
else
    echo "! No hardware brightness control found - the app will use software brightness"
fi

echo ""
echo "=========================================="
echo "        Installation Complete!"
echo "=========================================="
echo ""
echo "How to use:"
echo "1. Search for 'Brightness Controller' in your applications menu"
echo "2. Or run directly: ./brightness_controller.py"
echo "3. Or double-click on brightness_controller.py in file manager"
echo ""
echo "If you have issues:"
echo "- Run: python3 brightness_controller.py --check"
echo "- This will test what brightness methods work on your system"
echo ""
echo "For your RTX 3050 / i5-12500H laptop:"
echo "- The app should work with Intel integrated graphics brightness"
echo "- If hardware control doesn't work, it will use software brightness"
echo "- Software brightness works immediately but resets on reboot"
echo ""
echo "Note: If the app asks for your password, that's normal for hardware"
echo "brightness control. The password setup above should minimize this."