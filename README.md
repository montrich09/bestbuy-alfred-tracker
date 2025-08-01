# Shopping App

A Python application for searching and tracking products from Best Buy with a modern interface.

## Features

### 🛒 Shopping App
- **Product Search**: Search Best Buy for products with real-time results
- **Product Lists**: Display search results with product cards
- **Product Details**: View price, rating, reviews, and availability
- **Product Tracking**: Monitor price changes over time
- **Browser Integration**: Open products directly in web browser

## Quick Start

**To start the Shopping App immediately:**
```bash
# Install dependencies
pip3 install -r requirements.txt

# Start the app
python3 shopping_app.py
```

## Setup

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Configure Credentials (Optional)

If you want to use price checking functionality, set up your Oxylabs credentials:

**Option A: Using Environment Variables**
```bash
export OXYLABS_USERNAME="your_username"
export OXYLABS_PASSWORD="your_password"
```

**Option B: Using .env File**
1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` and add your actual credentials:
   ```
   OXYLABS_USERNAME=your_actual_username
   OXYLABS_PASSWORD=your_actual_password
   ```

### 3. Run the Application

```bash
python3 shopping_app.py
```

## Shopping App Usage

### 🚀 Quick Start
1. Launch the shopping app: `python3 shopping_app.py`
2. **Search for products** by typing in the search box
3. Press **Enter** or click "Search Products"
4. View product cards with details and prices
5. Click "Track Price" to monitor price changes
6. Click "View Details" or "Open in Browser" to see more

### 📋 Search Features

| Feature | Description |
|---------|-------------|
| **Real-time Search** | Search as you type (3+ characters) |
| **Product Cards** | Visual display with icons and details |
| **Price Information** | Current prices and availability |
| **Rating & Reviews** | Product ratings and review counts |
| **Quick Actions** | View details, track price, open in browser |

### ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Enter** | Search products |
| **Ctrl+R** | Refresh search results |
| **Escape** | Hide window |
| **Ctrl+Q** | Quit application |
| **Ctrl+H** | Show help |

## File Structure

```
shopping-app/
├── shopping_app.py         # Main shopping application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── env.example            # Environment template
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── unused/                # Other development files
    ├── README.md          # Documentation of unused files
    ├── alfred_search.py   # Alfred search box
    ├── main.py            # Price tracking app
    ├── launch_alfred.py   # Alfred launcher
    ├── setup_alfred.py    # Setup script
    └── ...                # Other development files
```

## Troubleshooting

### Shopping App Issues

**App won't start:**
- Check if Tkinter is installed: `python3 -c "import tkinter"`
- Install if missing: `sudo apt-get install python3-tk`
- Ensure all dependencies are installed: `pip3 install -r requirements.txt`

**Window doesn't appear:**
- Check if Tkinter is installed: `python3 -c "import tkinter"`
- Install if missing: `sudo apt-get install python3-tk`
- Try running with verbose output: `python3 -v shopping_app.py`

**Search doesn't work:**
- Check your internet connection
- Verify the search query is at least 3 characters
- Try refreshing the search with Ctrl+R

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.