import psutil
import gpustat
from app.utils.logger_util import logger


psutil.PROCFS_PATH = "/host/proc"


def get_cpu_usage():
  usage = psutil.cpu_percent(interval=1)

  return int(usage)


def get_memory_usage():
  usage = psutil.virtual_memory()

  return int(usage.percent)


def get_disk_usage(disk: int):
  disks = ["/", "/mnt/sda1", "/mnt/sdb1"]

  usage = psutil.disk_usage(disks[disk - 1])
  
  return int(usage.percent)


def get_gpu_usage():
  gpu_stats = gpustat.GPUStatCollection.new_query()
  usage = 0
  for gpu in gpu_stats.gpus:
    usage += gpu.utilization
  
  return int(usage)
