import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import webbrowser
import os
import json
from datetime import datetime
import threading
from urllib.parse import urlparse, parse_qs
import re
# Removed PIL imports to avoid dependency issues

def get_product(link):
    """
    Fetch product data from Oxylabs API for a given product link.
    Returns a dict with title, price, currency, and optionally more.
    """
    USERNAME = os.getenv('OXYLABS_USERNAME')
    PASSWORD = os.getenv('OXYLABS_PASSWORD')
    if not USERNAME or not PASSWORD:
        raise ValueError("OXYLABS_USERNAME and OXYLABS_PASSWORD environment variables must be set")

    payload = {
        'source': 'universal_ecommerce',
        'url': link,
        'geo_location': 'United States',
        'parse': True,
    }

    response = requests.post(
        'https://realtime.oxylabs.io/v1/queries',
        auth=(USERNAME, PASSWORD),
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    response_json = response.json()

    # Parse the response
    try:
        content = response_json["results"][0]["content"]
        product = {
            "title": content.get("title", "N/A"),
            "price": content.get("price", {}).get("price", "N/A"),
            "currency": content.get("price", {}).get("currency", "N/A"),
            "url": link,
            "rating": content.get("rating", "N/A"),
            "availability": "In Stock" if not content.get("is_sold_out") else "Sold Out",
            "reviews": content.get("additional_information", {}).get("reviews", "N/A"),
        }
        return product
    except Exception as e:
        raise RuntimeError(f"Failed to parse Oxylabs response: {e}\nRaw response: {response_json}")

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class ShoppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping App - Product Tracker")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c2c2c')
        
        # Make window always on top
        self.root.attributes('-topmost', True)
        
        # Center the window
        self.center_window()
        
        # Product data storage
        self.current_product = None
        self.product_history = []
        self.search_results = []
        
        # Commands database
        self.commands = {
            'bestbuy': 'Best Buy Product',
            'amazon': 'Amazon Product',
            'walmart': 'Walmart Product',
            'target': 'Target Product',
            'newegg': 'Newegg Product',
            'price': 'Check Price',
            'track': 'Track Product',
            'history': 'View History',
            'compare': 'Compare Prices',
            'alerts': 'Price Alerts',
            'help': 'Show Help'
        }
        
        self.setup_ui()
        self.bind_shortcuts()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1000x700+{x}+{y}")
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c2c2c')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Shopping App", 
                              font=('Arial', 18, 'bold'), 
                              fg='#ffffff', bg='#2c2c2c')
        title_label.pack(pady=(0, 20))
        
        # Search frame
        search_frame = tk.Frame(main_frame, bg='#2c2c2c')
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search label
        search_label = tk.Label(search_frame, text="Search Products:", 
                              font=('Arial', 12, 'bold'),
                              fg='#ffffff', bg='#2c2c2c')
        search_label.pack(anchor='w', pady=(0, 5))
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, 
                                   textvariable=self.search_var,
                                   font=('Arial', 12),
                                   bg='#3c3c3c',
                                   fg='#ffffff',
                                   insertbackground='#ffffff',
                                   relief=tk.FLAT,
                                   bd=10)
        self.search_entry.pack(fill=tk.X, ipady=8)
        self.search_entry.focus()
        
        # Bind search events
        self.search_var.trace('w', self.on_search_change)
        self.search_entry.bind('<Return>', self.search_products)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#2c2c2c')
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Search button
        self.search_btn = tk.Button(buttons_frame, 
                                  text="Search Products", 
                                  command=self.search_products,
                                  font=('Arial', 12, 'bold'),
                                  bg='#007acc',
                                  fg='#ffffff',
                                  relief=tk.FLAT,
                                  bd=0,
                                  padx=20,
                                  pady=8)
        self.search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Search results frame
        self.search_frame = tk.Frame(main_frame, bg='#2c2c2c')
        self.search_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Setup search results display
        self.setup_search_results()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Search for products")
        status_label = tk.Label(main_frame, 
                              textvariable=self.status_var,
                              font=('Arial', 10),
                              fg='#888888', 
                              bg='#2c2c2c')
        status_label.pack(pady=(10, 0))
        
    def setup_search_results(self):
        """Setup search results display"""
        # Search results label
        self.search_label = tk.Label(self.search_frame, 
                                   text="Search for products to see results here",
                                   font=('Arial', 14, 'bold'),
                                   fg='#ffffff', 
                                   bg='#2c2c2c')
        self.search_label.pack(pady=(20, 10))
        
        # Create canvas and scrollbar for search results
        self.search_canvas = tk.Canvas(self.search_frame, bg='#2c2c2c', highlightthickness=0)
        self.search_scrollbar = tk.Scrollbar(self.search_frame, orient="vertical", command=self.search_canvas.yview)
        self.search_scrollable_frame = tk.Frame(self.search_canvas, bg='#2c2c2c')
        
        self.search_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.search_canvas.configure(scrollregion=self.search_canvas.bbox("all"))
        )
        
        self.search_canvas.create_window((0, 0), window=self.search_scrollable_frame, anchor="nw")
        self.search_canvas.configure(yscrollcommand=self.search_scrollbar.set)
        
        self.search_canvas.pack(side="left", fill="both", expand=True)
        self.search_scrollbar.pack(side="right", fill="y")
        

        
    def bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Escape>', self.hide_window)
        self.root.bind('<Control-q>', self.quit_app)
        self.root.bind('<Control-h>', self.show_help)
        self.root.bind('<Control-r>', self.refresh_product)
        
    def on_search_change(self, *args):
        """Handle search input changes"""
        query = self.search_var.get().strip()
        
        if len(query) >= 3:  # Search after 3 characters
            self.search_products()
        elif len(query) == 0:
            self.clear_search_results()
            
    def search_products(self, event=None):
        """Search for products on Best Buy"""
        query = self.search_var.get().strip()
        
        if not query:
            return
            
        self.status_var.set(f"Searching Best Buy for: {query}")
        
        def search_thread():
            try:
                # Use Best Buy search API or web scraping
                results = self.search_bestbuy(query)
                self.display_search_results(results)
                self.status_var.set(f"Found {len(results)} products")
            except Exception as e:
                self.status_var.set(f"Search error: {str(e)}")
                messagebox.showerror("Search Error", f"Failed to search: {str(e)}")
                
        # Run search in background thread
        thread = threading.Thread(target=search_thread)
        thread.daemon = True
        thread.start()
        
    def search_bestbuy(self, query):
        """
        Search Best Buy for products using Oxylabs API.
        For demo, uses a few sample links. In production, you would scrape or use a real search API.
        """
        # Example product links (replace with real search results if you have a way to get them)
        product_links = [
            "https://www.bestbuy.com/site/samsung-galaxy-z-flip5-256gb-unlocked-graphite/6548838.p?skuId=6548838",
            "https://www.bestbuy.com/site/apple-iphone-15-pro-128gb-blue-titanium-verizon/6467420.p?skuId=6467420",
            "https://www.bestbuy.com/site/google-pixel-8-128gb-unlocked-obsidian/6536482.p?skuId=6536482"
        ]
        results = []
        for link in product_links:
            try:
                product = get_product(link)
                results.append(product)
            except Exception as e:
                print(f"Error fetching product for {link}: {e}")
        return results
            
    def display_search_results(self, results):
        """Display search results in a product list format"""
        # Clear previous results
        for widget in self.search_scrollable_frame.winfo_children():
            widget.destroy()
            
        if not results:
            no_results_label = tk.Label(self.search_scrollable_frame,
                                      text="No products found",
                                      font=('Arial', 12),
                                      fg='#888888',
                                      bg='#2c2c2c')
            no_results_label.pack(pady=20)
            return
            
        # Display each product
        for i, product in enumerate(results):
            self.create_product_card(product, i)
            
    def create_product_card(self, product, index):
        """Create a product card widget"""
        # Product card frame
        card_frame = tk.Frame(self.search_scrollable_frame,
                            bg='#3c3c3c',
                            relief=tk.RAISED,
                            bd=2)
        card_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Product image (placeholder)
        try:
            # In a real app, you'd load the actual image
            image_label = tk.Label(card_frame,
                                 text="📱",
                                 font=('Arial', 48),
                                 fg='#ffffff',
                                 bg='#3c3c3c')
            image_label.pack(side=tk.LEFT, padx=10, pady=10)
        except:
            # Fallback to text
            image_label = tk.Label(card_frame,
                                 text="📱",
                                 font=('Arial', 48),
                                 fg='#ffffff',
                                 bg='#3c3c3c')
            image_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Product info frame
        info_frame = tk.Frame(card_frame, bg='#3c3c3c')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Product title
        title_label = tk.Label(info_frame,
                             text=product['title'],
                             font=('Arial', 14, 'bold'),
                             fg='#ffffff',
                             bg='#3c3c3c',
                             anchor='w')
        title_label.pack(anchor='w', pady=(5, 2))
        
        # Price
        price_label = tk.Label(info_frame,
                             text=f"${product['price']} {product['currency']}",
                             font=('Arial', 16, 'bold'),
                             fg='#28a745',
                             bg='#3c3c3c',
                             anchor='w')
        price_label.pack(anchor='w', pady=(0, 2))
        
        # Rating and reviews
        rating_text = f"⭐ {product['rating']} ({product['reviews']} reviews)"
        rating_label = tk.Label(info_frame,
                              text=rating_text,
                              font=('Arial', 10),
                              fg='#ffc107',
                              bg='#3c3c3c',
                              anchor='w')
        rating_label.pack(anchor='w', pady=(0, 2))
        
        # Availability
        availability_label = tk.Label(info_frame,
                                   text=f"📦 {product['availability']}",
                                   font=('Arial', 10),
                                   fg='#17a2b8',
                                   bg='#3c3c3c',
                                   anchor='w')
        availability_label.pack(anchor='w', pady=(0, 5))
        
        # Buttons frame
        buttons_frame = tk.Frame(info_frame, bg='#3c3c3c')
        buttons_frame.pack(anchor='w')
        
        # View Details button
        view_btn = tk.Button(buttons_frame,
                           text="View Details",
                           command=lambda p=product: self.view_product_details(p),
                           font=('Arial', 10),
                           bg='#007acc',
                           fg='#ffffff',
                           relief=tk.FLAT,
                           bd=0,
                           padx=15,
                           pady=5)
        view_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Track Product button
        track_btn = tk.Button(buttons_frame,
                            text="Track Price",
                            command=lambda p=product: self.track_product_from_search(p),
                            font=('Arial', 10),
                            bg='#28a745',
                            fg='#ffffff',
                            relief=tk.FLAT,
                            bd=0,
                            padx=15,
                            pady=5)
        track_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Open in Browser button
        browser_btn = tk.Button(buttons_frame,
                              text="Open in Browser",
                              command=lambda p=product: self.open_product_in_browser(p),
                              font=('Arial', 10),
                              bg='#ffc107',
                              fg='#000000',
                              relief=tk.FLAT,
                              bd=0,
                              padx=15,
                              pady=5)
        browser_btn.pack(side=tk.LEFT)
        
    def view_product_details(self, product):
        """View detailed product information"""
        self.current_product = product
        # Open product in browser
        webbrowser.open(product['url'])
        self.status_var.set("Opened product in browser")
        
    def track_product_from_search(self, product):
        """Track a product from search results"""
        # Add to history
        if product not in self.product_history:
            self.product_history.append(product.copy())
            
        # Save to file
        self.save_tracked_products()
        
        messagebox.showinfo("Product Tracked", 
                          f"Now tracking: {product['title']}\n"
                          f"Price: {product['price']} {product['currency']}")
        
        self.status_var.set(f"Product tracked: {product['title']}")
        
    def open_product_in_browser(self, product):
        """Open product URL in browser"""
        webbrowser.open(product['url'])
        self.status_var.set("Opened in browser")
        
    def clear_search_results(self):
        """Clear search results"""
        for widget in self.search_scrollable_frame.winfo_children():
            widget.destroy()
            
        self.search_label.config(text="Search for products to see results here")
        

        
    def refresh_product(self, event=None):
        """Refresh search results"""
        if self.search_var.get().strip():
            self.search_products()
        return "break"
        
    def save_tracked_products(self):
        """Save tracked products to file"""
        try:
            with open('tracked_products.json', 'w') as f:
                json.dump(self.product_history, f, indent=2)
        except Exception as e:
            print(f"Error saving tracked products: {e}")
            
    def load_tracked_products(self):
        """Load tracked products from file"""
        try:
            if os.path.exists('tracked_products.json'):
                with open('tracked_products.json', 'r') as f:
                    self.product_history = json.load(f)
        except Exception as e:
            print(f"Error loading tracked products: {e}")
            
    def show_help(self, event=None):
        """Show help dialog"""
        help_text = """
Shopping App - Help

Keyboard Shortcuts:
• Enter: Search products
• Ctrl+R: Refresh search results
• Escape: Hide window
• Ctrl+Q: Quit application
• Ctrl+H: Show this help

Search Features:
• Type in search box to find products
• Real-time search results from Best Buy
• Product cards with details and prices
• Price, rating, and availability info

Features:
• Product search and discovery
• Product tracking and monitoring
• Browser integration
• Product history

Usage:
1. Type in the search box to find products
2. View product cards with details
3. Click "View Details" to open in browser
4. Click "Track Price" to monitor price changes
5. Click "Open in Browser" to view product page
        """
        messagebox.showinfo("Help", help_text)
        
    def hide_window(self, event=None):
        """Hide the window"""
        self.root.withdraw()
        
    def quit_app(self, event=None):
        """Quit the application"""
        self.save_tracked_products()
        self.root.quit()

def main():
    root = tk.Tk()
    app = ShoppingApp(root)
    
    # Load tracked products
    app.load_tracked_products()
    
    root.mainloop()

if __name__ == "__main__":
    main() 