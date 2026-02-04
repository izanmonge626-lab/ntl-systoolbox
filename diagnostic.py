import platform
import psutil
import json
from datetime import datetime


def run():

    data = {
        "os": platform.system(),
        "os_version": platform.version(),
        "uptime_minutes": int(psutil.boot_time()),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "ram_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }

    filename = f"diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print("Diagnostic terminé →", filename)

    return 0