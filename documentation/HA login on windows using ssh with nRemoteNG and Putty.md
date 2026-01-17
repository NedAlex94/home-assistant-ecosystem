
**WHY**  
I wanted a reliable way of accessing my Home Assistant OS instance from my laptop to code using VS Code (YAML and PyScript) instead of relying on the built-in add-ons.

**REQUIREMENTS**
- Home Assistant OS running on your LAN.
- The official 'Terminal & SSH' add-on installed
- Windows laptop or desktop.
- PuTTY and PuTTYgen installed. PuTTYgen auto installs with PuTTY alongside Pageant.
- mRemoteNG installed.
- No need for port forwarding for the HA SSH port on your router. This is a local-only access guide.

---

### 1) Generate an SSH key pair with PuTTYgen
Start PuTTYgen on Windows.

Under 'Type of key to generate', select EdDSA / Ed25519.

Click Generate and move the mouse in the blank area until the bar completes. This generates the key using a random pattern.

In 'Key passphrase' and 'Confirm passphrase', enter a passphrase you want to use for this key. I reccomend a password manager to remember it.

Click Save private key and store it as e.g.:

```
C:\\Users\\<user>\\.ssh\\homeassistant.ppk
```

Select and copy the entire line that starts with ssh-ed25519 (the Public key)

At this points, we now have:
- Private key file: homeassistant.ppk (protected by your passphrase)
- Public key text: ssh-ed25519 AAAA…
- Passphrase safely saved.

---

### 2) Configure the Terminal & SSH add-on in Home Assistant
In the HA web UI, go to:

##### Settings > Add-ons > Add-on Store

Install the official Terminal & SSH add-on if it is not already installed.

Open the Terminal & SSH add-on, go to the Configuration tab.

Here, paste the public key in the authorize keys field:

```
authorized_keys:
  - 'ssh-ed25519 AAAA...paste-your-public-key-here...'
```

Leave the password empty. It more secure to login with a key instead.
In the add-on’s Network settings, map a host port to container port 22, for example:

```
SSH port: 2222 22/tc
```

Save the configuration and start (or restart) the add-on.

---

### 3) Create and test a PuTTY session
PuTTY has a very confusing UI, so don’t get discouraged if you find it confusing.

Start PuTTY.

In the Session category:

- Host Name: <HA_IP>

- Port: 2222

- Connection type: SSH

In Connection > Data:

- Auto-login username: root
- 
In Connection > SSH > Auth 
- Ensure that “Attempt authentication using Pageant” is selected.

In Connection > SSH > Auth > Credentials

“Private key file for authentication”: select

```
C:\\Users\\<user>\\.ssh\\homeassistant.ppk
```

Go back to Session:

Under “Saved Sessions”, enter homeassistant

Click Save

Test:
Select homeassistant, click Load, then Open.

Accept the host key on first connection.

PuTTY partially connects, refusing due to the missing password key.

---

### 4) Save the key password using Pageant
Open Pageant (automatically installed alongside PuTTY).
Click on 'Add Key' and select the key we made earlier 'C:\\Users\\<user>\\.ssh\\homeassistant.ppk'
Enter the key passphrase once.

While Pageant is running, PuTTY and mRemoteNG will use the unlocked key from Pageant and will not ask for the passphrase for each new connection.

---

### 5) Configure mRemoteNG to use the PuTTY session
Goal: mRemoteNG should reuse the PuTTY session homeassistant and your key.
Open mRemoteNG.

##### Ensure PuTTY path is correct and initialised:

Go to Tools > Options > Advanced.

Verify the PuTTY path points to your putty.exe.

From the same dialog, click the button to launch PuTTY once (this is required on some setups before sessions work correctly through mRemoteNG). Close PuTTY again.

In the connection tree, create a New Connection.

##### With the connection selected, set these properties:

- Name: Home Assistant (or anything you like)

- Protocol: SSH2

- Hostname: <HA_IP>

- Port: 2222

- Username: root

- PuTTY Session: homeassistant (must exactly match the session name saved in PuTTY)

Double-click the connection.

##### On connect, mRemoteNG will:
- Use the homeassistant PuTTY session,

- Use your homeassistant.ppk key,

- Prompt for the key passphrase (same as PuTTY),

- Log you into HA as root.

And that’s it :). If anyone actually reads this and whans an image tutorial, let me know.
