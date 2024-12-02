OPERATING SYSTEM - UBUNTU 24.04

1. Setup docker and nvidia environment by this guide https://docs.nvidia.com/ai-enterprise/deployment/vmware/latest/docker.html
2. Fix cuda runtime for docker - sudo nano /etc/nvidia-container-runtime/config.toml, change to no-cgroups = false, save

Then restart docker daemon: sudo systemctl restart docker

3. If using docker swarm - https://gist.github.com/RafaelWO/290b764e88933b0c0769b6d2394fcad2


Useful articles:
1. Format and mount disk https://techguides.yt/guides/how-to-partition-format-and-auto-mount-disk-on-ubuntu-20-04/