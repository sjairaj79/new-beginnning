# Oracle ACME Bulk Activation and Fallback Tool

A Python-based automation tool designed for configuring network devices such as SBCs (Session Border Controllers). 
This script simplifies the process of activating or rolling back configurations by automating SSH connections and executing commands from user-provided `.ttl` files.

---

## Features

- **Bulk Configuration**:
  - Supports activation (`ACTIVATION.ttl`) and fallback (`FALLBACK.ttl`) configurations.
  - Applies configuration commands to multiple devices in one session.
- **Interactive Workflow**:
  - Displays commands for user confirmation before execution.
  - Allows users to choose between activation or fallback configurations.
- **Secure Credentials**:
  - Prompts for credentials securely using `getpass`.
- **Post-Configuration Commands**:
  - Optionally runs `save-config` and `activate-config` commands after applying configurations.
- **Error Handling**:
  - Provides detailed feedback on SSH connection, DNS resolution, and execution issues.

---

## Infrastructure Setup

### **Infrastructure Layout**
1. **User PC/Laptop**:
   - Acts as the starting point to deploy and manage the script.
   - Requires network access to the Jump Server.

2. **Jump Server**:
   - **Requirements**:
     - Python installed with the `paramiko` library.
     - Network access to all target devices (e.g., SBCs).
   - **Purpose**:
     - Acts as a secure bridge between the user and the network resources.

3. **Network Resources**:
   - Devices like SBCs that allow SSH access from the Jump Server.

### **Infrastructure Diagram**


User PC/Laptop
       |
       v
Jump Server (Python Installed)
       |
       v
Network Resources (SBCs, etc.)


---

## Requirements

- **Python 3.x**
- **Dependencies**:
  - `paramiko` (for SSH connectivity)

Install dependencies with:
bash
pip install paramiko


---

## Directory Structure


/
├── oracle_acme_bulk_activation_fallback_SCRIPT.py  # Main script
├── ACTIVATION.ttl                                  # Activation commands
├── FALLBACK.ttl                                    # Fallback commands
└── README.md                                       # Documentation


---

## How to Use

1. **Prepare the Environment**:
   - Ensure Python 3.x and the required dependencies are installed.
   - Place the script and `.ttl` files in the same directory or update the file paths in the script.

2. **Run the Script**:
   bash
   python3 oracle_acme_bulk_activation_fallback_SCRIPT.py
   

3. **Follow the Prompts**:
   - Choose the configuration type:
     - `1` for Activation
     - `2` for Fallback
   - Review the configuration commands from the `.ttl` file.
   - Provide the list of device IPs or hostnames, separated by spaces or commas.
   - Enter your username and password when prompted.

4. **Monitor the Execution**:
   - The script will display the output of commands executed on each device.

---

## Example Interaction


ACTIVATE or FALLBACK Config? Choose an option below:
1. Config_ACTIVATION
2. Config_FALLBACK
Enter 1 or 2: 1

You have selected: ACTIVATION.ttl
The following commands will be sent to the SBC:

command1
command2
command3

Do you want to proceed with these commands? (yes/no): yes

Enter SBC device names or IP addresses (separated by space or comma): 192.168.1.1
Enter your username: admin
Enter your password: ******

Connecting to SBC at 192.168.1.1...
Sending command: command1
<Response from device>
...


---

## Error Handling

- **SSH Connection Issues**:
  - The script displays errors if the device is unreachable or SSH authentication fails.
- **Invalid Hostname/IP**:
  - DNS errors are reported with actionable feedback.
- **User Abort**:
  - Users can abort operations at any step by declining confirmation prompts.

---

## Logs

- The script prints the output from the SBCs in the terminal for real-time monitoring.
- Ensure logs are reviewed for any unexpected behavior during configuration.

---

## Limitations and Notes

- The script currently supports `.ttl` files formatted for Oracle ACME SBCs.
- For use with other devices, ensure `.ttl` files contain compatible commands.
- Cisco devices or other network equipment may require script modifications (e.g., replacing `save-config` with `write memory`).

---

## License

This project is licensed under the MIT License.

---

