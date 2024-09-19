### Updating Ollama Server

Ollama Server is installed in a Debian LXC container on Proxmox.

#### Installation Process

Follow the official guide with the necessary adjustments for LXC:

1. Install curl:
   ```bash
   apt install curl
   ```

2. Install Ollama:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

3. Set up the server:
   ```bash
   export OLLAMA_HOST=0.0.0.0
   ollama serve   # Use 'ollama serve &' to run in the background if terminal access is needed
   ```

#### Getting and Running Models

Models can be found at [Ollama Library](https://ollama.com/library).

To install and run a model:
```bash
ollama run <model_name>
```

### Passing iGPU to the Proxmox LXC

Sure! Here’s the continuation of your current guide in your preferred style:

---

### Adding Intel iGPU to LXC in Proxmox

#### Step 1: Enable IOMMU

1. Edit the GRUB configuration file:
   ```bash
   nano /etc/default/grub
   ```

2. Add `intel_iommu=on` to the `GRUB_CMDLINE_LINUX_DEFAULT` line, so it looks like this:
   ```bash
   GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on"
   ```

#### Step 2: Load the i915 Module at Boot

1. Edit the `/etc/modules` file to load the i915 module automatically (might not be needed):
   ```bash
   nano /etc/modules
   ```

2. Add this line at the end and save the file:
   ```bash
   i915
   ```

#### Update GRUB and Reboot

1. Update GRUB and reboot the system:
   ```bash
   update-grub
   reboot
   ```


#### Step 3: Find the iGPU Device Path

1. After rebooting, check for the iGPU device path:
   ```bash
   ls -l /dev/dri
   ```

   You should see:
   ```
   card1
   renderD128
   ```

#### Step 4: Add the iGPU to the LXC via the Proxmox UI

1. In Proxmox UI, go to **Datacenter > Your LXC > Hardware**.
2. Click **Add > Device > GPU**.
3. Set the device path to:
   - **/dev/dri/renderD128** for rendering tasks.
   - **/dev/dri/card1** for general GPU access.
4. Save and restart the container:
   ```bash
   pct restart 101
   ```
