from rest_framework.views import APIView  # برای ایجاد view در Django REST Framework (API endpoint)
from rest_framework.response import Response  # برای ارسال پاسخ HTTP از view‌ها در قالب JSON
import socket  # برای دسترسی به اطلاعات شبکه مانند hostname، IP و MAC
import time  # برای کار با زمان و محاسبه اختلاف زمان یا وقفه‌ها (sleep)
import platform  # برای دریافت اطلاعات سیستم عامل و سخت‌افزار
import psutil  # برای دسترسی به اطلاعات سخت‌افزاری سیستم (CPU، RAM، دیسک، شبکه، باتری و …)
import GPUtil  # برای دریافت اطلاعات کارت گرافیک (GPU) مانند مصرف حافظه، دما و بار پردازنده
import wmi  # مخصوص ویندوز، برای دسترسی به اطلاعات سخت‌افزاری مانند GPU، CPU، دیسک و … از طریق Windows Management Instrumentation
# ======================================================================================================================
# کلاس کمکی برای گرفتن اطلاعات GPU (هم GPUtil و هم WMI)
# ======================================================================================================================
class GPUInfoHelper:
    @staticmethod
    def get_gpus():
        """
        گرفتن اطلاعات کارت گرافیک‌ها
        با استفاده از GPUtil و WMI (برای ویندوز)
        """
        gpus = []

        # اگر GPUtil نصب و در دسترس باشد
        if GPUtil:
            try:
                for gpu in GPUtil.getGPUs():
                    gpus.append({
                        "id": gpu.id,
                        "name": gpu.name,
                        "uuid": getattr(gpu, 'uuid', None),
                        "driver_version": getattr(gpu, 'driver_version', None),
                        "memory_total_gb": round(gpu.memoryTotal / 1024, 2),
                        "memory_used_gb": round(gpu.memoryUsed / 1024, 2),
                        "memory_free_gb": round(gpu.memoryFree / 1024, 2),
                        "memory_utilization_percent": round(gpu.memoryUtil * 100, 1) if hasattr(gpu, 'memoryUtil') else None,
                        "load_percent": round(gpu.load * 100, 1),
                        "temperature_c": gpu.temperature,
                        "fan_speed_percent": getattr(gpu, 'fanSpeed', None),
                        "pci_bus_id": getattr(gpu, 'pciBusID', None),
                    })
            except Exception:
                pass

        # گرفتن اطلاعات GPU از طریق WMI (برای ویندوز)
        if wmi:
            try:
                c = wmi.WMI()
                for gpu in c.Win32_VideoController():
                    gpus.append({
                        "name": gpu.Name,
                        "driver_version": getattr(gpu, "DriverVersion", None),
                        "memory_total_mb": getattr(gpu, "AdapterRAM", 0) // (1024 ** 2),
                        "status": getattr(gpu, "Status", None),
                    })
            except Exception:
                pass

        return gpus
# ======================================================================================================================
# کلاس برای گرفتن اطلاعات کامل سیستم
# ======================================================================================================================
class SystemInfoView(APIView):
    def get(self, request):
        # اطلاعات سیستم عامل
        os_info = {
            "name": platform.system(),
            "version": platform.version(),
            "release": platform.release(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "fqdn": socket.getfqdn(),
        }

        # اطلاعات CPU
        cpu_freq = psutil.cpu_freq()
        cpu_info = {
            "model": platform.processor(),
            "cores_physical": psutil.cpu_count(logical=False),
            "cores_logical": psutil.cpu_count(logical=True),
            "max_frequency_mhz": cpu_freq.max if cpu_freq else None,
            "min_frequency_mhz": cpu_freq.min if cpu_freq else None,
            "current_frequency_mhz": cpu_freq.current if cpu_freq else None,
        }

        # اطلاعات حافظه
        virtual_mem = psutil.virtual_memory()
        memory_info = {
            "total_gb": round(virtual_mem.total / (1024 ** 3), 2),
            "available_gb": round(virtual_mem.available / (1024 ** 3), 2),
            "used_gb": round(virtual_mem.used / (1024 ** 3), 2),
            "usage_percent": virtual_mem.percent,
        }

        # اطلاعات دیسک‌ها
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
                # برخی پارتیشن‌ها ممکن است دسترسی نداشته باشند
                pass

        # اطلاعات شبکه
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

        # اطلاعات باتری
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

        # جمع‌بندی داده‌ها
        data = {
            "operating_system": os_info,
            "cpu": cpu_info,
            "memory": memory_info,
            "disks": disks,
            "network": network,
            "gpu": GPUInfoHelper.get_gpus(),
            "battery": battery,
        }

        return Response(data)
# ======================================================================================================================
# کلاس برای گرفتن وضعیت فعلی سیستم (لحظه‌ای)
# ======================================================================================================================
class SystemStatusView(APIView):
    def get(self, request):
        # مصرف CPU به صورت درصدی برای هر هسته
        cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
        cpu_total_percent = sum(cpu_percent_per_core) / len(cpu_percent_per_core)
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

        # اطلاعات حافظه با محاسبه تغییر مصرف
        mem1 = psutil.virtual_memory()
        time.sleep(0.5)
        mem2 = psutil.virtual_memory()
        memory_info = {
            "total_gb": round(mem2.total / (1024 ** 3), 2),
            "used_gb": round(mem2.used / (1024 ** 3), 2),
            "available_gb": round(mem2.available / (1024 ** 3), 2),
            "usage_percent": mem2.percent,
            "used_delta_mb": round((mem2.used - mem1.used) / (1024 ** 2), 2),
        }

        # اطلاعات دیسک با محاسبه تغییر مصرف
        disk_info = []
        for partition in psutil.disk_partitions():
            try:
                usage1 = psutil.disk_usage(partition.mountpoint)
                time.sleep(0.2)
                usage2 = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    "device": partition.device,
                    "mount_point": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total_gb": round(usage2.total / (1024 ** 3), 2),
                    "used_gb": round(usage2.used / (1024 ** 3), 2),
                    "free_gb": round(usage2.free / (1024 ** 3), 2),
                    "usage_percent": usage2.percent,
                    "used_delta_mb": round((usage2.used - usage1.used) / (1024 ** 2), 2),
                })
            except PermissionError:
                continue

        # اطلاعات شبکه با محاسبه تغییرات
        net1 = psutil.net_io_counters(pernic=True)
        time.sleep(1)
        net2 = psutil.net_io_counters(pernic=True)
        network_info = {}
        for iface in net1:
            network_info[iface] = {
                "bytes_sent_mb": round(net2[iface].bytes_sent / (1024 ** 2), 2),
                "bytes_recv_mb": round(net2[iface].bytes_recv / (1024 ** 2), 2),
                "packets_sent": net2[iface].packets_sent,
                "packets_recv": net2[iface].packets_recv,
                "delta_bytes_sent_mb": round((net2[iface].bytes_sent - net1[iface].bytes_sent) / (1024 ** 2), 2),
                "delta_bytes_recv_mb": round((net2[iface].bytes_recv - net1[iface].bytes_recv) / (1024 ** 2), 2),
            }

        # اطلاعات باتری
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

        # مدت زمان روشن بودن سیستم
        uptime_seconds = int(time.time() - psutil.boot_time())

        # جمع‌بندی داده‌ها
        data = {
            "cpu": cpu_info,
            "memory": memory_info,
            "disk": disk_info,
            "network": network_info,
            "gpu": GPUInfoHelper.get_gpus(),
            "battery": battery,
            "uptime_seconds": uptime_seconds
        }

        return Response(data)
# ======================================================================================================================