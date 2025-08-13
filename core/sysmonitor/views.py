from rest_framework.views import APIView
from rest_framework.response import Response
import socket
import time
import platform
import psutil
import os
import json

try:
    import GPUtil
except ImportError:
    GPUtil = None

# مسیر فایل مشترک روی Host که داخل کانتینر mount شده
SHARED_INFO_FILE = os.path.join(os.path.dirname(__file__), "system_info.json")

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

        # رم
        virtual_mem = psutil.virtual_memory()
        memory_info = {
            "total_gb": round(virtual_mem.total / (1024 ** 3), 2),
            "available_gb": round(virtual_mem.available / (1024 ** 3), 2),
            "used_gb": round(virtual_mem.used / (1024 ** 3), 2),
            "usage_percent": virtual_mem.percent,
        }

        # دیسک‌ها
        disks = []
        for partition in psutil.disk_partitions():
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
                pass

        # شبکه
        network = []
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    network.append({
                        "interface": iface,
                        "ip_address": addr.address,
                        "netmask": addr.netmask,
                        "broadcast_ip": addr.broadcast,
                    })
                elif hasattr(socket, 'AF_PACKET') and addr.family == socket.AF_PACKET:
                    network.append({
                        "interface": iface,
                        "mac_address": addr.address,
                    })

        # GPU
        gpus = []
        if GPUtil:
            try:
                for gpu in GPUtil.getGPUs():
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
            except Exception:
                gpus = []

        # باتری
        battery = None
        if hasattr(psutil, "sensors_battery"):
            try:
                batt = psutil.sensors_battery()
                if batt:
                    battery = {
                        "percent": batt.percent,
                        "secs_left": batt.secsleft,
                        "plugged_in": batt.power_plugged,
                    }
            except Exception:
                battery = None

        # fallback به فایل system_info.json اگر GPU یا باتری پیدا نشد
        if (not gpus or battery is None) and os.path.exists(SHARED_INFO_FILE):
            try:
                with open(SHARED_INFO_FILE, 'r') as f:
                    shared = json.load(f)
                    if not gpus:
                        gpus = shared.get("gpu", [])
                    if battery is None:
                        battery = shared.get("battery", None)
            except Exception as e:
                print("Error reading system_info.json:", e)

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
        # CPU
        cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
        cpu_total_percent = psutil.cpu_percent(interval=None)  # درصد کل CPU بدون وقفه
        cpu_freq = psutil.cpu_freq()
        cpu_info = {
            "total_usage_percent": cpu_total_percent,
            "per_core_usage_percent": cpu_percent_per_core,
            "cores_physical": psutil.cpu_count(logical=False),
            "cores_logical": psutil.cpu_count(logical=True),
            "max_frequency_mhz": cpu_freq.max if cpu_freq else None,
            "min_frequency_mhz": cpu_freq.min if cpu_freq else None,
            "current_frequency_mhz": cpu_freq.current if cpu_freq else None,
        }

        # رم
        mem = psutil.virtual_memory()
        memory_info = {
            "total_gb": round(mem.total / (1024 ** 3), 2),
            "used_gb": round(mem.used / (1024 ** 3), 2),
            "available_gb": round(mem.available / (1024 ** 3), 2),
            "usage_percent": mem.percent,
        }

        # دیسک
        disk = psutil.disk_usage('/')
        disk_info = {
            "total_gb": round(disk.total / (1024 ** 3), 2),
            "used_gb": round(disk.used / (1024 ** 3), 2),
            "free_gb": round(disk.free / (1024 ** 3), 2),
            "usage_percent": disk.percent,
        }

        # GPU
        gpus = []
        if 'GPUtil' in globals() and GPUtil:
            try:
                for gpu in GPUtil.getGPUs():
                    gpus.append({
                        "id": gpu.id,
                        "name": gpu.name,
                        "memory_total_gb": round(gpu.memoryTotal / 1024, 2),
                        "memory_used_gb": round(gpu.memoryUsed / 1024, 2),
                        "memory_free_gb": round(gpu.memoryFree / 1024, 2),
                        "load_percent": round(gpu.load * 100, 1),
                        "temperature_c": gpu.temperature,
                    })
            except Exception:
                gpus = []

        # زمان روشن بودن سیستم
        uptime_seconds = int(time.time() - psutil.boot_time())

        data = {
            "cpu": cpu_info,
            "memory": memory_info,
            "disk": disk_info,
            "gpu": gpus,
            "uptime_seconds": uptime_seconds
        }

        return Response(data)


# ======================================================================================================================