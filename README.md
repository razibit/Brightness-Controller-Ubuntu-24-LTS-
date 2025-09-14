# Brightness Controller for Ubuntu 24 LTS

**A simple app to fix brightness control when Ubuntu's default slider doesn't work**

Perfect for laptops with Intel i5-12500H + RTX 3050 and similar configurations.

---

## 🚀 Quick Start (For Beginners)

### Step 1: Install the App
1. Open Terminal (Ctrl + Alt + T)
2. Navigate to the app folder:
   ```bash
   cd /home/apostrophe/Downloads/Owmegle-linux
   ```
3. Run the installation script:
   ```bash
   bash install.sh
   ```
4. Enter your password when asked (this is normal)

### Step 2: Use the App
- **Method 1**: Search for "Brightness Controller" in Activities (Super key)
- **Method 2**: Double-click `brightness_controller.py` in file manager
- **Method 3**: Run in terminal: `python3 brightness_controller.py`

---

## 💡 How It Works

This app tries multiple methods to control your screen brightness:

1. **Hardware Control** (Best) - Direct access to backlight hardware
2. **Software Control** (Backup) - Uses xrandr to adjust display output
3. **BrightnessCtl** (Alternative) - Uses system brightness utility

### Why Your Default Slider Doesn't Work
Common reasons on laptops like yours:
- Intel/NVIDIA hybrid graphics confusion
- Missing graphics drivers
- Ubuntu not detecting the correct backlight device
- ACPI brightness control issues

---

## 🛠️ Features

- **Simple slider interface** - Easy to use, just like Windows
- **Preset buttons** - Quick access to 25%, 50%, 75%, 100%
- **Real-time control** - Changes brightness immediately
- **Multiple methods** - Tries different ways to control brightness
- **No root required** - Works without administrator privileges
- **Auto-detection** - Finds the right brightness control for your laptop

---

## 🔧 Troubleshooting

### The app asks for my password
- This is normal for hardware brightness control
- The install script tries to reduce this by setting up permissions
- You may need to log out and back in after installation

### Brightness resets when I reboot
- This happens with software brightness (xrandr method)
- Hardware brightness control remembers settings after reboot
- If you only have software brightness, run the app after each boot

### No brightness change at all
1. Check what methods are available:
   ```bash
   python3 brightness_controller.py --check
   ```
2. Try manual brightness control:
   ```bash
   # List available backlight devices
   ls /sys/class/backlight/
   
   # Try brightnessctl (if installed)
   brightnessctl set 50%
   ```

### App won't start
1. Install missing dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
   ```

2. Check for errors:
   ```bash
   python3 brightness_controller.py
   ```

---

## 🖥️ Technical Details

### Your Hardware (i5-12500H + RTX 3050)
- **NVIDIA WMI EC backlight**: Usually `/sys/class/backlight/nvidia_wmi_ec_backlight` (most common)
- **Intel integrated graphics**: Usually `/sys/class/backlight/intel_backlight`
- **NVIDIA discrete**: Usually doesn't control laptop screen brightness
- **Display output**: Likely connected to Intel graphics or NVIDIA WMI

### Brightness Control Methods Used
1. **Direct file writing**: `/sys/class/backlight/*/brightness` (prioritizes NVIDIA WMI EC)
2. **xrandr**: Software-based brightness adjustment
3. **brightnessctl**: System utility for backlight control

### File Locations
- App: `/home/apostrophe/Downloads/Owmegle-linux/brightness_controller.py`
- Desktop entry: `~/.local/share/applications/brightness-controller.desktop`
- Permissions rule: `/etc/udev/rules.d/90-brightness.rules`

---

## 📝 Manual Installation (Alternative)

If the automatic installer doesn't work:

1. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 brightnessctl
   ```

2. **Make executable**:
   ```bash
   chmod +x brightness_controller.py
   ```

3. **Copy desktop entry**:
   ```bash
   cp brightness-controller.desktop ~/.local/share/applications/
   update-desktop-database ~/.local/share/applications/
   ```

4. **Set up permissions** (optional):
   ```bash
   sudo usermod -a -G video $USER
   # Then log out and back in
   ```

---

## ❓ FAQ

**Q: Is this safe to use?**
A: Yes, it only controls brightness using standard Linux methods.

**Q: Will this affect my NVIDIA graphics?**
A: No, this controls display brightness, not GPU performance.

**Q: Can I uninstall it?**
A: Yes, just delete the files and remove the desktop entry:
```bash
rm ~/.local/share/applications/brightness-controller.desktop
rm -rf /home/apostrophe/Downloads/Owmegle-linux
```

**Q: Why don't you just fix Ubuntu's brightness slider?**
A: Ubuntu's brightness issues often require driver updates or system changes. This app provides a working solution without modifying system files.

---

## 🆘 Getting Help

If you need help:

1. **Check system compatibility**:
   ```bash
   python3 brightness_controller.py --check
   ```

2. **View available brightness controls**:
   ```bash
   ls -la /sys/class/backlight/
   ```

3. **Test brightness manually**:
   ```bash
   # Check current brightness
   cat /sys/class/backlight/*/brightness
   cat /sys/class/backlight/*/max_brightness
   ```

---

**Made for Ubuntu 24 LTS newcomers** 🐧
*Simple brightness control when the default doesn't work*