import subprocess
import json
from datetime import datetime


def scan_network(network):

    result = subprocess.run(
        ["nmap", "-O", network],
        capture_output=True,
        text=True
    )

    machines = []
    current = {}

    for line in result.stdout.split("\n"):

        if "Nmap scan report for" in line:
            if current:
                machines.append(current)
            current = {"host": line.split("for")[1].strip()}

        if "OS details:" in line:
            current["os"] = line.split(":")[1].strip()

    if current:
        machines.append(current)

    return machines


def run():

    network = input("Plage réseau (ex 192.168.1.0/24) : ")

    results = scan_network(network)

    filename = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w") as f:
        json.dump(results, f, indent=4)

    print("Audit terminé →", filename)

    return 0
