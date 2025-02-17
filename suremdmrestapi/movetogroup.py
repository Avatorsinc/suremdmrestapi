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
        self.setWindowTitle("Device Relocation Tool")
        self.setGeometry(100, 100, 500, 400)

        self.lbl_store = QLabel("Enter Store ID (numbers only):")
        self.entry_store = QLineEdit()
        
        self.lbl_device = QLabel("Enter Device ID:")
        self.entry_device = QLineEdit()
        
        self.btn_assign = QPushButton("Assign Device")
        self.btn_assign.clicked.connect(self.assign_device)
        
        self.txt_output = QTextEdit()
        self.txt_output.setReadOnly(True)
        

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_store)
        layout.addWidget(self.entry_store)
        layout.addWidget(self.lbl_device)
        layout.addWidget(self.entry_device)
        layout.addWidget(self.btn_assign)
        layout.addWidget(self.txt_output)
        self.setLayout(layout)

        # Explicitly load the .env file from the current directory
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

        # Debugging the loaded environment variables
        #self.debug_env_vars()

        self.group_url = "https://salling.eu.suremdm.io/api/v2/group/082400110/getall"
        self.assignment_url = "https://salling.eu.suremdm.io/api/v2/deviceassignment"
        self.headers = {
            'ApiKey': "296A306B-B3BA-4719-9921-BA40CA5C690D",
            'Content-Type': "application/json",
        }
        

        self.email = os.getenv("MY_EMAIL")
        self.password = os.getenv("MY_PASSWORD")
        self.credentials = (self.email, self.password)

    def debug_env_vars(self):
        """Debug function to print environment variables."""
        print("Email:", os.getenv("MY_EMAIL"))
        print("Password:", os.getenv("MY_PASSWORD"))

    def append_output(self, message):
        """Append a line of text to the output text edit."""
        self.txt_output.append(message)

    def assign_device(self):
        """Fetch groups, match valid group, and assign device using API calls."""
        store_id = self.entry_store.text().strip()
        device_id = self.entry_device.text().strip()


        if not store_id or not device_id:
            QMessageBox.critical(self, "Input Error", "Both Store ID and Device ID are required!")
            return


        self.txt_output.clear()
        self.append_output("Fetching groups from API...")

        try:
            response = requests.get(
                self.group_url,
                auth=self.credentials,
                headers=self.headers,
                verify=False
            )
            response.raise_for_status()
            raw_data = response.json()

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

        valid_prefixes = [
            f"Home/PDA/DE/Netto/{store_id}",
            f"Home/PDA/PL/Netto/{store_id}",
            f"Home/PDA/DK/Netto/{store_id}",
            f"Home/PDA/DK/Bilka/{store_id}",
            f"Home/PDA/DK/BR/{store_id}",
            f"Home/PDA/DK/Carls Jr/{store_id}",
            f"Home/PDA/DK/Foetex/{store_id}",
            f"Home/PDA/DK/Salling/{store_id}",
            f"Home/PDA/DK/Salling Fashion Stores/{store_id}",
            f"Home/PDA/WH/{store_id}"
        ]

        self.append_output("Searching for matching group...")
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
        assignment_payload = [
            {
                "DeviceId": device_id,
                "GroupId": group_id
            }
        ]
        assignment_payload_json = json.dumps(assignment_payload)

        self.append_output("Sending device assignment request...")

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
    app = QApplication(sys.argv)
    window = DeviceAssignmentApp()
    window.show()
    sys.exit(app.exec())
