import paramiko
import time
import getpass
import socket
import os
import warnings
warnings.filterwarnings(action='ignore', module='.*paramiko.*')


# Function to read the commands from the .ttl file
def read_ttl_file(file_path):
    with open(file_path, 'r') as file:
        config_commands = file.readlines()
    return config_commands

# Function to send configuration commands via SSH
def send_config_to_sbc(ip, username, password, commands, delay=2, timeout=10):
    try:
        # Create an SSH client object
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown host keys

        print(f"Connecting to SBC at {ip}...")
        ssh.connect(ip, username=username, password=password, timeout=timeout)

        # Open an interactive shell
        shell = ssh.invoke_shell()
        time.sleep(1)  # Give the shell time to start

        # Send configuration commands
        for command in commands:
            command = command.strip()  # Clean up any extra whitespace
            if command:
                print(f"Sending command: {command}")
                shell.send(command + '\n')
                time.sleep(delay)  # Delay to ensure the command is processed properly
                output = shell.recv(65535).decode('utf-8')  # Receive the output
                print(output)  # Print output for monitoring/logging



        # Ask the user if they want to execute verify-config, save-config, and activate-config commands
        confirmation = input("\nDo you want to execute 'save-config', and 'activate-config' on this SBC? (yes/no): ").lower()
        if confirmation == 'yes':

            print("Sending 'save-config' command...")
            shell.send('save-config\n')
            time.sleep(delay)
            output = shell.recv(65535).decode('utf-8')
            print(output)

            print("Sending 'activate-config' command...")
            shell.send('activate-config\n')
            time.sleep(delay)
            output = shell.recv(65535).decode('utf-8')
            print(output)
        else:
            print("Skipping 'save-config', and 'activate-config' commands.")


    except (paramiko.SSHException, socket.timeout) as e:
        print(f"Error: Unable to connect to SBC at {ip}. Reason: {str(e)}")
    except socket.gaierror as e:
        print(f"DNS Error: Could not resolve {ip}. Please check the hostname or IP. Reason: {str(e)}")
    except Exception as e:
        print(f"Unexpected error occurred while connecting to {ip}: {str(e)}")

# Main function to handle multiple SBCs
def main():
    # Define the directory where TTL files are stored
    ttl_directory = '/home/www-root/scripts/your_scripts/location/'

    # Prompt user for action they want to take (activate config or fallback Config)
    print("\nACTIVATE or FALLBACK Config? Choose an option below:")
    print("1. Config_ACTIVATION")
    print("2. Config_FALLBACK")

    choice = input("Enter 1 or 2: ")

    # Automatically select the correct .ttl file based on user choice
    if choice == '1':
        ttl_file_path = os.path.join(ttl_directory, 'ACTIVATION.ttl')
        print("\nYou have selected: ACTIVATION.ttl")
    elif choice == '2':
        ttl_file_path = os.path.join(ttl_directory, 'FALLBACK.ttl')
        print("\nYou have selected: FALLBACK.ttl")
    else:
        print("Invalid choice. Exiting.")
        return

    # Read the TTL configuration file
    config_commands = read_ttl_file(ttl_file_path)

    # Display the commands and ask for confirmation
    print("\nThe following commands will be sent to the SBC:\n")
    for command in config_commands:
        print(command.strip())

    confirmation = input("\nDo you want to proceed with these commands? (yes/no): ").lower()
    if confirmation != 'yes':
        print("Operation aborted by user. Exiting.")
        return

    # Prompt user for SBC device names/IPs
    sbc_input = input("\nEnter SBC device names or IP addresses (separated by space or comma): ")

    # Split input into a list of IPs/hostnames
    sbc_ips = [sbc.strip() for sbc in sbc_input.replace(',', ' ').split()]

    # Prompt the user for credentials
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")  # Securely prompt for the password

    # Loop through each SBC and apply the configuration
    for sbc_ip in sbc_ips:
        send_config_to_sbc(sbc_ip, username, password, config_commands, delay=2, timeout=10)

# Run the script
if __name__ == "__main__":
    main()
