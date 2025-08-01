import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import webbrowser
import os
import json
from datetime import datetime
import threading
import queue

class AlfredSearchBox:
    def __init__(self, root):
        self.root = root
        self.root.title("Alfred Search Box")
        self.root.geometry("600x400")
        self.root.configure(bg='#2c2c2c')
        
        # Make window always on top
        self.root.attributes('-topmost', True)
        
        # Center the window
        self.center_window()
        
        # Search history
        self.search_history = []
        self.history_index = -1
        
        # Commands database
        self.commands = {
            'google': 'Search Google',
            'youtube': 'Search YouTube',
            'github': 'Search GitHub',
            'stackoverflow': 'Search Stack Overflow',
            'amazon': 'Search Amazon',
            'bestbuy': 'Search Best Buy',
            'calculator': 'Open Calculator',
            'notepad': 'Open Notepad',
            'terminal': 'Open Terminal',
            'file': 'Search Files',
            'web': 'Open Website',
            'price': 'Check Product Price',
            'weather': 'Check Weather',
            'time': 'Show Current Time',
            'date': 'Show Current Date',
            'help': 'Show Help'
        }
        
        self.setup_ui()
        self.bind_shortcuts()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"600x400+{x}+{y}")
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c2c2c')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Alfred Search", 
                              font=('Arial', 16, 'bold'), 
                              fg='#ffffff', bg='#2c2c2c')
        title_label.pack(pady=(0, 20))
        
        # Search frame
        search_frame = tk.Frame(main_frame, bg='#2c2c2c')
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, 
                                   textvariable=self.search_var,
                                   font=('Arial', 14),
                                   bg='#3c3c3c',
                                   fg='#ffffff',
                                   insertbackground='#ffffff',
                                   relief=tk.FLAT,
                                   bd=10)
        self.search_entry.pack(fill=tk.X, ipady=10)
        self.search_entry.focus()
        
        # Bind search events
        self.search_var.trace('w', self.on_search_change)
        self.search_entry.bind('<Return>', self.execute_search)
        self.search_entry.bind('<Up>', self.navigate_history_up)
        self.search_entry.bind('<Down>', self.navigate_history_down)
        
        # Results frame
        results_frame = tk.Frame(main_frame, bg='#2c2c2c')
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results listbox
        self.results_listbox = tk.Listbox(results_frame,
                                        bg='#3c3c3c',
                                        fg='#ffffff',
                                        selectbackground='#007acc',
                                        selectforeground='#ffffff',
                                        font=('Arial', 12),
                                        relief=tk.FLAT,
                                        bd=5)
        self.results_listbox.pack(fill=tk.BOTH, expand=True)
        self.results_listbox.bind('<Double-Button-1>', self.on_result_select)
        self.results_listbox.bind('<Return>', self.on_result_select)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Type to search")
        status_label = tk.Label(main_frame, 
                              textvariable=self.status_var,
                              font=('Arial', 10),
                              fg='#888888', 
                              bg='#2c2c2c')
        status_label.pack(pady=(10, 0))
        
    def bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Escape>', self.hide_window)
        self.root.bind('<Control-q>', self.quit_app)
        self.root.bind('<Control-h>', self.show_help)
        
    def on_search_change(self, *args):
        """Handle search input changes"""
        query = self.search_var.get().strip().lower()
        
        if not query:
            self.clear_results()
            self.status_var.set("Ready - Type to search")
            return
            
        # Filter commands based on query
        filtered_commands = []
        for cmd, desc in self.commands.items():
            if query in cmd.lower() or query in desc.lower():
                filtered_commands.append((cmd, desc))
        
        # Update results
        self.update_results(filtered_commands)
        
        if filtered_commands:
            self.status_var.set(f"Found {len(filtered_commands)} results")
        else:
            self.status_var.set("No results found")
            
    def update_results(self, results):
        """Update the results listbox"""
        self.results_listbox.delete(0, tk.END)
        
        for cmd, desc in results:
            self.results_listbox.insert(tk.END, f"{cmd} - {desc}")
            
    def clear_results(self):
        """Clear the results listbox"""
        self.results_listbox.delete(0, tk.END)
        
    def execute_search(self, event=None):
        """Execute the selected search"""
        selection = self.results_listbox.curselection()
        if selection:
            selected_item = self.results_listbox.get(selection[0])
            command = selected_item.split(' - ')[0]
            self.execute_command(command)
        else:
            # Execute first result if available
            if self.results_listbox.size() > 0:
                first_item = self.results_listbox.get(0)
                command = first_item.split(' - ')[0]
                self.execute_command(command)
                
    def on_result_select(self, event=None):
        """Handle result selection"""
        self.execute_search()
        
    def execute_command(self, command):
        """Execute a command based on the search"""
        query = self.search_var.get().strip()
        
        # Add to history
        if query not in self.search_history:
            self.search_history.append(query)
        self.history_index = -1
        
        try:
            if command == 'google':
                webbrowser.open(f"https://www.google.com/search?q={query}")
                self.status_var.set(f"Searching Google for: {query}")
                
            elif command == 'youtube':
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                self.status_var.set(f"Searching YouTube for: {query}")
                
            elif command == 'github':
                webbrowser.open(f"https://github.com/search?q={query}")
                self.status_var.set(f"Searching GitHub for: {query}")
                
            elif command == 'stackoverflow':
                webbrowser.open(f"https://stackoverflow.com/search?q={query}")
                self.status_var.set(f"Searching Stack Overflow for: {query}")
                
            elif command == 'amazon':
                webbrowser.open(f"https://www.amazon.com/s?k={query}")
                self.status_var.set(f"Searching Amazon for: {query}")
                
            elif command == 'bestbuy':
                webbrowser.open(f"https://www.bestbuy.com/site/searchpage.jsp?st={query}")
                self.status_var.set(f"Searching Best Buy for: {query}")
                
            elif command == 'calculator':
                subprocess.Popen(['gnome-calculator'] if os.name == 'posix' else ['calc'])
                self.status_var.set("Opening Calculator")
                
            elif command == 'notepad':
                subprocess.Popen(['gedit'] if os.name == 'posix' else ['notepad'])
                self.status_var.set("Opening Text Editor")
                
            elif command == 'terminal':
                subprocess.Popen(['gnome-terminal'] if os.name == 'posix' else ['cmd'])
                self.status_var.set("Opening Terminal")
                
            elif command == 'file':
                # Open file manager with search
                if os.name == 'posix':
                    subprocess.Popen(['nautilus', '--search', query])
                else:
                    subprocess.Popen(['explorer', '/select,', query])
                self.status_var.set(f"Searching files for: {query}")
                
            elif command == 'web':
                if query.startswith(('http://', 'https://')):
                    webbrowser.open(query)
                else:
                    webbrowser.open(f"https://{query}")
                self.status_var.set(f"Opening website: {query}")
                
            elif command == 'price':
                # Use your existing price tracking functionality
                self.check_product_price(query)
                
            elif command == 'weather':
                webbrowser.open(f"https://www.google.com/search?q=weather+{query}")
                self.status_var.set(f"Checking weather for: {query}")
                
            elif command == 'time':
                current_time = datetime.now().strftime("%H:%M:%S")
                messagebox.showinfo("Current Time", f"Current time: {current_time}")
                self.status_var.set(f"Current time: {current_time}")
                
            elif command == 'date':
                current_date = datetime.now().strftime("%A, %B %d, %Y")
                messagebox.showinfo("Current Date", f"Current date: {current_date}")
                self.status_var.set(f"Current date: {current_date}")
                
            elif command == 'help':
                self.show_help()
                
            else:
                # Default to Google search
                webbrowser.open(f"https://www.google.com/search?q={query}")
                self.status_var.set(f"Searching Google for: {query}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error executing command: {str(e)}")
            self.status_var.set("Error executing command")
            
    def check_product_price(self, query):
        """Check product price using your existing functionality"""
        try:
            # Import your existing price checking functionality
            from main import get_product
            
            # For demonstration, we'll use a sample Best Buy URL
            sample_url = "https://www.bestbuy.com/site/samsung-galaxy-z-flip5-256gb-unlocked-graphite/6548838.p?skuId=6548838"
            
            def price_check_thread():
                try:
                    product = get_product(sample_url)
                    if product and product['price'] != "Price not available":
                        messagebox.showinfo("Product Price", 
                                          f"Product: {product['title']}\n"
                                          f"Price: {product['price']} {product['currency']}")
                        self.status_var.set(f"Price checked: {product['price']} {product['currency']}")
                    else:
                        messagebox.showwarning("Price Check", "Unable to retrieve price information")
                        self.status_var.set("Price check failed")
                except Exception as e:
                    messagebox.showerror("Error", f"Error checking price: {str(e)}")
                    self.status_var.set("Price check error")
            
            # Run price check in background thread
            thread = threading.Thread(target=price_check_thread)
            thread.daemon = True
            thread.start()
            
        except ImportError:
            messagebox.showinfo("Price Check", "Price checking functionality not available")
            self.status_var.set("Price checking not available")
            
    def navigate_history_up(self, event=None):
        """Navigate up in search history"""
        if self.search_history and self.history_index < len(self.search_history) - 1:
            self.history_index += 1
            self.search_var.set(self.search_history[-(self.history_index + 1)])
            self.search_entry.icursor(tk.END)
        return "break"
        
    def navigate_history_down(self, event=None):
        """Navigate down in search history"""
        if self.history_index > 0:
            self.history_index -= 1
            self.search_var.set(self.search_history[-(self.history_index + 1)])
            self.search_entry.icursor(tk.END)
        elif self.history_index == 0:
            self.history_index = -1
            self.search_var.set("")
        return "break"
        
    def show_help(self, event=None):
        """Show help dialog"""
        help_text = """
Alfred Search Box - Help

Keyboard Shortcuts:
• Enter: Execute selected command
• Escape: Hide window
• Ctrl+Q: Quit application
• Ctrl+H: Show this help
• Up/Down: Navigate search history

Available Commands:
• google: Search Google
• youtube: Search YouTube
• github: Search GitHub
• amazon: Search Amazon
• bestbuy: Search Best Buy
• calculator: Open Calculator
• notepad: Open Text Editor
• terminal: Open Terminal
• file: Search Files
• web: Open Website
• price: Check Product Price
• weather: Check Weather
• time: Show Current Time
• date: Show Current Date

Usage:
1. Type your search query
2. Select a command from the results
3. Press Enter or double-click to execute
        """
        messagebox.showinfo("Help", help_text)
        
    def hide_window(self, event=None):
        """Hide the window"""
        self.root.withdraw()
        
    def quit_app(self, event=None):
        """Quit the application"""
        self.root.quit()

def main():
    root = tk.Tk()
    app = AlfredSearchBox(root)
    root.mainloop()

if __name__ == "__main__":
    main() 