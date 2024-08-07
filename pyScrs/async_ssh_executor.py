import asyncio
import shlex
   
async def run_command_over_ssh(host, username, command):
    ssh_command = shlex.split(f"ssh {username}@{host} {command}")
    
    process = await asyncio.create_subprocess_exec(
        *ssh_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    print(host, stdout.decode())
    return (host, stdout.decode(), stderr.decode(), process.returncode)

async def batch_ssh_command(servers, command, username):
    tasks = [run_command_over_ssh(host, username, command) for host in servers]
    results = await asyncio.gather(*tasks)
    return [{"host":host, "stdout":stdout,"stderr":stderr} for host, stdout, stderr, *_ in results]


