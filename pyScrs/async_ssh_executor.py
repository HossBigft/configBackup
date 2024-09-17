import asyncio

PLESK_SERVER_LIST = (
    "cloud-1.hoster.kz.",
    "aturbo-2.hoster.kz.",
    "apkz1.hoster.kz.",
    "apkz2.hoster.kz.",
    "apkz3.hoster.kz.",
    "apkz4.hoster.kz.",
    "apkz6.hoster.kz.",
    "apkz7.hoster.kz.",
    "pkz37.hoster.kz.",
    "pkz47.hoster.kz.",
    "pkz48.hoster.kz.",
    "pkz49.hoster.kz.",
    "pkz50.hoster.kz.",
    "pkz58.hoster.kz.",
    "cloud-2.hoster.kz",
    "nturbo-2.hoster.kz",
    "nturbo-1.hoster.kz",
    "pkz4.hoster.kz.",
    "pkz5.hoster.kz.",
    "pkz6.hoster.kz.",
    "pkz7.hoster.kz.",
    "pkz8.hoster.kz.",
    "pkz9.hoster.kz.",
    "pkz10.hoster.kz.",
    "pkz11.hoster.kz.",
    "pkz12.hoster.kz.",
    "pkz13.hoster.kz.",
    "pkz14.hoster.kz.",
    "pkz15.hoster.kz.",
    "pkz17.hoster.kz.",
    "pkz18.hoster.kz.",
    "pkz20.hoster.kz.",
    "pkz21.hoster.kz.",
    "pkz22.hoster.kz.",
    "pkz23.hoster.kz.",
    "pkz24.hoster.kz.",
    "pkz25.hoster.kz.",
    "pkz27.hoster.kz.",
    "pkz31.hoster.kz.",
    "pkz32.hoster.kz.",
    "pkz33.hoster.kz.",
    "pkz34.hoster.kz.",
    "pkz35.hoster.kz.",
    "pkz36.hoster.kz.",
    "pkz37.hoster.kz.",
    "pkz38.hoster.kz.",
    "pkz39.hoster.kz.",
    "pkz40.hoster.kz.",
    "pkz41.hoster.kz.",
    "pkz42.hoster.kz.",
    "pkz43.hoster.kz.",
    "pkz44.hoster.kz.",
    "pkz45.hoster.kz.",
    "pkz46.hoster.kz.",
    "pkz51.hoster.kz.",
    "pkz52.hoster.kz.",
    "pkz53.hoster.kz.",
    "pkz54.hoster.kz.",
    "pkz55.hoster.kz.",
    "pkz56.hoster.kz.",
    "pkz57.hoster.kz.",
    "pkz59.hoster.kz.",
    "pkz60.hoster.kz.",
    "pkz61.hoster.kz.",
    "pkz62.hoster.kz.",
    "pkz63.hoster.kz.",
    "pkz64.hoster.kz.",
    "pkz65.hoster.kz.",
    "pkz66.hoster.kz.",
    "pkz67.hoster.kz.",
    "pkz68.hoster.kz.",
    "cloud-3.hoster.kz.",
    "cloud-4.hoster.kz.",
    "cloud-5.hoster.kz.",
    "acloud-1.hoster.kz.",
)

TEST_SERVER_LIST = ("185.111.106.116", "185.129.51.20" ,"google.com")


async def _run_command_over_ssh(host, username, command, verbose: bool , timeout=5):
    ssh_command = f'ssh  -o PasswordAuthentication=no -o ConnectTimeout={timeout} {username}@{host} "{command}"'
    process = await asyncio.create_subprocess_shell(
        ssh_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    if verbose:
        print(f"{host} {ssh_command}| Awaiting result...")
    stdout, stderr = await process.communicate()
    if verbose:
        succesfulAnswer = stdout.decode().strip()
        failAnswer = stderr.decode().strip()
        if failAnswer: 
            print(f"{host} failed: {failAnswer}")
        else:
            print(f"{host} answered: {succesfulAnswer}")

    return (host, stdout.decode().strip(), stderr.decode().strip(), process.returncode)


async def _batch_ssh_command_prepare(servers, username, command, verbose: bool):
    tasks = [
        _run_command_over_ssh(host, username, command, verbose) for host in servers
    ]
    results = await asyncio.gather(*tasks)
    return [
        {"host": host, "stdout": stdout, "stderr": stderr}
        for host, stdout, stderr, *_ in results
    ]


def batch_ssh_command_result(server_list, username, command, verbose=False, test=False):
    serverList: list
    if server_list == "plesk":
        serverList = PLESK_SERVER_LIST
    else:
        serverList = server_list

    if test:
        serverList = TEST_SERVER_LIST
        username = "root"
    return asyncio.run(
        _batch_ssh_command_prepare(serverList, username, command, verbose)
    )
