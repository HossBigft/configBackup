import requests
import os
import sys
import typer
from termcolor import colored


def getNodeInfo():
    api_key = os.getenv("VZR_API_KEY")
    api_pass = os.getenv("VZR_API_PASS")

    if not api_key or not api_pass:
        print("API keys are not set in the environment variables.")
        return 1

    vpsInfoRequest = f"https://virtualizor.hoster.kz:4085/index.php?act=servers&api=json&reslen=1000000&adminapikey={api_key}&adminapipass={api_pass}"

    try:
        response = requests.get(vpsInfoRequest)
        response.raise_for_status()
        response = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return 1
    server_info = [
        {
            k: record[k]
            for k in [
                "serid",
                "ip",
                "os",
                "ram",
                "space",
                "total_space",
                "status",
                "server_name",
                "ram",
                "total_ram",
            ]
        }
        for record in response["servs"].values()
        if not (
            record["status"] == "0"
            or record["total_space"] == 0
            or record["server_name"] == "virtualizor.hoster.kz"
        )
    ]

    for server in server_info:
        server["total_space"] = int(server["total_space"])
        server["space"] = int(server["space"])
        server["used_space"] = server["total_space"] - server["space"]
        server["used_space_percent"] = round(
            (((server["used_space"] / server["total_space"]) * 10000 + 100 - 1) / 100),
            2,
        )

        server["total_ram"] = round(int(server["total_ram"]) / 1024, 2)
        server["ram"] = round(int(server["ram"]) / 1024, 2)
        server["used_ram"] = round(server["total_ram"] - server["ram"], 2)
        server["used_ram_percent"] = round(
            (((server["used_ram"] / server["total_ram"]) * 10000 + 100 - 1) / 100), 2
        )

    return server_info


def main(machine_size: float, machine_ram: float):
    """
    machine_size --- size of machine to be migrated in GB

    machine_ram --- RAM size of machine to be migrated in GB
    """
    server_info = getNodeInfo()
    server_info = [
        server
        for server in server_info
        if not (server["used_space_percent"] >= 89 or server["used_ram_percent"] >= 89)
    ]
    for server in server_info:
        server["used_space_after"] = server["total_space"] - (
            server["space"] - machine_size
        )

        server["free_space_after"] = server["total_space"] - server["used_space_after"]

        server["used_space_percent_after"] = round(
            (
                ((server["used_space_after"] / server["total_space"]) * 10000 + 100 - 1)
                / 100
            ),
            2,
        )

        server["used_ram_after"] = round(
            server["total_ram"] - (server["ram"] - machine_ram), 2
        )
        server["free_ram_after"] = server["total_ram"] - server["used_ram_after"]
        server["used_ram_percent_after"] = round(
            (
                ((server["used_ram_after"] / server["total_ram"]) * 10000 + 100 - 1)
                / 100
            ),
            2,
        )

    server_info = [
        server
        for server in server_info
        if not (
            server["used_space_percent_after"] >= 89
            or server["used_ram_percent_after"] >= 89
        )
    ]
    for server in server_info:
        print(server["used_space_percent_after"])
    server_info = sorted(server_info, key=lambda d: (d["space"], d["ram"]))
    for server in server_info:
        print(
            f"{colored('Online','green') if int(server['status'])==1 else colored('Offline','red') if int(server['status'])==0 else server['status']}|{server['server_name']}|{server['ip']}|ID:{server['serid']}"
        )
        print(
            f"{colored('Space','light_blue')}:{server['used_space']}/{server['total_space']}GB, Free {server['space']}GB|{colored('RAM','light_yellow')}:{server['used_ram']}/{server['total_ram']}GB, Free RAM {server['ram']}GB"
        )
        print(
            f"{colored('Space','light_blue')}:{server['used_space_percent']}/100%, Free {round(100-server['used_space_percent'], 2)}%|{colored('RAM','light_yellow')}:{server['used_ram_percent']}/100%, Free RAM {round(100 -server['used_ram_percent'], 2)}%"
        )
        print(f"{server['os']}\n")


if __name__ == "__main__":
    typer.run(main)
