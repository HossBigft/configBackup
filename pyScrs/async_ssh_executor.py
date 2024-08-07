import asyncio


async def _run_command_over_ssh(host, username, command, verbose: bool):
    ssh_command = f'ssh {username}@{host} "{command}"'
    process = await asyncio.create_subprocess_shell(
        ssh_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    if verbose:
        print(f"{host} {ssh_command}| Awaiting result...")
    stdout, stderr = await process.communicate()
    if verbose:
        print(f"{host} answered: {stdout.decode()}")

    return (host, stdout.decode(), stderr.decode(), process.returncode)


async def _batch_ssh_command_prepare(servers, username, command, verbose: bool):
    tasks = [
        _run_command_over_ssh(host, username, command, verbose) for host in servers
    ]
    results = await asyncio.gather(*tasks)
    return [
        {"host": host, "stdout": stdout, "stderr": stderr}
        for host, stdout, stderr, *_ in results
    ]


def batch_ssh_command_result(servers, username, command, verbose=False):
    return asyncio.run(_batch_ssh_command_prepare(servers, username, command, verbose))
