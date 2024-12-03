import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3
import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import os

# Disable SSL certificate warnings
urllib3.disable_warnings()

class DnacAPI:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.token = None

    def get_auth_token(self):
        """Authenticate with DNA Center and get token"""
        url = f"https://{self.host}/dna/system/api/v1/auth/token"
        
        try:
            response = requests.post(
                url,
                auth=HTTPBasicAuth(self.username, self.password),
                verify=False
            )
            response.raise_for_status()
            self.token = response.json()["Token"]
            return self.token
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error getting auth token: {e}")

    def get_device_inventory(self):
        """Get list of all network devices"""
        if not self.token:
            self.get_auth_token()

        url = f"https://{self.host}/dna/intent/api/v1/network-device"
        headers = {
            "X-Auth-Token": self.token,
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error getting device inventory: {e}")

class DnacGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cisco DNA Center Inventory")
        self.root.geometry("800x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Connection details frame
        self.conn_frame = ttk.LabelFrame(self.main_frame, text="Connection Details", padding="5")
        self.conn_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Host input
        ttk.Label(self.conn_frame, text="Host:").grid(row=0, column=0, sticky=tk.W)
        self.host_var = tk.StringVar()
        self.host_entry = ttk.Entry(self.conn_frame, textvariable=self.host_var, width=40)
        self.host_entry.grid(row=0, column=1, padx=5)
        
        # Username input
        ttk.Label(self.conn_frame, text="Username:").grid(row=1, column=0, sticky=tk.W)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(self.conn_frame, textvariable=self.username_var, width=40)
        self.username_entry.grid(row=1, column=1, padx=5)
        
        # Password input
        ttk.Label(self.conn_frame, text="Password:").grid(row=2, column=0, sticky=tk.W)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.conn_frame, textvariable=self.password_var, show="*", width=40)
        self.password_entry.grid(row=2, column=1, padx=5)
        
        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.fetch_button = ttk.Button(self.button_frame, text="Fetch Inventory", command=self.fetch_inventory)
        self.fetch_button.grid(row=0, column=0, padx=5)
        
        self.export_button = ttk.Button(self.button_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_button.grid(row=0, column=1, padx=5)
        self.export_button.state(['disabled'])
        
        # Treeview for inventory
        self.tree = ttk.Treeview(self.main_frame, columns=("hostname", "ip", "platform", "version", "serial", "uptime"),
                                show="headings", height=20)
        
        # Define headings
        self.tree.heading("hostname", text="Hostname")
        self.tree.heading("ip", text="Management IP")
        self.tree.heading("platform", text="Platform ID")
        self.tree.heading("version", text="Software Version")
        self.tree.heading("serial", text="Serial Number")
        self.tree.heading("uptime", text="Up Time")
        
        # Column widths
        self.tree.column("hostname", width=120)
        self.tree.column("ip", width=120)
        self.tree.column("platform", width=120)
        self.tree.column("version", width=120)
        self.tree.column("serial", width=120)
        self.tree.column("uptime", width=120)
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Grid the treeview and scrollbar
        self.tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        
        self.devices = None

    def fetch_inventory(self):
        try:
            dnac = DnacAPI(self.host_var.get(), self.username_var.get(), self.password_var.get())
            self.devices = dnac.get_device_inventory()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add new items
            for device in self.devices:
                self.tree.insert("", tk.END, values=(
                    device.get('hostname'),
                    device.get('managementIpAddress'),
                    device.get('platformId'),
                    device.get('softwareVersion'),
                    device.get('serialNumber'),
                    device.get('upTime')
                ))
            
            self.export_button.state(['!disabled'])
            messagebox.showinfo("Success", "Inventory fetched successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_to_csv(self):
        if not self.devices:
            messagebox.showerror("Error", "No data to export!")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dna_inventory_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow(['Hostname', 'Management IP', 'Platform ID', 
                               'Software Version', 'Serial Number', 'Up Time'])
                
                # Write data
                for device in self.devices:
                    writer.writerow([
                        device.get('hostname'),
                        device.get('managementIpAddress'),
                        device.get('platformId'),
                        device.get('softwareVersion'),
                        device.get('serialNumber'),
                        device.get('upTime')
                    ])
            
            messagebox.showinfo("Success", f"Inventory exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV: {str(e)}")

def main():
    root = tk.Tk()
    app = DnacGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
