
## Updating Homeassistant

Ollama server is installed in a Debian LXC (container) in Proxmox.

### Installation Process
The installation process follows the official guide, with minor adjustments to make it work in an LXC.


curl -fsSL https://ollama.com/install.sh | sh

apt install curl

...

export OLLAMA_HOS=0.0.0.0

ollama serve
