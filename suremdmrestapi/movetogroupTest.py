import os
import sys
import requests
import json
from dotenv import load_dotenv

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

class DeviceAssignmentApp(QWidget):
    def __init__(self):
        super().__init__()
        # Set window properties
        self.setWindowTitle("Device Relocation Tool")
        self.setGeometry(100, 100, 500, 400)

        # Create and configure widgets for store ID input
        # If you want to use a store identifier that is not strictly numeric (e.g., alphanumeric or codes),
        # change the label text and adjust any logic that depends on numeric formatting.
        self.lbl_store = QLabel("Enter Store ID (numbers only or your code):")
        self.entry_store = QLineEdit()
        
        # Create and configure widgets for device name input
        self.lbl_device = QLabel("Enter Device Name:")
        self.entry_device = QLineEdit()
        
        # Create a button that triggers device assignment
        self.btn_assign = QPushButton("Assign Device")
        self.btn_assign.clicked.connect(self.assign_device)
        
        # Create a text area to display output and log messages
        self.txt_output = QTextEdit()
        self.txt_output.setReadOnly(True)

        # Set up a vertical layout and add widgets to it
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_store)
        layout.addWidget(self.entry_store)
        layout.addWidget(self.lbl_device)
        layout.addWidget(self.entry_device)
        layout.addWidget(self.btn_assign)
        layout.addWidget(self.txt_output)
        self.setLayout(layout)

        # Load environment variables from a .env file located in the same directory as this script
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

        # API endpoint configuration:
        # Replace the URLs below with your public API endpoint details.
        self.group_url = "https://YOUR_API_ENDPOINT/api/v2/group/PLACEHOLDER/getall"  # URL for fetching group information
        self.assignment_url = "https://YOUR_API_ENDPOINT/api/v2/deviceassignment"      # URL for device assignment
        self.headers = {
            'ApiKey': "YOUR_API_KEY",  # Replace with your public API key
            'Content-Type': "application/json",
        }

        # Credentials loaded from the .env file (e.g., MY_EMAIL, MY_PASSWORD)
        self.email = os.getenv("MY_EMAIL")
        self.password = os.getenv("MY_PASSWORD")
        self.credentials = (self.email, self.password)

    def debug_env_vars(self):
        """
        Debug function to print environment variables.
        Use this for troubleshooting the loaded credentials.
        """
        print("Email:", os.getenv("MY_EMAIL"))
        print("Password:", os.getenv("MY_PASSWORD"))

    def append_output(self, message):
        """
        Append a line of text to the output text edit widget.
        Useful for logging progress and errors to the user.
        """
        self.txt_output.append(message)

    def get_device_id(self, device_name):
        """
        Fetch the device ID from the API based on the provided device name.
        Update the base URL or parameters if your API uses a different approach.
        """
        # Base API URL for device queries; replace with your endpoint as needed.
        baseurl = "https://YOUR_API_ENDPOINT/api"
        # Retrieve credentials and API key from environment variables.
        Username = os.getenv("MY_EMAIL")
        Password = os.getenv("MY_PASSWORD")
        ApiKey = os.getenv("API_KEY")  # Ensure API_KEY is set in your .env file
        url = baseurl + "/device"
        
        # Set up request headers using the API key.
        headers = {
            'ApiKey': ApiKey,
            'Content-Type': "application/json",
        }
        
        # Credentials tuple for basic authentication.
        credentials = (Username, Password)
        
        # JSON payload for the device search request.
        payload = {
            "ID": "AllDevices",
            "IsSearch": True,
            "Limit": 10,
            "SearchColumns": ["DeviceName"],
            "SearchValue": device_name,
            "SortColumn": "LastTimeStamp",
            "SortOrder": "asc"
        }

        try:
            response = requests.post(url, auth=credentials, json=payload, headers=headers, verify=False)
            
            if response.status_code == 200:
                if response.text != '[]':
                    data = response.json()
                    # Loop through the returned devices and match by device name
                    for device in data.get('rows', []):
                        if device.get('DeviceName') == device_name:
                            return device.get("DeviceID")
            else:
                self.append_output(f"Error: {response.status_code} - {response.text}")
                QMessageBox.critical(self, "API Error", f"Error fetching device ID: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            self.append_output(f"Error fetching device ID: {e}")
            QMessageBox.critical(self, "API Error", f"Error fetching device ID: {e}")
            return None

    def assign_device(self):
        """
        Main function to perform the device assignment.
        It validates input, fetches the device ID, retrieves group data,
        finds a matching group based on valid prefixes, and finally assigns the device.
        """
        store_id = self.entry_store.text().strip()  # This variable can be a numeric ID or any code
        device_name = self.entry_device.text().strip()

        # Validate that both store ID and device name are provided.
        if not store_id or not device_name:
            QMessageBox.critical(self, "Input Error", "Both Store ID and Device Name are required!")
            return

        # Clear previous output and start logging
        self.txt_output.clear()
        self.append_output("Fetching device ID...")

        device_id = self.get_device_id(device_name)

        if not device_id:
            err = f"No device found with name: {device_name}"
            self.append_output(err)
            QMessageBox.critical(self, "Device Not Found", err)
            return

        self.append_output(f"Found Device ID: {device_id} for Device Name: {device_name}")
        self.append_output("Fetching groups from API...")

        # Fetch group information using a GET request
        try:
            response = requests.get(
                self.group_url,
                auth=self.credentials,
                headers=self.headers,
                verify=False
            )
            response.raise_for_status()
            raw_data = response.json()

            # Validate that the expected 'data' key exists in the JSON response
            if isinstance(raw_data, dict) and "data" in raw_data:
                inner_data = raw_data["data"]
                if isinstance(inner_data, dict) and "Groups" in inner_data and isinstance(inner_data["Groups"], list):
                    groups_list = inner_data["Groups"]
                else:
                    err = "Unexpected data format in 'data'. Available keys: " + str(list(inner_data.keys()))
                    self.append_output(err)
                    QMessageBox.critical(self, "Data Format Error", err)
                    return
            else:
                err = "Unexpected API response format. 'data' key not found."
                self.append_output(err)
                QMessageBox.critical(self, "API Response Error", err)
                return

        except requests.exceptions.RequestException as e:
            err = "Error during group API request: " + str(e)
            self.append_output(err)
            QMessageBox.critical(self, "Request Error", err)
            return
        except json.JSONDecodeError as e:
            err = "Error: Group API response is not valid JSON: " + str(e)
            self.append_output(err)
            QMessageBox.critical(self, "JSON Error", err)
            return

        # Define valid group path prefixes.
        # The valid_prefixes are built using the store_id.
        # If your store identifier is not numeric or requires a different structure,
        # modify the strings below accordingly.
        valid_prefixes = [
            f"Home/PDA/DE/PLACEHOLDER/{store_id}",
            f"Home/PDA/PL/PLACEHOLDER/{store_id}",
            f"Home/PDA/DK/PLACEHOLDER/{store_id}",
            f"Home/PDA/DK/PLACEHOLDER/{store_id}",
            f"Home/PDA/DK/PLACEHOLDER/{store_id}",
            f"Home/PDA/DK/PLACEHOLDER/{store_id}",
            f"Home/PDA/DK/PLACEHOLDER/{store_id}",
            f"Home/PDA/DK/PLACEHOLDER/{store_id}",
            f"Home/PDA/DK/PLACEHOLDER/{store_id}",
            f"Home/PDA/WH/{store_id}"
        ]

        self.append_output("Searching for matching group...")
        # Find the first group that matches one of the valid prefixes
        matching_group = next(
            (
                group for group in groups_list
                if isinstance(group, dict) and any(group.get("GroupPath", "").startswith(prefix) for prefix in valid_prefixes)
            ),
            None
        )

        if not matching_group:
            err = f"No matching group found for Store ID: {store_id}"
            self.append_output(err)
            QMessageBox.critical(self, "Group Not Found", err)
            return

        group_id = matching_group.get("GroupID")
        success_msg = f"Found Group ID: {group_id} for Store ID: {store_id}"
        self.append_output(success_msg)
        
        # Prepare the JSON payload for the device assignment request
        assignment_payload = [
            {
                "DeviceId": device_id,
                "GroupId": group_id
            }
        ]
        assignment_payload_json = json.dumps(assignment_payload)

        self.append_output("Sending device assignment request...")

        # Send the device assignment request using a PUT method
        try:
            assign_response = requests.put(
                self.assignment_url,
                auth=self.credentials,
                data=assignment_payload_json,
                headers=self.headers,
                verify=False
            )
            assign_response.raise_for_status()
            result_msg = "Device assignment response: Device has been moved\n" + assign_response.text
            self.append_output(result_msg)
            QMessageBox.information(self, "Success", result_msg)
        except requests.exceptions.RequestException as e:
            err = "Error during device assignment request: " + str(e)
            self.append_output(err)
            QMessageBox.critical(self, "Assignment Error", err)

if __name__ == "__main__":
    # Initialize the Qt application
    app = QApplication(sys.argv)
    window = DeviceAssignmentApp()
    window.show()
    # Execute the application's main loop
    sys.exit(app.exec())
