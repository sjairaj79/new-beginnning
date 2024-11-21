#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paramiko
import os
import warnings
import smtplib
import time
from email.mime.text import MIMEText

warnings.filterwarnings(action='ignore', module='.*paramiko.*')

# List of nodes to connect to, You can use server names or IP Addresses 
nodes = ["XYZ105", "192.168.2.2"]

# Set threshold valu as you prefer, below example we use 60 percentage 
disk_threshold = 60
memory_threshold = 60
cpu_threshold = 60

# Commands used to monitor, Please verify this commands manually on you nodes you prefer to monitor.
disk_command = 'df'
memory_command = "free | grep Mem | awk '{print $3/$2 * 100.0}'"
cpu_command = "top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'"

# SSH credentials - Update your credentials
username = "admin"
password = "YourPassword"

# Loop through all nodes
for node in nodes:
    # SSH to the node
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(node, username=username, password=password)

    # Check disk usage
    stdin, stdout, stderr = ssh.exec_command(disk_command)
    data = stdout.read().decode()
    with open(f'{node}_disk.txt', 'w') as f:
        f.write(data)
    ssh.close()

    # Remove unwanted characters from file
    with open(f'{node}_disk.txt', 'r') as f:
        data = f.read().replace("Use%", "")
    with open(f'{node}_disk.txt', 'w') as f:
        f.write(data)

    # Check disk usage threshold
    with open(f'{node}_disk.txt', 'r') as f:
        for line in f:
            if '%' in line:
                usage = line.split()[4]
                if int(usage[:-1]) >= disk_threshold:
                    
                    # Send an email to the device owner
                    msg = MIMEText(f'{node} One of the DISK PARTITION USAGE above {disk_threshold}%\n\n' \
                                    f'COMMAND-->>  {disk_command}\n'\
                                    f'{data}\n'\
                                    'PLEASE TAKE APPROPRIATE ACTION')
                    msg['Subject'] = f'{node} One of the DISK PARTITION USAGE above {disk_threshold}%'
                    msg['From'] = 'vPSX_HIGH_DISK_USAGE@anydomain.com.com'
                    msg['To'] = 'anydomain.com.etec@anydomain.com, xyz.test@anydomain.com, abc.test@anydomain.com'
                    s = smtplib.SMTP('localhost')
                    s.send_message(msg)
                    s.quit()

    # Check memory usage
    ssh.connect(node, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(memory_command)
    memory_usage = stdout.read().decode().strip()
    command_output = stdout.read().decode()
    ssh.close()

    if float(memory_usage) >= memory_threshold:
        # Send an email to the device owner
        msg = MIMEText(f'NBI vPSX {node} CURRENT MEMORY USAGE above {memory_threshold}%\n\n' \
                       f'COMMAND -->>  {memory_command}\n'\
                       f'{command_output}\n'\
                       f'CURRENT MEM USAGE %-->>  {memory_usage}\n'\
                       f'NBI vPSX - PLEASE PLAN TO RESTART SOFTSWITCH ON {node} -  OSMC TEAM PLEASE SEND TICKET TO ETEC anydomain.com')
        msg['Subject'] = f'NBI vPSX - {node} CURRENT MEMORY USAGE above {memory_threshold}% PLEASE RESTART SOFTSWITCH'
        msg['From'] = 'nODE_HIGH_MEMORY_USAGE@anydomain.com'
        msg['To'] = 'blabla@anydomain.com, la.test@anydomain.com'
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()

    # Run the CPU command and save output to file
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(node, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(cpu_command)
    cpu_output = stdout.read().decode()
    with open(f'{node}_cpu.txt', 'w') as f:
        f.write(cpu_output)
    ssh.close()

    # Check if the CPU usage is above the threshold
    if float(cpu_output) >= cpu_threshold:
        # Send an email to the device owner

        msg = MIMEText(f'{node} CPU USAGE above {cpu_threshold}%\n\n' \
                       f'Command to check CPU Usage-->>  {cpu_command}\n' \
                       f'Current CPU Usage % -->>  {cpu_output}')
        msg['Subject'] = f'{node} CPU USAGE above {cpu_threshold}%'
        msg['From'] = 'nODE_HIGH_CPU_USAGE@anydomain.com'
        msg['To'] = 'anydomain.etec@anydomain.com, bla.bla@anydomain.com, la.la@anydomain.com'

        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()

    
    

    os.remove(f'{node}_disk.txt')
    os.remove(f'{node}_cpu.txt')
