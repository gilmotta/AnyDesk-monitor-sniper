import psutil
import os
import time
import smtplib
from email.mime.text import MIMEText
import subprocess
from colorama import Fore, init
import socket

# Initialize colorama for colored terminal output
init(autoreset=True)

# Define AnyDesk process and service names
ANYDESK_PROCESS_NAME = "AnyDesk.exe"
ANYDESK_SERVICE_NAME = "AnyDesk"
LOG_FILE = "kmkz-monitor-sniper.log"

# Get the PC's hostname
PC_NAME = socket.gethostname()

# Define email details with PC name
EMAIL_SUBJECT = f"AnyDesk Alert - {PC_NAME}"  # Dynamically append the PC name to the subject
EMAIL_FROM = "youremail@gmail.com"
EMAIL_TO = "toyouremail@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Function to log messages to the console and file
def log_message(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_entry = f"{timestamp} - {PC_NAME} - {message}"
    print(log_entry)
    
    # Write to log file
    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_entry + "\n")

# Function to send an email alert and log it
def send_alert(subject, message):
    log_message("Preparing to send email alert...")

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    # Retrieve password from the environment variable
    SMTP_PASSWORD = os.getenv('YOUREMAILPASSWORDVAR')

    try:
        # Log the email content for thoroughness
        log_message(f"Email Subject: {subject}")
        log_message(f"Email From: {EMAIL_FROM}")
        log_message(f"Email To: {EMAIL_TO}")
        log_message(f"Email Content: {message}")

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, SMTP_PASSWORD)  # Use environment variable
        server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        server.quit()

        log_message("Alert email sent successfully.")
    except Exception as e:
        log_message(f"Error sending alert email: {e}")

# Function to check if a process is running and log it
def is_process_running(process_name):
    log_message(f"Checking if process {process_name} is running...")
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            log_message(f"{process_name} is running!")
            return True
    log_message(f"{process_name} is NOT running.")
    return False

# Function to kill a process by name and log it
def kill_process(process_name):
    try:
        log_message(f"Attempting to kill process {process_name}...")
        os.system(f"taskkill /IM {process_name} /F")
        log_message(f"{process_name} process killed successfully!")
    except Exception as e:
        log_message(f"Failed to kill {process_name}: {e}")

# Function to disable the AnyDesk service and log it
def disable_anydesk_service():
    log_message("Checking and disabling AnyDesk service if necessary...")
    try:
        # Command to disable AnyDesk service
        command = 'sc config AnyDesk start= disabled'
        
        # Log the command being executed
        log_message(f"Executing command: {command}")
        subprocess.run(command, shell=True, check=True)
        
        log_message("Successfully disabled AnyDesk service.")
    except subprocess.CalledProcessError as e:
        log_message(f"Error disabling AnyDesk service: {e}")

def monitor_anydesk():
    """Monitor AnyDesk process and service, and take action if detected."""
    while True:
        # Check for AnyDesk process
        if is_process_running(ANYDESK_PROCESS_NAME):
            log_message(Fore.RED + "ALERT: AnyDesk process detected running!")
            
            # Kill the AnyDesk process
            kill_process(ANYDESK_PROCESS_NAME)
            
            # Send an alert email (optional)
            send_alert(EMAIL_SUBJECT, f"AnyDesk process detected and killed on {PC_NAME}!")
        
        time.sleep(10)

if __name__ == "__main__":
    log_message("Starting AnyDesk monitoring script...")

    # Disable AnyDesk service on script start and log the action
    disable_anydesk_service()

    # Start monitoring the AnyDesk process and log any detections
    monitor_anydesk()
