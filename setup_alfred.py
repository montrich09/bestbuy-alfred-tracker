#!/usr/bin/env python3
"""
Setup script for Alfred Search Box
This script installs the desktop entry and sets up keyboard shortcuts
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def get_desktop_path():
    """Get the user's desktop directory"""
    home = os.path.expanduser("~")
    desktop_paths = [
        os.path.join(home, "Desktop"),
        os.path.join(home, ".local", "share", "applications"),
        "/usr/share/applications"
    ]
    
    for path in desktop_paths:
        if os.path.exists(path):
            return path
    return desktop_paths[1]  # Default to local applications

def install_desktop_entry():
    """Install the desktop entry file"""
    try:
        # Get current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        desktop_entry_src = os.path.join(current_dir, "alfred-search.desktop")
        
        # Get desktop directory
        desktop_dir = get_desktop_path()
        desktop_entry_dst = os.path.join(desktop_dir, "alfred-search.desktop")
        
        # Update the Exec path in the desktop entry
        with open(desktop_entry_src, 'r') as f:
            content = f.read()
        
        # Replace the Exec path with the actual path
        content = content.replace(
            "Exec=python3 /home/mont/Documents/Work/bestbuy-alfred-tracker/launch_alfred.py",
            f"Exec=python3 {os.path.join(current_dir, 'launch_alfred.py')}"
        )
        
        # Write the updated desktop entry
        with open(desktop_entry_dst, 'w') as f:
            f.write(content)
        
        # Make it executable
        os.chmod(desktop_entry_dst, 0o755)
        
        print(f"✅ Desktop entry installed to: {desktop_entry_dst}")
        return True
        
    except Exception as e:
        print(f"❌ Error installing desktop entry: {e}")
        return False

def setup_keyboard_shortcut():
    """Set up keyboard shortcut using gsettings (GNOME)"""
    try:
        # Try to set up keyboard shortcut for GNOME
        cmd = [
            "gsettings", "set", "org.gnome.desktop.keybindings", 
            "custom-keybindings", "['/org/gnome/desktop/keybindings/custom0/']"
        ]
        subprocess.run(cmd, check=True)
        
        cmd = [
            "gsettings", "set", "org.gnome.desktop.keybindings.custom0", 
            "name", "Alfred Search Box"
        ]
        subprocess.run(cmd, check=True)
        
        cmd = [
            "gsettings", "set", "org.gnome.desktop.keybindings.custom0", 
            "command", f"python3 {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'launch_alfred.py')}"
        ]
        subprocess.run(cmd, check=True)
        
        cmd = [
            "gsettings", "set", "org.gnome.desktop.keybindings.custom0", 
            "binding", "<Super>space"
        ]
        subprocess.run(cmd, check=True)
        
        print("✅ Keyboard shortcut set to Super+Space")
        print("   You can change this in Settings > Keyboard > Custom Shortcuts")
        return True
        
    except subprocess.CalledProcessError:
        print("⚠️  Could not set keyboard shortcut automatically")
        print("   Please set it manually in your system settings:")
        print("   - Open Settings > Keyboard > Custom Shortcuts")
        print("   - Add new shortcut")
        print("   - Name: Alfred Search Box")
        print(f"   - Command: python3 {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'launch_alfred.py')}")
        print("   - Suggested shortcut: Super+Space")
        return False
    except Exception as e:
        print(f"❌ Error setting keyboard shortcut: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import tkinter
        print("✅ Tkinter is available")
        return True
    except ImportError:
        print("❌ Tkinter is not available")
        print("   Install it with: sudo apt-get install python3-tk")
        return False

def main():
    print("🚀 Setting up Alfred Search Box...")
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Install desktop entry
    if install_desktop_entry():
        print()
        
        # Set up keyboard shortcut
        setup_keyboard_shortcut()
        
        print()
        print("🎉 Setup complete!")
        print()
        print("Usage:")
        print("  • Run from terminal: python3 launch_alfred.py")
        print("  • Run from desktop: Double-click alfred-search.desktop")
        print("  • Use keyboard shortcut: Super+Space (if set)")
        print()
        print("Features:")
        print("  • Web searches (Google, YouTube, GitHub, etc.)")
        print("  • Application launcher (Calculator, Terminal, etc.)")
        print("  • File search")
        print("  • Price checking (integrated with your BestBuy tracker)")
        print("  • Weather and time queries")
        print()
        print("Keyboard shortcuts:")
        print("  • Enter: Execute command")
        print("  • Escape: Hide window")
        print("  • Ctrl+Q: Quit")
        print("  • Ctrl+H: Show help")
        print("  • Up/Down: Navigate history")
        
    else:
        print("❌ Setup failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 