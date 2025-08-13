import json
import psutil
import subprocess
# از pynvml برای GPU دقیق‌تر استفاده می‌کنیم
try:
    import pynvml
except ImportError:
    pynvml = None

# ======================================================================================================================
def get_battery_info():
    """اطلاعات باتری"""
    try:
        batt = psutil.sensors_battery()
        if batt:
            return {
                "percent": batt.percent,
                "secs_left": batt.secsleft,
                "plugged_in": batt.power_plugged,
            }
    except Exception:
        pass
    return None

# ======================================================================================================================


def get_gpu_info_nvidia_smi():
    gpus = []
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=index,name,memory.total,memory.used,driver_version,temperature.gpu,utilization.gpu", "--format=csv,noheader,nounits"],
                                capture_output=True, text=True, check=True)
        for line in result.stdout.strip().split("\n"):
            idx, name, mem_total, mem_used, driver, temp, load = [x.strip() for x in line.split(",")]
            gpus.append({
                "id": int(idx),
                "name": name,
                "memory_total_gb": round(int(mem_total)/1024, 2),
                "memory_used_gb": round(int(mem_used)/1024, 2),
                "memory_free_gb": round((int(mem_total)-int(mem_used))/1024, 2),
                "load_percent": float(load),
                "temperature_c": float(temp),
                "driver_version": driver
            })
    except Exception as e:
        print("Error getting GPU info with nvidia-smi:", e)
    return gpus

data = {
    "battery": None,  # psutil می‌تواند باتری بدهد
    "gpu": get_gpu_info_nvidia_smi()
}

with open("system_info.json", "w") as f:
    json.dump(data, f, indent=4)


# ======================================================================================================================
def main():
    data = {
        "battery": get_battery_info(),
        "gpu": get_gpu_info_nvidia_smi(),
    }
    with open("system_info.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Host system info saved to system_info.json")

if __name__ == "__main__":
    main()
