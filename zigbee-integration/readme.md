### Guide: Integrating Zigbee with Home Assistant on Proxmox

This guide documetns the steps for integrating Zigbee coordinator into my Home Assistant installation running in a Proxmox LXC container.

#### Hardware Required

- **Sonoff USB Zigbee 3.0 Dongle (ZBDongle-E)**: It is plug and play, but the device must be correctly initiated into the Proxmox server and correctly passed to HA.

------------

#### Step 1: Initiate Device and Get USB ID

1. **Connect the Dongle**: Plug the Zigbee dongle into a USB 2.0 port on your server. USB 3.0 has been reported to cause interference.
   
2. **Identify the Device**: On the Proxmox host, list connected USB devices to get the vendor ID and product ID:
   ```bash
   lsusb
   ```
   Example output:
   ```
   Bus 001 Device 004: ID 1a86:55d4 QinHeng Electronics SONOFF Zigbee 3.0 USB Dongle Plus V2
   ```
   - `1a86` is the vendor ID (QinHeng Electronics).
   - `55d4` is the product ID (SONOFF Zigbee 3.0 USB Dongle Plus V2).

3. **Retrieve Device Path**: Use the device information from the `lsusb` command to find the device path:
   ```bash
   udevadm info -q path -n /dev/bus/usb/001/004
   ```
   Replace `001` and `004` with your specific device info from the `lsusb` output.
   Example output:
   ```
   /devices/pci0000:00/0000:00:14.0/usb1/1-7
   ```

4. **Find the Device Serial**: This helps in identifying the exact device path:
   ```bash
   ls -l /dev/serial/by-id/
   ```
   Example output:
   ```
   lrwxrwxrwx 1 root root 13 Aug 9 23:12 usb-ITEAD_SONOFF_Zigbee_3.0_USB_Dongle_Plus_V2_20231122155837-if00 -> ../../ttyACM0
   ```
   What we need is *ttyACM0*.

------------

#### Step 2: Pass the Device to Home Assistant LXC

1. **Identify the LXC ID for Home Assistant**:
   ```bash
   pct list
   ```
   Look for the `homeassistant-core` in the output to find your LXC ID.
   Example output:
   ```
   114 running homeassistant-core-test
   ```

2. **Modify the LXC Configuration:**
   - Open the LXC configuration file for the Home Assistant container:
     ```bash
     nano /etc/pve/lxc/114.conf
     ```
   - Add the following lines to pass the USB device to the container:
     ```bash
     lxc.cgroup2.devices.allow: c 166:* rwm
     lxc.mount.entry: /dev/ttyACM0 dev/ttyACM0 none bind,optional,create=file
     ```
	 
   - Save and close the file using *ctrl + x*.

3. **Ensure Permissions:**
   If you encounter issues with permissions, set the correct permissions on the device:
   ```bash
   chmod 666 /dev/ttyACM0
   ```

4. **Restart the LXC Container:**
   After modifying the configuration file, restart the container to apply the changes:
   ```bash
   pct restart 114
   ```
  Or manually restart from the GUI.

------------


#### Step 3: Add integration in Home Assistant


