# AnyDesk Monitor Sniper
# Author: Gilson Motta - 2024

**AnyDesk Monitor Sniper** is a Python script designed to monitor if the **AnyDesk** screen-sharing application is running on your Windows system. When detected, it automatically kills any running instances of AnyDesk and optionally sends an email alert.

AnyDesk is a legitimate remote access tool, but it can be exploited by hackers or unauthorized users to gain control of a system. By creating a script that monitors and terminates AnyDesk instances, you're protecting the system from unauthorized remote access attempts.

## Features
- **Monitors for AnyDesk**: Checks if the AnyDesk application is running and kills it if found.
- **Email Alerts**: Sends an email notification when AnyDesk is detected and killed (optional).
- **Service Management**: Disables AnyDesk as a Windows service to prevent it from restarting on boot.
- **Logs Activity**: Detailed logging of all activity (detections, process kills, service disabling, email notifications) for easy review.

## Getting Started

### Prerequisites

1. **Python 3.x** installed on your system.
2. Install the required Python libraries:
   ```bash
   pip install psutil colorama
3. To use the email feature:
   ```Rename the email names in the script to your correct email accounts.
   ```Create an environment variable with your SMTP email account password and replace the code with the correct variable name.

   
