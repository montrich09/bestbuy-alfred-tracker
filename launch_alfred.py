#!/usr/bin/env python3
"""
Alfred Search Box Launcher
This script can be bound to a keyboard shortcut to show/hide the search box
"""

import tkinter as tk
import sys
import os
from alfred_search import AlfredSearchBox

class AlfredLauncher:
    def __init__(self):
        self.root = None
        self.app = None
        
    def show_search_box(self):
        """Show or create the search box"""
        if self.root is None or not self.root.winfo_exists():
            # Create new window
            self.root = tk.Tk()
            self.app = AlfredSearchBox(self.root)
            
            # Bind window close event
            self.root.protocol("WM_DELETE_WINDOW", self.hide_search_box)
            
            # Show window
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            
        else:
            # Show existing window
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            
    def hide_search_box(self):
        """Hide the search box"""
        if self.root and self.root.winfo_exists():
            self.root.withdraw()
            
    def toggle_search_box(self):
        """Toggle the search box visibility"""
        if self.root and self.root.winfo_exists() and self.root.state() != 'withdrawn':
            self.hide_search_box()
        else:
            self.show_search_box()

def main():
    launcher = AlfredLauncher()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "show":
            launcher.show_search_box()
        elif sys.argv[1] == "hide":
            launcher.hide_search_box()
        elif sys.argv[1] == "toggle":
            launcher.toggle_search_box()
        else:
            print("Usage: python3 launch_alfred.py [show|hide|toggle]")
            sys.exit(1)
    else:
        # Default: show the search box
        launcher.show_search_box()
    
    # Start the main loop
    if launcher.root:
        launcher.root.mainloop()

if __name__ == "__main__":
    main() 