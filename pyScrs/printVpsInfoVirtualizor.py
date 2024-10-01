import requests
import os
import argparse
import sys
import phpserialize


def vInfoVpsGet(vps_hostname):
    """
    Returns info about given Virtualizor VPS by hostname.
    """
    api_key = os.getenv("VZR_API_KEY")
    api_pass = os.getenv("VZR_API_PASS")

    if not api_key or not api_pass:
        print("API keys are not set in the environment variables.")
        return 1

    if not vps_hostname:
        print("Empty input")
        return 1

    # Make the API request
    url = f"https://virtualizor.hoster.kz:4085/index.php?act=vs&vpshostname={vps_hostname}&api=json&adminapikey={api_key}&adminapipass={api_pass}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        request_result = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return 1
    request_result = {
        k: v
        for server_record in request_result["vs"].values()
        for k, v in server_record.items()
        if k
        in [
            "hostname",
            "vps_name",
            "vpsid",
            "os_name",
            "space",
            "ram",
            "cores",
            "network_speed",
            "upload_speed",
            "suspended",
            "nic_type",
            "cpu_mode",
            "server_name",
            "email",
            "cached_disk",
        ]
        or (k == "ips" and {f"ips:{ip}" for ip in v.values()})
    }

    ips = request_result["ips"]

    ip_list = [f"ips:{ip}" for ip in ips.values()]

    serialized_data = request_result["cached_disk"]
    data = phpserialize.loads(serialized_data.encode("utf-8"))

    # Convert byte strings to regular strings
    disk_data = {
        k.decode("utf-8"): {
            kk.decode("utf-8"): vv.decode("utf-8") for kk, vv in v.items()
        }
        for k, v in data.items()
    }
    filesystem = disk_data["disk"]["Filesystem"]
    total_gb = round(int(disk_data["disk"]["1K-blocks"]) / 1048576, 3)
    used_gb = round(int(disk_data["disk"]["Used"]) / 1048576, 3)
    used_Percent = disk_data["disk"]["Use%"]

    total_inodes = disk_data["inode"]["Inodes"]
    used_inodes = disk_data["inode"]["IUsed"]
    used_inodes_Percent = disk_data["inode"]["IUse%"]

    # Display results
    print(f"IP|{' '.join(ip_list)}")
    print(f"ID|{request_result['vpsid']}\\{request_result['vps_name']}")
    print(f"Hostname|{request_result['hostname']}")

    print(f"Disk Info|{request_result['space']}")
    print(f"Filesystem|{filesystem}")
    print(f"Space||{used_Percent}/100%|{used_gb}/{total_gb}gB")
    print(f"Inode|{used_inodes_Percent}/100%|{used_inodes}/{total_inodes}")

    print(f"User|{request_result['email']}")
    print(f"Is suspended|{request_result['suspended']}")
    print(f"Server|{request_result['server_name']}")
    print(f"OS|{request_result['os_name']}")
    print(f"NIC|{request_result['nic_type']}")
    print(f"Space|{request_result['space']}")
    print(f"RAM|{request_result['ram']}")
    print(f"CPU mode|{request_result['cpu_mode']}")
    print(f"Cores|{request_result['cores']}")
    print(f"Network speed|{request_result['network_speed']}")
    print(f"Upload speed|{request_result['upload_speed']}")

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get information about a Virtualizor VPS by hostname."
    )
    parser.add_argument("vps_hostname", help="The hostname of the VPS to query.")

    args = parser.parse_args()

    # Call the function with the parsed argument
    exit_code = vInfoVpsGet(args.vps_hostname)
    sys.exit(exit_code)
