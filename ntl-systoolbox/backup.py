import subprocess
import json
from datetime import datetime


def run():

    backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

    cmd = [
        "mysqldump",
        "-u", "root",
        "-pPASSWORD",   # remplace par ta config
        "nom_base"
    ]

    with open(backup_file, "w") as f:
        subprocess.run(cmd, stdout=f)

    data = {
        "backup_file": backup_file,
        "status": "completed"
    }

    json_file = backup_file.replace(".sql", ".json")

    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)

    print("Backup terminé →", backup_file)

    return 0
