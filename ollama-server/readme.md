
## Updating Homeassistant

Ollama server is installed in a Debian LXC (container) in Proxmox.

### Installation Process
The installation process follows the official guide, with minor adjustments to make it work in an LXC.


curl -fsSL https://ollama.com/install.sh | sh

apt install curl

...

export OLLAMA_HOS=0.0.0.0

ollama serve, or ollama serve & if needing to interact with the terminal

### Getting and Running Models

Models are available at https://ollama.com/library

Install and run a model using "ollama run model_name"
