#!/usr/bin/env python3
"""
Brightness Controller for Ubuntu 24 LTS
A simple GUI app to control screen brightness when the default slider doesn't work.
"""

import gi
import subprocess
import os
import sys
import glob
from pathlib import Path

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class BrightnessController:
    def __init__(self):
        self.brightness_path = None
        self.max_brightness = 100
        self.current_brightness = 50
        
        # Find brightness control path
        self.find_brightness_path()
        
        # Create the main window
        self.window = Gtk.Window()
        self.window.set_title("Brightness Controller")
        self.window.set_default_size(400, 200)
        self.window.set_resizable(False)
        self.window.connect("destroy", Gtk.main_quit)
        
        # Set window icon (if available)
        try:
            self.window.set_icon_name("display-brightness")
        except:
            pass
        
        self.create_ui()
        self.update_current_brightness()
        
    def find_brightness_path(self):
        """Find the correct brightness control path for your system"""
        possible_paths = [
            "/sys/class/backlight/*/brightness",
            "/sys/class/backlight/*/max_brightness"
        ]
        
        # Look for NVIDIA WMI EC backlight first (common on NVIDIA laptops)
        nvidia_paths = glob.glob("/sys/class/backlight/nvidia_wmi_ec_backlight/brightness")
        if nvidia_paths:
            self.brightness_path = "/sys/class/backlight/nvidia_wmi_ec_backlight"
            return
            
        # Look for Intel graphics (common on laptops)
        intel_paths = glob.glob("/sys/class/backlight/intel_backlight/brightness")
        if intel_paths:
            self.brightness_path = "/sys/class/backlight/intel_backlight"
            return
            
        # Look for other backlight controls
        backlight_dirs = glob.glob("/sys/class/backlight/*")
        if backlight_dirs:
            # Use the first available backlight
            self.brightness_path = backlight_dirs[0]
            return
            
        print("Warning: No brightness control found. Will try xrandr as fallback.")
        
    def get_max_brightness(self):
        """Get maximum brightness value"""
        if not self.brightness_path:
            return 100
            
        try:
            with open(f"{self.brightness_path}/max_brightness", "r") as f:
                return int(f.read().strip())
        except:
            return 100
            
    def get_current_brightness(self):
        """Get current brightness value"""
        if not self.brightness_path:
            return 50
            
        try:
            with open(f"{self.brightness_path}/brightness", "r") as f:
                current = int(f.read().strip())
                max_bright = self.get_max_brightness()
                # Convert to percentage
                return int((current / max_bright) * 100)
        except:
            return 50
            
    def set_brightness(self, percentage):
        """Set brightness using multiple methods"""
        success = False
        
        # Method 1: Direct file write (requires proper permissions)
        if self.brightness_path:
            try:
                max_bright = self.get_max_brightness()
                brightness_value = int((percentage / 100) * max_bright)
                
                # Try to write directly without sudo first
                brightness_file = f"{self.brightness_path}/brightness"
                try:
                    with open(brightness_file, 'w') as f:
                        f.write(str(brightness_value))
                    success = True
                except PermissionError:
                    # If direct write fails, try with sudo
                    cmd = f"echo {brightness_value} | sudo tee {brightness_file} > /dev/null"
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        success = True
            except Exception as e:
                print(f"Direct write failed: {e}")
        
        # Method 2: Using xrandr (works without root but only temporary)
        if not success:
            try:
                # Get the primary display
                result = subprocess.run(['xrandr', '--listactivemonitors'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        # Extract display name from the second line
                        display_line = lines[1]
                        display_name = display_line.split()[-1]
                        
                        # Set brightness using xrandr
                        brightness_decimal = percentage / 100.0
                        cmd = ['xrandr', '--output', display_name, '--brightness', str(brightness_decimal)]
                        result = subprocess.run(cmd, capture_output=True)
                        if result.returncode == 0:
                            success = True
            except Exception as e:
                print(f"xrandr method failed: {e}")
        
        # Method 3: Using brightnessctl (if available)
        if not success:
            try:
                cmd = ['brightnessctl', 'set', f"{percentage}%"]
                result = subprocess.run(cmd, capture_output=True)
                if result.returncode == 0:
                    success = True
            except Exception as e:
                print(f"brightnessctl method failed: {e}")
        
        return success
    
    def create_ui(self):
        """Create the user interface"""
        # Main container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        vbox.set_margin_left(20)
        vbox.set_margin_right(20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        
        # Title label
        title_label = Gtk.Label()
        title_label.set_markup("<big><b>Screen Brightness Controller</b></big>")
        vbox.pack_start(title_label, False, False, 0)
        
        # Current brightness info
        self.info_label = Gtk.Label()
        self.info_label.set_text("Detecting current brightness...")
        vbox.pack_start(self.info_label, False, False, 0)
        
        # Brightness slider
        brightness_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        dim_label = Gtk.Label("Dim")
        brightness_box.pack_start(dim_label, False, False, 0)
        
        self.brightness_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 100, 1)
        self.brightness_scale.set_value(50)
        self.brightness_scale.set_hexpand(True)
        self.brightness_scale.connect("value-changed", self.on_brightness_changed)
        brightness_box.pack_start(self.brightness_scale, True, True, 0)
        
        bright_label = Gtk.Label("Bright")
        brightness_box.pack_start(bright_label, False, False, 0)
        
        vbox.pack_start(brightness_box, False, False, 0)
        
        # Percentage label
        self.percentage_label = Gtk.Label()
        self.percentage_label.set_text("50%")
        vbox.pack_start(self.percentage_label, False, False, 0)
        
        # Preset buttons
        preset_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        preset_box.set_halign(Gtk.Align.CENTER)
        
        presets = [("25%", 25), ("50%", 50), ("75%", 75), ("100%", 100)]
        for label, value in presets:
            button = Gtk.Button(label=label)
            button.connect("clicked", self.on_preset_clicked, value)
            preset_box.pack_start(button, False, False, 0)
        
        vbox.pack_start(preset_box, False, False, 0)
        
        # Status label
        self.status_label = Gtk.Label()
        self.status_label.set_text("Ready")
        vbox.pack_start(self.status_label, False, False, 0)
        
        # Instructions
        instructions = Gtk.Label()
        instructions.set_markup("<small><i>Tip: If the app asks for password, it's normal for brightness control.</i></small>")
        instructions.set_line_wrap(True)
        vbox.pack_start(instructions, False, False, 0)
        
        self.window.add(vbox)
        
    def update_current_brightness(self):
        """Update the current brightness display"""
        current = self.get_current_brightness()
        self.brightness_scale.set_value(current)
        self.percentage_label.set_text(f"{current}%")
        
        if self.brightness_path:
            device_name = os.path.basename(self.brightness_path)
            if "nvidia" in device_name.lower():
                self.info_label.set_text(f"Using NVIDIA backlight: {device_name}")
            elif "intel" in device_name.lower():
                self.info_label.set_text(f"Using Intel backlight: {device_name}")
            else:
                self.info_label.set_text(f"Using backlight: {device_name}")
        else:
            self.info_label.set_text("Using xrandr (software brightness)")
        
    def on_brightness_changed(self, scale):
        """Handle brightness slider changes"""
        value = int(scale.get_value())
        self.percentage_label.set_text(f"{value}%")
        
        # Update brightness
        success = self.set_brightness(value)
        
        if success:
            self.status_label.set_text("Brightness updated successfully")
        else:
            self.status_label.set_text("Failed to update brightness")
            
    def on_preset_clicked(self, button, value):
        """Handle preset button clicks"""
        self.brightness_scale.set_value(value)
        
    def run(self):
        """Run the application"""
        self.window.show_all()
        Gtk.main()

def check_dependencies():
    """Check if required tools are available"""
    print("Checking brightness control methods...")
    
    # Check for brightness control paths
    backlight_dirs = glob.glob("/sys/class/backlight/*")
    if backlight_dirs:
        print(f"✓ Found hardware brightness controls: {[os.path.basename(d) for d in backlight_dirs]}")
    else:
        print("! No hardware brightness controls found")
    
    # Check for xrandr
    try:
        subprocess.run(['xrandr', '--version'], capture_output=True, check=True)
        print("✓ xrandr available (software brightness)")
    except:
        print("! xrandr not available")
    
    # Check for brightnessctl
    try:
        subprocess.run(['brightnessctl', '--version'], capture_output=True, check=True)
        print("✓ brightnessctl available")
    except:
        print("! brightnessctl not available (optional)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        check_dependencies()
        sys.exit(0)
        
    try:
        app = BrightnessController()
        app.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        print("\nTrying to install missing dependencies...")
        print("Run: sudo apt install python3-gi gir1.2-gtk-3.0")