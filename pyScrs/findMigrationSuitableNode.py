import requests
import os
import argparse
import sys
import phpserialize


def getNodeInfo():
    api_key = os.getenv("VZR_API_KEY")
    api_pass = os.getenv("VZR_API_PASS")

    if not api_key or not api_pass:
        print("API keys are not set in the environment variables.")
        return 1

    vpsInfoRequest = f"https://virtualizor.hoster.kz:4085/index.php?act=servers&api=json&reslen=1000000&adminapikey={api_key}&adminapipass={api_pass}"

    try:
        response = requests.get(vpsInfoRequest)
        response.raise_for_status()  # Raise an error for bad responses
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
            ]
        }
        for record in response["servs"].values()
        # filter out inactive
        if not record["status"] == "0" or not record["total_space"] == 0
    ]

    return server_info


if __name__ == "__main__":
    server_info = getNodeInfo()
    server_info = [
        server
        for server in server_info
        if (
            (
                (
                    int(server["total_space"])
                    - int(server["space"]) / int(server["total_space"])
                )
                * 10000
                + 100
                - 1
            )
            / 100
        ) > 89
    ]
    server_info = sorted(server_info, key=lambda d: int(d["space"]))
    for server in server_info:
        print(
            f"{server['server_name']}|{server['ip']}|{'Online' if int(server['status'])==1 else 'Offline' if int(server['status'])==0 else server['status']}|Space:{int(server['total_space']) - int(server['space'])}/{server['total_space']}GB|Free {server['space']}GB|"
        )
