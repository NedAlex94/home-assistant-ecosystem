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
