1. Firstly - setup soft by this instructions and steps https://docs.nvidia.com/ai-enterprise/deployment/vmware/latest/docker.html
2. Fix cuda - sudo nano /etc/nvidia-container-runtime/config.toml, then changed no-cgroups = false, save
Then restart docker daemon: sudo systemctl restart docker