import argparse
import socket
import sys
import requests


def main():
    parser = argparse.ArgumentParser(description="Queries ipinfo.io about IP geodata")

    parser.add_argument(
        "ip",
        nargs="?",
        type=str,
        help="list of IPs to ",
    )
    args = parser.parse_args()

    if args.ip:
        ip_list = args.ip.splitlines()
    else:
        ip_list = sys.stdin.read().strip().splitlines()

    for ip in ip_list:
        r = requests.get(f"https://ipinfo.io/{ip.strip()}")
        json = r.json()
        ip = json["ip"]

        country: str
        try:
            country = json["country"]
        except KeyError:
            country = ""

        org: str
        try:
            org = json["org"]
        except KeyError:
            org = ""

        ptr: str
        try:
            ptr = socket.getfqdn(socket.gethostbyaddr(json["ip"])[0])
        except socket.herror:
            ptr = f"No result for {json['ip']}"

        print(f"ip:{ip}")
        print(f"country:{country}")
        print(f"org:{org}")
        print(f"PTR:{ptr}")

        print("⋁" * len(f"PTR:{ptr}"))


if __name__ == "__main__":
    main()
