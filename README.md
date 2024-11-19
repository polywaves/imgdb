1. Setup docker and nvidia environment by this guide https://docs.nvidia.com/ai-enterprise/deployment/vmware/latest/docker.html
2. Fix cuda - sudo nano /etc/nvidia-container-runtime/config.toml, then changed no-cgroups = false, save
Then restart docker daemon: sudo systemctl restart docker