# BestBuy Alfred Tracker

A Python application to track product prices on BestBuy using the Oxylabs API, plus an Alfred-style search box for quick access to applications and web searches.

## Features

### 🛒 Price Tracking
- Tracks product prices over time
- Generates price history charts
- Detects price drops and alerts
- Stores historical data in JSON format

### 🔍 Alfred Search Box
- **Web Searches**: Google, YouTube, GitHub, Stack Overflow, Amazon, Best Buy
- **Application Launcher**: Calculator, Terminal, Text Editor
- **System Tools**: File search, Weather, Time, Date
- **Price Integration**: Check product prices using your existing tracker
- **Keyboard Shortcuts**: Quick access with customizable hotkeys

## Quick Start

**To start the Alfred Search Box immediately:**
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run setup (one-time)
python3 setup_alfred.py

# Start the app
python3 launch_alfred.py
```

## Setup

```bash
pip install -r requirements.txt
```

### 2. Configure Credentials

**Option A: Using Environment Variables (Recommended)**

Set your Oxylabs credentials as environment variables:

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

**⚠️ Security Notes:**
- Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore` to prevent accidental commits
- Use strong, unique passwords for your API credentials
- Consider using a secrets manager for production environments

### 3. Setup Alfred Search Box

Run the setup script to install the desktop entry and keyboard shortcuts:

```bash
python3 setup_alfred.py
```

This will:
- Install a desktop entry for easy launching
- Set up keyboard shortcut (Super+Space by default)
- Configure the application for quick access

### 4. Run the Applications

**Price Tracker:**
```bash
python3 main.py
```

**Alfred Search Box:**

**Method 1: Terminal Command (Recommended)**
```bash
python3 launch_alfred.py
```

**Method 2: Desktop Icon**
- Go to your Desktop
- Double-click the `alfred-search.desktop` icon

**Method 3: Direct Launch**
```bash
python3 alfred_search.py
```

**Method 4: Keyboard Shortcut (After Setup)**
- Press **Super+Space** (if you set up the keyboard shortcut manually)

**Manual Keyboard Shortcut Setup:**
1. Open System Settings
2. Go to Keyboard > Custom Shortcuts
3. Click "Add"
4. Fill in the details:
   - **Name**: `Alfred Search Box`
   - **Command**: `python3 /home/mont/Documents/Work/bestbuy-alfred-tracker/launch_alfred.py`
   - **Shortcut**: Press `Super+Space` (or your preferred key combination)

## Alfred Search Box Usage

### 🚀 Quick Start
1. Press **Super+Space** (or your custom shortcut)
2. Type your search query
3. Select a command from the results
4. Press **Enter** to execute

### 📋 Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `google` | Search Google | `google python tutorial` |
| `youtube` | Search YouTube | `youtube cooking recipes` |
| `github` | Search GitHub | `github machine learning` |
| `amazon` | Search Amazon | `amazon wireless headphones` |
| `bestbuy` | Search Best Buy | `bestbuy samsung phone` |
| `calculator` | Open Calculator | `calculator` |
| `terminal` | Open Terminal | `terminal` |
| `file` | Search Files | `file document.pdf` |
| `web` | Open Website | `web github.com` |
| `price` | Check Product Price | `price samsung phone` |
| `weather` | Check Weather | `weather new york` |
| `time` | Show Current Time | `time` |
| `date` | Show Current Date | `date` |

### ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Enter** | Execute selected command |
| **Escape** | Hide window |
| **Ctrl+Q** | Quit application |
| **Ctrl+H** | Show help |
| **Up/Down** | Navigate search history |

### 🎯 Advanced Features

- **Search History**: Navigate through previous searches
- **Smart Suggestions**: Commands are filtered as you type
- **Background Processing**: Price checks run in background threads
- **Error Handling**: Graceful handling of API errors
- **Cross-platform**: Works on Linux, Windows, and macOS

## Configuration

### Price Tracker Configuration
You can modify the `tracked_product_links` list in `main()` to add or remove products you want to track.

### Alfred Search Box Configuration
Edit the `commands` dictionary in `alfred_search.py` to add custom commands:

```python
self.commands = {
    'mycommand': 'My Custom Command',
    # Add your custom commands here
}
```

## File Structure

```
bestbuy-alfred-tracker/
├── main.py                 # Price tracking application
├── alfred_search.py        # Alfred search box GUI
├── launch_alfred.py        # Launcher script
├── setup_alfred.py         # Setup script
├── alfred-search.desktop   # Desktop entry
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── env.example            # Environment template
├── data.json              # Price tracking data
└── README.md              # This file
```

## Troubleshooting

### Alfred Search Box Issues

**App won't start:**
- Check if Tkinter is installed: `python3 -c "import tkinter"`
- Install if missing: `sudo apt-get install python3-tk`
- Ensure all dependencies are installed: `pip3 install -r requirements.txt`

**Window doesn't appear:**
- Check if Tkinter is installed: `python3 -c "import tkinter"`
- Install if missing: `sudo apt-get install python3-tk`
- Try running with verbose output: `python3 -v launch_alfred.py`

**Keyboard shortcut doesn't work:**
- Check system settings: Settings > Keyboard > Custom Shortcuts
- Verify the command path is correct
- Try a different shortcut key
- Test the command manually: `python3 launch_alfred.py`

**Desktop icon doesn't work:**
- Check if the desktop entry exists: `ls -la ~/Desktop/alfred-search.desktop`
- Make it executable: `chmod +x ~/Desktop/alfred-search.desktop`
- Verify the path in the desktop entry is correct

**Price checking fails:**
- Ensure your Oxylabs credentials are set correctly
- Check your internet connection
- Verify the API endpoint is accessible

### Price Tracker Issues

**Credentials not found:**
- Check that environment variables are set
- Verify `.env` file exists and has correct format
- Ensure `python-dotenv` is installed

**API errors:**
- Verify your Oxylabs credentials are valid
- Check your API usage limits
- Ensure the product URLs are accessible

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.