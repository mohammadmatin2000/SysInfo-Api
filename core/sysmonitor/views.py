from rest_framework.views import APIView
from rest_framework.response import Response
import socket
import time
import platform
import psutil
import GPUtil

# ======================================================================================================================
class SystemInfoView(APIView):
    def get(self, request):
        # سیستم عامل
        os_info = {
            "name": platform.system(),
            "version": platform.version(),
            "release": platform.release(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "fqdn": socket.getfqdn(),
        }

        # CPU
        cpu_freq = psutil.cpu_freq()
        cpu_info = {
            "model": platform.processor(),
            "cores_physical": psutil.cpu_count(logical=False),
            "cores_logical": psutil.cpu_count(logical=True),
            "max_frequency_mhz": cpu_freq.max if cpu_freq else None,
            "min_frequency_mhz": cpu_freq.min if cpu_freq else None,
            "current_frequency_mhz": cpu_freq.current if cpu_freq else None,
        }

        # رم (حافظه)
        virtual_mem = psutil.virtual_memory()
        memory_info = {
            "total_gb": round(virtual_mem.total / (1024 ** 3), 2),
            "available_gb": round(virtual_mem.available / (1024 ** 3), 2),
            "used_gb": round(virtual_mem.used / (1024 ** 3), 2),
            "usage_percent": virtual_mem.percent,
        }

        # دیسک‌ها
        disk_partitions = psutil.disk_partitions()
        disks = []
        for partition in disk_partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    "device": partition.device,
                    "mount_point": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total_gb": round(usage.total / (1024 ** 3), 2),
                    "used_gb": round(usage.used / (1024 ** 3), 2),
                    "free_gb": round(usage.free / (1024 ** 3), 2),
                    "usage_percent": usage.percent,
                })
            except PermissionError:
                pass  # بعضی پارتیشن‌ها اجازه دسترسی ندارند

        # شبکه
        net_if_addrs = psutil.net_if_addrs()
        network = []
        for interface_name, addresses in net_if_addrs.items():
            for addr in addresses:
                if addr.family == socket.AF_INET:  # IPv4
                    network.append({
                        "interface": interface_name,
                        "ip_address": addr.address,
                        "netmask": addr.netmask,
                        "broadcast_ip": addr.broadcast,
                    })
                elif addr.family == socket.AF_PACKET:  # MAC Address
                    network.append({
                        "interface": interface_name,
                        "mac_address": addr.address,
                    })

        # GPU
        gpus = []
        try:
            gpu_list = GPUtil.getGPUs()
            for gpu in gpu_list:
                gpus.append({
                    "id": gpu.id,
                    "name": gpu.name,
                    "driver_version": getattr(gpu, 'driver_version', None),
                    "memory_total_gb": round(gpu.memoryTotal / 1024, 2),
                    "memory_used_gb": round(gpu.memoryUsed / 1024, 2),
                    "memory_free_gb": round(gpu.memoryFree / 1024, 2),
                    "load_percent": round(gpu.load * 100, 1),
                    "temperature_c": gpu.temperature,
                })
        except Exception as e:
            gpus.append({"error": str(e)})

        # باتری
        battery = None
        if hasattr(psutil, "sensors_battery"):
            batt = psutil.sensors_battery()
            if batt:
                battery = {
                    "percent": batt.percent,
                    "secs_left": batt.secsleft,
                    "plugged_in": batt.power_plugged,
                }

        # ساختار نهایی
        data = {
            "operating_system": os_info,
            "cpu": cpu_info,
            "memory": memory_info,
            "disks": disks,
            "network": network,
            "gpu": gpus,
            "battery": battery,
        }

        return Response(data)

# ======================================================================================================================
class SystemStatusView(APIView):
    def get(self, request):
        # مصرف CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        # مصرف رم
        mem = psutil.virtual_memory()
        # مصرف دیسک
        disk = psutil.disk_usage('/')
        # آپتایم
        uptime_seconds = time.time() - psutil.boot_time()

        data = {
            "cpu_usage_percent": cpu_percent,
            "memory": {
                "total_gb": round(mem.total / (1024 ** 3), 2),
                "used_gb": round(mem.used / (1024 ** 3), 2),
                "available_gb": round(mem.available / (1024 ** 3), 2),
                "usage_percent": mem.percent,
            },
            "disk": {
                "total_gb": round(disk.total / (1024 ** 3), 2),
                "used_gb": round(disk.used / (1024 ** 3), 2),
                "free_gb": round(disk.free / (1024 ** 3), 2),
                "usage_percent": disk.percent,
            },
            "uptime_seconds": int(uptime_seconds)
        }
        return Response(data)
