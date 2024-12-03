# Cisco DNA Center Device Inventory Script

This script provides a GUI interface to interact with Cisco DNA Center's API and retrieve device inventory information. The inventory can be viewed in the application and exported to CSV.

## Prerequisites

- Python 3.6 or higher
- Access to a Cisco DNA Center instance
- API credentials (username and password)

### macOS Users
For better experience on macOS, additional package is required:
```bash
pip install tkmacosx
```
This package improves button appearance and handling on macOS.

## Installation

1. Clone or download this repository
2. Install required packages using pip:
pip install -r requirements.txt
Note: tkinter comes pre-installed with Python, so it's not included in requirements.txt.

## Features

- User-friendly GUI interface
- Secure password entry
- Real-time inventory display in a table format
- Export functionality to CSV with timestamp
- Error handling with user-friendly messages

## Usage

1. Run the script:
python main.py
2. Enter your DNA Center details in the provided fields.
3. Click the "Get Inventory" button to fetch and display the device inventory.
4. Use the "Export to CSV" button to save the inventory data to a file.

2. In the GUI:
   - Enter your DNA Center hostname/IP
   - Enter your username
   - Enter your password
   - Click "Fetch Inventory" to retrieve the device list
   - Click "Export to CSV" to save the inventory to a file

The exported CSV file will be named `dna_inventory_YYYYMMDD_HHMMSS.csv` and will contain the following information for each device:
- Hostname
- Management IP
- Platform ID
- Software Version
- Serial Number
- Up Time

## Security Note

The script currently disables SSL verification. In a production environment, you should:
1. Enable SSL verification
2. Use environment variables or a secure configuration file for credentials
3. Implement proper error handling and logging

## API Documentation

For more information about Cisco DNA Center API, visit:
https://developer.cisco.com/docs/dna-center/
The requirements.txt file includes:
requests: For making HTTP requests to the DNA Center API
urllib3: Required by requests and used for SSL warning suppression
I didn't include tkinter in requirements.txt because:
