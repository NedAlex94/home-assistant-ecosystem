
## Updating Homeassistant

HA is installed in a Proxmox LXC container, using Python.

### Before you begin:

Backup the Proxmox LXC.

### Steps:

#### Connect to Proxmox (web interface or SSH).
1) Click on the LXC and login using credentials.
2) Navigate to the Home Assistant directory: /srv/homeassistant
3) Stop HA sudo systemctl stop homeassistant
4) Activate virtual environment : source /srv/homeassistant/bin/activate

5) Update with pip: pip install --upgrade homeassistant (wait for download and installation).

6) Restart Home Assistant: sudo systemctl restart homeassistant
 
